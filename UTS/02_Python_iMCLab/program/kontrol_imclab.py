"""Kontrol iMCLab melalui firmware Modul 01; log hanya data serial asli."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime
import math
from pathlib import Path
import re
import sys
import time

VID_PID = {(0x10C4, 0xEA60), (0x1A86, 0x7523), (0x1A86, 0x55D4),
           (0x0403, 0x6001), (0x303A, 0x1001)}
KEYWORDS = ('cp210', 'ch340', 'ch341', 'ch910', 'ft232', 'espressif', 'esp32')
STATUS = re.compile(r'^(?:DATA|ACK|STATUS) PWM=(\d+) SET=(\d+) RPM=([\d.]+) '
                    r'PULSES=(\d+) DT_MS=(\d+)$')


def normalize_command(command: str) -> str:
    command = command.strip().upper()
    if command in {'0', '1', '+', '-', 'R'}:
        return command
    match = re.fullmatch(r'(?:PWM:|P)([0-9]{1,3})', command)
    if match and 0 <= int(match[1]) <= 255:
        return f'PWM:{int(match[1])}'
    raise ValueError('Gunakan 0, 1, +, -, R, atau PWM:0..255 (p150 juga boleh).')


def select_port(ports) -> str:
    candidates = []
    for port in ports:
        description = f'{port.description or ""} {port.manufacturer or ""}'.lower()
        if 'bluetooth' in description:
            continue
        if (port.vid, port.pid) in VID_PID or any(key in description for key in KEYWORDS):
            candidates.append(port.device)
    if len(candidates) == 1:
        return candidates[0]
    raise ValueError('Port belum pasti. Gunakan --list, lalu pilih --port COMx secara eksplisit.')


class Log:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        # Mode x menjaga data eksperimen sebelumnya tidak tertimpa.
        self.file = path.open('x', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['timestamp', 'direction', 'raw', 'pwm', 'set_pwm',
                              'rpm', 'pulses', 'dt_ms'])

    def write(self, direction: str, raw: str):
        values = STATUS.fullmatch(raw) if direction == 'RX' else None
        self.writer.writerow([datetime.now().astimezone().isoformat(), direction, raw,
                              *(values.groups() if values else ('',) * 5)])
        self.file.flush()

    def close(self):
        self.file.close()


def read_for(connection, log: Log, seconds: float, require_pulses: bool = False):
    started = time.monotonic()
    deadline = started + seconds
    last_data = last_pulse = started
    while time.monotonic() < deadline:
        raw = connection.readline().decode('utf-8', errors='replace').strip()
        now = time.monotonic()
        if raw:
            log.write('RX', raw)
            print(f'ESP32: {raw}')
            values = STATUS.fullmatch(raw) if raw.startswith('DATA ') else None
            if values:
                last_data = now
                if int(values[4]) > 0:
                    last_pulse = now
        if require_pulses:
            if now - last_data >= 3:
                raise RuntimeError('DATA tidak diterima selama 3 detik; hentikan motor.')
            if now - last_pulse >= 3:
                raise RuntimeError('Pulsa tidak terdeteksi selama 3 detik; hentikan motor.')


def confirmation_matches(command: str, raw: str) -> bool:
    values = STATUS.fullmatch(raw)
    if not values:
        return False
    if command == 'R':
        return raw.startswith('STATUS ')
    if not raw.startswith('ACK '):
        return False
    pwm, target = int(values[1]), int(values[2])
    if command == '0':
        return pwm == 0
    if command == '1':
        return pwm == target and pwm > 0
    if command.startswith('PWM:'):
        return target == int(command.split(':')[1])
    return True


def send_command(connection, log: Log, command: str, timeout: float = 2):
    command = normalize_command(command)
    connection.write((command + '\n').encode('ascii'))
    connection.flush()
    log.write('TX', command)
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        raw = connection.readline().decode('utf-8', errors='replace').strip()
        if not raw:
            continue
        log.write('RX', raw)
        print(f'ESP32: {raw}')
        if raw.startswith('ERR'):
            raise RuntimeError(raw)
        if confirmation_matches(command, raw):
            return raw
    raise TimeoutError(f'Tidak ada konfirmasi untuk {command!r}. Periksa firmware/newline/port.')


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='Tampilkan port, tanpa mengirim perintah')
    parser.add_argument('--port', help='Contoh COM5; wajib jika kandidat lebih dari satu')
    parser.add_argument('--log', type=Path, help='CSV baru; nama yang sudah ada ditolak')
    parser.add_argument('--capture', type=float, help='Detik perekaman otomatis per tahap (maksimum 60)')
    parser.add_argument('--pwm', type=int, default=200, help='PWM saat --capture (0..255); default 200')
    parser.add_argument('--sweep', type=int, nargs='+', help='Urutan PWM saat --capture, contoh: 200 160 120')
    args = parser.parse_args(argv)
    if not 0 <= args.pwm <= 255 or (args.capture is not None and (
            not math.isfinite(args.capture) or not 0 < args.capture <= 60)):
        parser.error('PWM harus 0..255 dan durasi harus lebih dari 0 hingga 60 detik.')
    if args.sweep is not None and (args.capture is None or any(not 0 <= p <= 255 for p in args.sweep)):
        parser.error('--sweep memerlukan --capture dan seluruh PWM harus 0..255.')
    try:
        import serial
        from serial.tools import list_ports
    except ImportError:
        print('Pasang dependensi: python -m pip install -r requirements.txt', file=sys.stderr)
        return 1
    ports = list(list_ports.comports())
    if args.list:
        for port in ports:
            print(f'{port.device}: {port.description}')
        if not ports:
            print('Tidak ada port serial.')
        return 0

    connection = None
    log = None
    result = 0
    try:
        port = args.port or select_port(ports)
        log_path = args.log or Path(__file__).resolve().parents[1] / 'data' / (
            datetime.now().strftime('serial_%Y%m%d_%H%M%S_%f.csv'))
        log = Log(log_path)
        print(f'Log: {log_path}')
        connection = serial.Serial(baudrate=115200, timeout=0.2, write_timeout=2)
        connection.dtr = False
        connection.rts = False
        connection.port = port
        connection.open()
        # Driver masih dapat memicu reset ketika port dibuka; beri waktu boot.
        time.sleep(2)
        read_for(connection, log, 0.5)
        send_command(connection, log, '0')
        if args.capture is not None:
            for pwm in args.sweep if args.sweep is not None else [args.pwm]:
                print(f'Mulai rekam {args.capture:g} detik pada PWM {pwm}. Ctrl+C untuk berhenti.')
                log.write('EVENT', f'CAPTURE PWM={pwm} SECONDS={args.capture:g}')
                send_command(connection, log, f'PWM:{pwm}')
                send_command(connection, log, '1' if pwm > 0 else '0')
                read_for(connection, log, args.capture, require_pulses=pwm > 0)
        else:
            print('1=ON, 0=OFF, +/-=ubah setpoint, p150=PWM150, R=status, q=keluar')
            while True:
                command = input('Perintah: ').strip()
                if command.lower() == 'q':
                    break
                try:
                    normalized = normalize_command(command)
                except ValueError as error:
                    print(error)
                    continue
                send_command(connection, log, normalized)
    except (KeyboardInterrupt, EOFError):
        print('\nSesi dihentikan.')
        if log is not None:
            log.write('EVENT', 'INTERRUPTED')
    except (OSError, ValueError, RuntimeError, TimeoutError, serial.SerialException) as error:
        print(f'Gagal: {error}', file=sys.stderr)
        if log is not None:
            log.write('EVENT', f'ERROR {error}')
        result = 1
    finally:
        if connection is not None and connection.is_open:
            try:
                send_command(connection, log, '0')
                read_for(connection, log, 3)
            except (OSError, RuntimeError, TimeoutError, serial.SerialException) as error:
                print(f'OFF belum terkonfirmasi: {error}. Matikan catu motor secara manual.', file=sys.stderr)
                result = 1
            finally:
                connection.close()
        if log is not None:
            log.close()
    return result


if __name__ == '__main__':
    raise SystemExit(main())
