"""Tampilkan uji Python asli untuk dokumentasi layar.

Entry point berkas ini tetap OFF; bukti_motor_on.py memilih uji ON singkat.
CSV dan salinan keluaran konsol disimpan sebagai bukti tambahan.
"""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
import sys

import kontrol_imclab


class ConsoleCopy:
    def __init__(self, screen, log):
        self.screen, self.log = screen, log

    def write(self, text):
        self.screen.write(text)
        self.log.write(text)
        self.log.flush()
        return len(text)

    def flush(self):
        self.screen.flush()
        self.log.flush()


def run_evidence(pwm: int = 0, seconds: int = 3):
    module = Path(__file__).resolve().parents[1]
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    label = 'off' if pwm == 0 else f'on{pwm}'
    csv_path = module / 'data' / f'bukti_{label}_{stamp}.csv'
    text_path = module / 'bukti' / f'bukti_{label}_{stamp}.txt'
    original_out, original_err = sys.stdout, sys.stderr
    with text_path.open('x', encoding='utf-8') as output:
        sys.stdout = ConsoleCopy(original_out, output)
        sys.stderr = ConsoleCopy(original_err, output)
        try:
            print('UTS MODUL 02 - PYTHON iMCLab')
            print('Bukti tambahan: ' + ('koneksi USB serial saat motor OFF' if pwm == 0
                                         else f'motor ON PWM {pwm} selama {seconds} detik, lalu OFF'))
            print('Waktu:', datetime.now().astimezone().isoformat(timespec='seconds'))
            print('Program:', Path(kontrol_imclab.__file__).resolve())
            print('Python:', sys.version.split()[0])
            print(f'Argumen: --port COM5 --capture {seconds} --pwm {pwm}')
            print()
            kontrol_imclab.main(['--list'])
            result = kontrol_imclab.main(['--port', 'COM5', '--capture', str(seconds),
                                         '--pwm', str(pwm), '--log', str(csv_path)])
            print()
            print('Kode keluar program:', result)
            if result == 0:
                with csv_path.open(encoding='utf-8', newline='') as source:
                    rows = list(csv.DictReader(source))
                ack = [r for r in rows if r['direction'] == 'RX' and r['raw'].startswith('ACK ')]
                active = [r for r in rows if r['direction'] == 'RX' and
                          r['raw'].startswith('DATA ') and int(r['pwm']) > 0]
                if active:
                    print('DATA aktif:', len(active), '| Rentang RPM estimasi:',
                          min(float(r['rpm']) for r in active), '-', max(float(r['rpm']) for r in active))
                if ack and ack[-1]['pwm'] == '0':
                    print('Balasan akhir: OFF terkonfirmasi (PWM=0).')
            print('Salinan konsol:', text_path.name)
            print('CSV tambahan:', csv_path.name)
        finally:
            sys.stdout, sys.stderr = original_out, original_err
    try:
        input('\nSelesai. Jendela ini siap difoto/screenshot. Enter untuk kembali. ')
    except EOFError:
        pass


def main():
    run_evidence(pwm=0, seconds=3)


if __name__ == '__main__':
    main()
