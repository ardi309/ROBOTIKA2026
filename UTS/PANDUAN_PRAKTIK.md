# Panduan praktik UTS

## Peralatan dan lingkungan

- Kit iMCLab dengan ESP32 klasik, motor DC, driver motor, dan sensor pulsa; cocokkan dengan revisi kit.
- Kabel USB data dan catu daya motor sesuai spesifikasi kit.
- Arduino IDE; konfigurasi acuan: **ESP32 by Espressif Systems 2.0.17**, board **ESP32 Dev Module**, library **Blynk 1.3.2**.
- Python 3.10 atau lebih baru; dependensi Modul 02 adalah `pyserial==3.5`.
- Wi-Fi 2,4 GHz dan akun Blynk untuk Modul 03/04. Periksa bahwa akun menyediakan akses Blynk.Air sebelum menjadwalkan demo OTA.

Versi di atas adalah baseline yang dipatok untuk paket ini, bukan pernyataan versi terbaru. Bagian motor memiliki cabang API LEDC untuk core 2.x/3.x, tetapi dependensi Edgent dipatok ke v1.3.2; hasil verifikasi yang benar-benar dijalankan dicatat terpisah di `VERIFIKASI.md`.

## Sambungan sesuai kode kelas

| Fungsi | GPIO ESP32 | Catatan |
| --- | --- | --- |
| LED | 2 | Indikasi keluaran PWM aktif |
| Driver IN1 | 27 | HIGH untuk arah percobaan |
| Driver IN2 | 26 | LOW untuk arah percobaan |
| Driver enable/PWM | 12 | 30 kHz, resolusi 8 bit |
| Sensor pulsa RPM | 13 | INPUT_PULLUP, interrupt FALLING |

Tabel ini adalah pemetaan perangkat lunak dari kode dosen, bukan skema listrik lengkap. Pastikan label terminal, ground bersama, catu driver, serta level sinyal sensor cocok dengan kit. Motor disuplai melalui driver, bukan langsung dari GPIO. Saat menguji, bebaskan poros/roda dari benda yang dapat tersangkut. Mematikan PWM tidak berarti poros langsung berhenti karena inersia.

`PULSES_PER_REV = 2` mengikuti `HOLES = 2` di materi. Putar poros satu putaran dan cek pulsa untuk mengonfirmasinya. Jika encoder berada sebelum gearbox, hasil RPM mewakili poros encoder; konversi ke poros keluaran memerlukan rasio gearbox yang benar.

## Modul 01: upload dan kontrol dasar

1. Buka `01_Basic_iMCLab/program/imclab_basic/imclab_basic.ino` bersama `ImcCore.h` dalam folder yang sama.
2. Pilih board dan port kit, kemudian Verify dan Upload melalui USB.
3. Buka Serial Monitor pada **115200 baud** dan pilih **Newline** atau **Both NL & CR**.
4. Kirim `0`, `PWM:120`, `1`, `R`, `+`, `-`, lalu `0`.
5. Ambil foto rangkaian dan tangkapan keluaran serial. Lakukan ulang pada nilai PWM sesuai tabel pengamatan.

### Arti perintah paket UTS

| Perintah | Perilaku |
| --- | --- |
| `1` | Mengaktifkan motor pada setpoint terakhir; setpoint 0 diganti 200 |
| `0` | Mematikan keluaran, mempertahankan setpoint |
| `PWM:120` | Mengubah setpoint menjadi 120; hanya berputar jika status ON |
| `+` / `-` | Mengubah setpoint 10, dibatasi 0..255; tidak mengaktifkan status OFF |
| `R` | Membaca status sampel RPM terakhir |

Pemisahan setpoint dan ON/OFF ini merupakan pengembangan dari kode dosen: slider atau pengubahan PWM saat OFF tidak otomatis menyalakan motor. `PWM:abc`, nilai negatif, atau nilai di atas 255 ditolak, tanpa mengubah setpoint.

Contoh **format** balasan (bukan hasil pengukuran):

```text
DATA PWM=<keluaran> SET=<setpoint> RPM=<nilai> PULSES=<jumlah> DT_MS=<durasi>
```

`ACK` berarti perintah diproses, bukan jaminan poros bergerak. `RPM` dihitung dari sensor; LED hanya menunjukkan keluaran PWM. Satu sampel `DATA` dihasilkan kira-kira tiap satu detik.

## Modul 02: Python

Hasil uji pertama sudah tersedia. [Panduan Modul 02](02_Python_iMCLab/PANDUAN_UJI.md) memuat tes OFF, pilot dua detik, dan variasi otomatis. `.venv` serta pySerial 3.5 sudah terpasang pada komputer ini; pembuatan venv dan instalasi berikut hanya untuk komputer baru.

Tutup Serial Monitor agar port tidak dipakai bersamaan. Dari root repositori jalankan:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r UTS/02_Python_iMCLab/program/requirements.txt
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --list
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --port COM5
```

Ganti COM5 dengan port kit. Penggunaan `--port` menghindari salah pilih jika beberapa adaptor USB tersambung. Tanpa argumen ini, program hanya menerima satu kandidat yang dikenali.

Setelah pilot dua detik berhasil dan operator siap, rekam tiga tahap PWM, masing-masing sekitar 15 detik (**perintah ini menyalakan motor**):

```powershell
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --port COM5 --capture 15 --sweep 200 160 120
```

Log otomatis masuk ke folder `02_Python_iMCLab/data/`. Capture dengan PWM > 0 dihentikan jika DATA atau pulsa hilang selama tiga detik; durasi dibatasi 60 detik per tahap. Mode interaktif membaca balasan setelah perintah dan dapat menumpuk data saat menunggu input; guard tersebut tidak aktif saat menunggu input. Saat keluar, program mengirim OFF, menunggu konfirmasi, dan membaca DATA tiga detik tambahan. Jika kabel terlepas, OFF mungkin tidak terkirim; matikan catu motor secara manual. Firmware basic tidak memiliki watchdog komunikasi.

## Modul 03: Blynk

1. Buat template ESP32/Wi-Fi dan sebuah device milik sendiri.
2. Atur datastream pada tabel berikut. Hubungkan widget dashboard web/mobile ke pin yang sama.
3. Salin `secrets.example.h` menjadi `secrets.h` di folder `imclab_blynk`. Isi Template ID, nama, token device, SSID, dan password sendiri.
4. Upload sketch; tunggu device online. Atur slider, lalu tombol ON. Catat PWM aktual dan RPM. Matikan lagi.
5. Uji putus koneksi secara terkontrol dan catat waktu sampai motor OFF. Pemutusan cloud tidak selalu langsung terdeteksi; mekanisme ini bukan emergency stop waktu nyata.

| Pin virtual | Nama | Tipe / rentang konfigurasi awal | Widget |
| --- | --- | --- | --- |
| V0 | RPM | Double, 0..10000, unit rpm | Value/gauge/chart |
| V1 | PWM aktual | Integer, 0..255 | Value |
| V2 | Setpoint PWM | Integer, 0..255 | Slider |
| V3 | Motor enable | Integer, 0..1 | Switch |
| V4 | Versi firmware | String, khusus Modul 04 | Value/label |

Rentang gauge RPM 0..10000 hanya konfigurasi tampilan awal; sesuaikan dengan spesifikasi motor dan hasil kalibrasi, bukan target putaran. Pada reconnect, firmware mengirim setpoint lokal dan status OFF. Pengguna perlu menekan ON lagi.

## Modul 04: OTA melalui Blynk.Air

1. Salin `template_config.example.h` menjadi `template_config.h` di `04_OTA_Blynk/program/imclab_ota/`, isi template milik sendiri. Jangan menambahkan `BLYNK_AUTH_TOKEN`: Edgent mengelolanya melalui provisioning.
2. Pilih partisi dengan **dua slot aplikasi OTA** dan kapasitas yang cukup. Hindari pilihan berlabel No OTA. Untuk board ESP32 4 MB, pilih partisi OTA yang tersedia dan cek ukuran binary hasil kompilasi.
3. Upload versi `1.0.0` lewat USB. Gunakan alur Add New Device/provisioning di aplikasi Blynk untuk memasukkan Wi-Fi dan mengaitkan device ke template.
4. Pastikan V4/Serial menunjukkan `1.0.0`. Rekam buktinya. Uji dashboard dan matikan motor.
5. Ubah `BLYNK_FIRMWARE_VERSION` menjadi `1.0.1`. **Export Compiled Binary**, tanpa melakukan Upload USB untuk versi ini.
6. Di Blynk.Air buat shipping, pilih template dan **device uji tertentu**, unggah binary aplikasi `.ino.bin`. Jangan pilih bootloader, partitions, atau merged binary. Periksa target sebelum menjalankan shipping.
7. Tunggu pembaruan dan reboot, kemudian buktikan device online dengan V4/Serial `1.0.1`. Rekam status shipping dan uji ON/OFF lagi.

Ini menggunakan [alur Blynk.Air](https://docs.blynk.io/en/blynk.edgent/updating-devices-firmwares-ota) dan [provisioning Edgent](https://docs.blynk.io/en/getting-started/activating-devices/blynk-edgent-wifi-provisioning). Jika Blynk.Air belum tersedia di akun, catat kendalanya: OTA belum dapat dinyatakan berhasil.

## Menghitung RPM dan membahas hasil

```text
Duty (%) = PWM / 255 * 100
RPM = jumlah_pulsa * 60000 / (pulsa_per_putaran * durasi_ms)
```

Contoh hitung teori: 40 pulsa dalam 1000 ms dengan 2 pulsa/putaran menghasilkan 1200 rpm. Pada 40 pulsa dalam 1200 ms hasilnya 1000 rpm. Angka tersebut bukan pengukuran kit. Resolusi hitungan untuk jendela 1 detik dan 2 pulsa/putaran adalah 30 rpm per pulsa.

Untuk perbandingan PWM, pertahankan catu, beban, posisi sensor, dan durasi uji. Abaikan sampel transisi awal ketika menganalisis putaran stabil; nyatakan kriteria stabil yang dipakai. Laporkan jumlah sampel, rata-rata, minimum, dan maksimum dari data asli. Jangan menganggap hubungan PWM dan RPM selalu linear.

## Masalah umum

| Gejala | Pemeriksaan |
| --- | --- |
| Port tidak muncul | Kabel data, driver USB-UART, port USB |
| Port sedang dipakai | Tutup Serial Monitor/notebook lain |
| Perintah tidak dibalas | Baud 115200, newline, firmware Modul 01 |
| LED menyala tetapi motor diam | Catu driver, kabel motor, beban, PWM terlalu rendah |
| RPM nol saat motor berputar | Pin 13, sensor, tepi pulsa, ground, PULSES_PER_REV |
| RPM terlalu besar/kecil | Pulsa/putaran, debounce, noise, posisi encoder/gearbox |
| `ledcSetup` tidak dikenali pada materi asli | Core 3.x mengubah API LEDC; gunakan baseline atau header paket UTS |
| Blynk offline | Template/token, Wi-Fi, internet, konfigurasi device |
| OTA tidak masuk / gagal | Versi berubah, device target, slot OTA, ukuran binary, koneksi |

Perubahan LEDC dirujuk dari [panduan migrasi resmi Espressif](https://docs.espressif.com/projects/arduino-esp32/en/latest/migration_guides/2.x_to_3.0.html).
