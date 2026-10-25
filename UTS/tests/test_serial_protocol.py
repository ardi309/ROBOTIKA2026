"""Uji protokol tanpa perangkat; bukan hasil eksperimen motor."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

source = Path(__file__).resolve().parents[1] / '02_Python_iMCLab/program/kontrol_imclab.py'
spec = importlib.util.spec_from_file_location('kontrol_imclab', source)
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


class MemoryLog:
    def __init__(self): self.rows = []
    def write(self, direction, raw): self.rows.append((direction, raw))


class SerialFake:
    def __init__(self, lines): self.lines, self.writes = list(lines), []
    def write(self, data): self.writes.append(data)
    def flush(self): pass
    def readline(self): return self.lines.pop(0) if self.lines else b''


def port(name, vid=0x10C4, pid=0xEA60, description='CP2102'):
    return SimpleNamespace(device=name, vid=vid, pid=pid, description=description, manufacturer='')


class ProtocolTests(unittest.TestCase):
    def test_command_boundaries_and_newline_injection(self):
        for invalid in ['PWM:-1', 'PWM:256', 'PWM:1.5', 'PWM:abc', '1\n0', 'ON', 'PWM:12345']:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                controller.normalize_command(invalid)
        for raw, expected in [('p0','PWM:0'), ('p255','PWM:255'), (' pwm:020 ','PWM:20'), ('r','R')]:
            self.assertEqual(controller.normalize_command(raw), expected)

    def test_only_one_identified_port_can_be_auto_selected(self):
        self.assertEqual(controller.select_port([port('COM5')]), 'COM5')
        for ports in [[], [port('COM5'), port('COM6')], [port('COM2',1,1,'Unknown')],
                      [port('COM9',description='Bluetooth CP2102')]]:
            with self.subTest(ports=ports), self.assertRaises(ValueError):
                controller.select_port(ports)

    def test_newline_and_ack_after_telemetry(self):
        ser = SerialFake([b'DATA PWM=0 SET=200 RPM=0.0 PULSES=0 DT_MS=1000\n',
                          b'ACK PWM=0 SET=120 RPM=0.0 PULSES=0 DT_MS=1000\n'])
        log = MemoryLog()
        controller.send_command(ser, log, 'p120')
        self.assertEqual(ser.writes, [b'PWM:120\n'])
        self.assertEqual(len(log.rows), 3)

    def test_device_error_and_missing_ack_are_not_success(self):
        with self.assertRaises(RuntimeError):
            controller.send_command(SerialFake([b'ERR motor locked\n']), MemoryLog(), '1')
        with self.assertRaises(TimeoutError):
            controller.send_command(SerialFake([]), MemoryLog(), '0', timeout=0.001)

    def test_rpm_sample_keeps_elapsed_time(self):
        match = controller.STATUS.fullmatch('DATA PWM=120 SET=120 RPM=1200.0 PULSES=48 DT_MS=1200')
        self.assertIsNotNone(match)
        self.assertEqual(match.groups(), ('120','120','1200.0','48','1200'))

    def test_wrong_ack_does_not_confirm_off_or_setpoint(self):
        for command, wrong, correct in [
            ('0', b'ACK PWM=200 SET=200 RPM=0.0 PULSES=0 DT_MS=1000\n',
             b'ACK PWM=0 SET=200 RPM=0.0 PULSES=0 DT_MS=1000\n'),
            ('p160', b'ACK PWM=0 SET=200 RPM=0.0 PULSES=0 DT_MS=1000\n',
             b'ACK PWM=0 SET=160 RPM=0.0 PULSES=0 DT_MS=1000\n'),
            ('R', b'ACK PWM=0 SET=200 RPM=0.0 PULSES=0 DT_MS=1000\n',
             b'STATUS PWM=0 SET=200 RPM=0.0 PULSES=0 DT_MS=1000\n')]:
            with self.subTest(command=command):
                actual = controller.send_command(SerialFake([wrong, correct]), MemoryLog(), command)
                self.assertEqual(actual, correct.decode().strip())

    def test_capture_stops_on_missing_pulses_or_telemetry(self):
        for line, expected in [(b'DATA PWM=200 SET=200 RPM=0.0 PULSES=0 DT_MS=1000\n', 'Pulsa'),
                               (b'', 'DATA')]:
            with self.subTest(expected=expected), patch.object(controller.time, 'monotonic',
                    side_effect=[0, 0, 1, 1, 2, 2, 3]), self.assertRaisesRegex(RuntimeError, expected):
                controller.read_for(SerialFake([line] * 3), MemoryLog(), 15, require_pulses=True)

    def test_motion_capture_accepts_pulses_and_off_capture_accepts_zero(self):
        for pulses, monitored in [(100, True), (0, False)]:
            line = f'DATA PWM=200 SET=200 RPM=3000.0 PULSES={pulses} DT_MS=1000\n'.encode()
            log = MemoryLog()
            with self.subTest(monitored=monitored), patch.object(controller.time, 'monotonic',
                    side_effect=[0, 0, 1, 1, 2, 2, 3, 3]):
                controller.read_for(SerialFake([line] * 3), log, 3, require_pulses=monitored)
            self.assertEqual(len(log.rows), 3)

    def test_non_finite_capture_duration_is_rejected_before_opening_port(self):
        for duration in ['nan', 'inf', '0', '61']:
            with self.subTest(duration=duration), self.assertRaises(SystemExit) as raised:
                controller.main(['--capture', duration])
            self.assertEqual(raised.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
