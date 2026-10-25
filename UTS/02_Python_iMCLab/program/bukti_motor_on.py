"""Bukti ON asli: PWM 200 selama 5 detik, kemudian OFF otomatis.

Jalankan ketika operator siap dan piringan bebas bergerak.
Guard kehilangan pulsa/telemetri menggunakan kontrol_imclab.py.
"""
from bukti_koneksi_off import run_evidence


if __name__ == '__main__':
    run_evidence(pwm=200, seconds=5)
