# Bukti eksperimen - Python iMCLab

Uji fisik dilakukan 19 Oktober 2026 pukul 06:10-06:14 WIB melalui COM5. Bukti utama berupa CSV asli dan keluaran konsol asli yang disimpan sebagai teks; teks tersebut **bukan screenshot**.

| Bukti | Asal dan fungsi |
| --- | --- |
| [01-daftar-port.txt](01-daftar-port.txt) | Keluaran kontrol_imclab.py --list; COM5 CP210x |
| [python_off_20261019_061024.txt](python_off_20261019_061024.txt) | Konsol uji PWM 0 selama tiga detik |
| [python_pilot200_20261019_061043.txt](python_pilot200_20261019_061043.txt) | Konsol uji singkat PWM 200 |
| [python_sweep_20261019_061241.txt](python_sweep_20261019_061241.txt) | Konsol rangkaian 200 -> 160 -> 120 lalu OFF |
| [python_perintah_20261019_061413.txt](python_perintah_20261019_061413.txt) | Konsol validasi input dan perubahan target saat OFF |
| [Indeks CSV asli](../data/ringkasan_log.md) | Waktu, TX/RX, teks raw; revisi utama juga mencatat EVENT dari program |
| [Catatan operator](../data/pengamatan.md) | Konfirmasi start, putaran pelan, dan berhenti tanpa bantuan |
| [02-terminal-python-off.png](02-terminal-python-off.png) | Screenshot asli dari operator: kontrol_imclab.py, Python 3.12.14, COM5, pemeriksaan PWM 0 pada 11:28 WIB |
| [03-foto-susunan-kit.png](03-foto-susunan-kit.png) | Foto asli susunan kit; ESP32, sambungan USB, motor, piringan, sensor, dan kabel motor terlihat |
| [04-terminal-python-on200.png](04-terminal-python-on200.png) | Screenshot asli dari operator: capture PWM 200 selama lima detik pada 11:35 WIB, pulsa positif, OFF, DATA terakhir nol, kode keluar 0 |

Firmware tetap [imclab_basic.ino](../../01_Basic_iMCLab/program/imclab_basic/imclab_basic.ino) dan ImcCore.h pada folder yang sama. Tidak ada upload firmware baru untuk Modul 02.

`gambar/arsitektur.svg` adalah ilustrasi rancangan. `gambar/hasil_python.svg` adalah grafik turunan DATA asli, bukan simulasi. RPM memakai asumsi PPR=2.

- [x] Daftar port, perintah, dan balasan perangkat.
- [x] Empat CSV dan keluaran konsol asli.
- [x] Observasi operator untuk pilot dan tahap akhir rangkaian.
- [x] Screenshot terminal Python yang memperlihatkan program dan port dengan jelas, pada uji OFF.
- [x] Screenshot terminal Python saat PWM 200, pembacaan pulsa positif, dan kondisi akhir OFF.
- [x] Foto susunan kit dan sambungan dari operator; tidak dipakai untuk menentukan status putaran.

Foto identifikasi dan screenshot Arduino Modul 01 tidak diklaim diambil saat sesi Python. Bukti layar OFF, ON, dan foto susunan kit sudah tersedia. [Panduan](../PANDUAN_UJI.md) menjelaskan cara mengulang dokumentasi bila diperlukan; tidak perlu mengulang tes hanya untuk melengkapi bukti yang sudah ada.

## Pemeriksaan tambahan untuk dokumentasi layar

Pada 19 Oktober 2026 pukul 11:24 WIB, [bukti_koneksi_off.py](../program/bukti_koneksi_off.py) menjalankan program kontrol asli dengan argumen `--port COM5 --capture 3 --pwm 0`. Keluaran aktual disimpan di [konsol teks tambahan](bukti_off_20261019_112450.txt) dan [CSV tambahan](../data/bukti_off_20261019_112450.csv). Seluruh PWM yang dilaporkan 0 dan tidak ada perintah ON. Beberapa DATA mencatat pulsa kecil saat PWM=0; angka tetap dipertahankan tanpa diagnosis penyebab.

Sesi tambahan ini terpisah dari empat sesi utama yang dipakai dalam grafik dan perbandingan laporan. Screenshot belum dihasilkan dari sesi ini karena konsol tidak bertahan sebagai jendela yang dapat ditangkap. Jalankan berkas bukti tersebut di PowerShell yang dibuka pengguna; setelah selesai, jendela menunggu Enter agar dapat diambil screenshot asli.

Operator kemudian menjalankan ulang pemeriksaan pada **11:28:27 WIB** dan mengirim screenshot. CSV [bukti_off_20261019_112827.csv](../data/bukti_off_20261019_112827.csv) dan [konsol teks](bukti_off_20261019_112827.txt) menyimpan hasil sesi yang terlihat pada gambar. Seluruh PWM dan RPM pada DATA sesi ini bernilai 0.

Pada **11:33:48 WIB**, percobaan [bukti_motor_on.py](../program/bukti_motor_on.py) gagal membuka COM5 dengan Access is denied. [CSV gagal](../data/bukti_on200_20261019_113348.csv) hanya berisi EVENT ERROR, tanpa TX atau RX; [konsol gagal](bukti_on200_20261019_113348.txt) dipertahankan. Pemilik port saat itu tidak teridentifikasi, dan percobaan ini tidak dihitung sebagai uji motor.

Pengulangan pada **11:35:27 WIB** berhasil dan screenshot dikirim operator. [CSV ON](../data/bukti_on200_20261019_113527.csv) serta [konsol ON](bukti_on200_20261019_113527.txt) mencatat 11 DATA, lima di antaranya aktif pada PWM 200 dengan pulsa 69, 203, 250, 258, dan 268 per 1000 ms. Jarak TX ON-OFF 5,198 detik. Setelah ACK OFF, DATA berisi 285, 3, lalu 0 pulsa; PWM akhir 0 dan kode keluar program 0. Sesi ini merupakan bukti tambahan, bukan data kestabilan untuk grafik utama.

Ketiga PNG merupakan salinan utuh lampiran operator, tanpa pengubahan gambar maupun teks. Hash SHA256 salinan cocok dengan sumber:

```text
02-terminal-python-off.png
4DE76D31BA261F5CEA98EEF3B37D62A5BB7792788904EDD64CF0E91BD8642B72
03-foto-susunan-kit.png
446085F828F44F61035CBA62DF1062E966D06F1A01286633D337BFC55AEC4245
04-terminal-python-on200.png
0A6C6A8B1A9765B1B66769763C3AA72D687FE6D2AC14A953483A7D72928ADBE2
```
