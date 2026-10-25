# Indeks data asli Modul 02

Dibuat oleh `UTS/tools/analisis_python.py`. Berkas python_*.csv adalah log asli; sampel_serial.csv hanya turunan baris DATA.

| Log | DATA | DATA dengan PWM > 0 | Durasi TX ON-OFF (s) |
| --- | --- | --- | --- |
| [python_off_20261019_061024.csv](python_off_20261019_061024.csv) | 5 | 0 | - |
| [python_perintah_20261019_061413.csv](python_perintah_20261019_061413.csv) | 6 | 0 | - |
| [python_pilot200_20261019_061043.csv](python_pilot200_20261019_061043.csv) | 5 | 2 | 2.194046 |
| [python_sweep_20261019_061241.csv](python_sweep_20261019_061241.csv) | 51 | 45 | 45.392255 |

Durasi berasal dari waktu komputer; bukan pengukuran langsung lama gerak mekanis. ACK/STATUS tidak dihitung sebagai sampel baru.
Dua baris DATA pada uji OFF pertama berisi satu pulsa. Angka dipertahankan; penyebab belum diketahui.
