# Mulai tes kit iMCLab

Urutan pengerjaan: **Basic -> Python -> Blynk -> OTA**. File `.h` seperti `ResetButton.h` adalah pendukung sketch. Untuk langkah pertama, buka `imclab_basic.ino` di Arduino IDE.

## 1. Tes motor dasar melalui USB

Untuk sesi manual pada kit yang sudah terpasang di COM5, ikuti [panduan uji manual Modul 01](01_Basic_iMCLab/PANDUAN_UJI_MANUAL.md). Panduan itu memuat pemeriksaan singkat, batas durasi saat motor diam, dan format hasil untuk laporan. Karena sesi sebelumnya menunjukkan gerakan yang belum konsisten, gunakan pemeriksaan awal pada panduan tersebut sebelum tes panjang.

1. Sambungkan kit memakai kabel USB data. Sediakan catu motor sesuai kit dan pastikan poros/roda bebas bergerak.
2. Di Arduino IDE buka [imclab_basic.ino](01_Basic_iMCLab/program/imclab_basic/imclab_basic.ino). Biarkan `ImcCore.h` di folder yang sama.
3. Pasang paket board **esp32 by Espressif Systems 2.0.17**. Jika paket belum muncul, masukkan `https://espressif.github.io/arduino-esp32/package_esp32_index.json` di Additional Boards Manager URLs pada Preferences, lalu cari paket di Boards Manager. Modul basic tidak memerlukan library Blynk.
4. Pilih **ESP32 Dev Module** untuk ESP32 klasik yang sesuai kit dan port COM yang muncul setelah USB tersambung. Klik **Verify**, lalu **Upload**.
5. Buka **Serial Monitor**, pilih **115200 baud**, dan **Newline**.
6. Kirim perintah pada tabel **satu per satu**, tekan Enter setelah setiap perintah.

| Perintah | Yang diperiksa |
| --- | --- |
| `0` | Keluaran motor OFF |
| `PWM:120` | Setpoint berubah ke 120; keluaran tetap OFF |
| `1` | Keluaran PWM aktif; amati apakah motor berputar |
| `R` | Lihat PWM, setpoint, RPM, jumlah pulsa, dan durasi sampel terakhir |
| `+` | Setpoint naik menjadi 130 |
| `-` | Setpoint turun kembali ke 120 |
| `0` | Keluaran OFF; tunggu poros berhenti |

Balasan `ACK` menunjukkan perintah diproses. Baris `DATA` muncul kira-kira tiap satu detik. Nilai RPM bergantung sensor dan kondisi motor; jangan mengharapkan angka tertentu dari contoh ini. Jika PWM aktif tetapi poros diam, periksa catu/driver/beban sebelum meningkatkan PWM.

Ambil foto kit dan screenshot Serial Monitor. Simpan di `01_Basic_iMCLab/bukti/`, lalu catat pengamatan di [lembar Modul 01](01_Basic_iMCLab/data/pengamatan.md).

## 2. Tes Python dengan firmware yang sama

Pengujian awal sudah selesai. Lihat [panduan Modul 02](02_Python_iMCLab/PANDUAN_UJI.md) untuk pengulangan dan screenshot. `.venv` serta pySerial sudah tersedia pada komputer ini; langkah pembuatan venv/instalasi berikut hanya diperlukan pada komputer baru. Tutup Serial Monitor dan buka PowerShell pada root `D:\ryudev_area\robotika`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r UTS/02_Python_iMCLab/program/requirements.txt
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --list
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --port COM5
```

Ganti `COM5` dengan port yang muncul pada komputer. Untuk memeriksa perintah saat OFF, ketik `p200`, `R`, `0`, lalu `q`, satu per satu. Log asli otomatis tersimpan di `02_Python_iMCLab/data/`.

Untuk pilot dua detik saat kit dan operator siap, gunakan perintah berikut. **Perintah ini menyalakan motor**, kemudian mencoba mematikannya saat selesai:

```powershell
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --port COM5 --capture 2 --pwm 200
```

Jika koneksi serial terlepas, OFF tidak dapat dijamin terkirim; hentikan catu motor secara manual.

## 3. Blynk dan OTA

Setelah dua modul pertama berhasil, ikuti [panduan lengkap](PANDUAN_PRAKTIK.md):

- **Blynk:** isi `secrets.h`, buat V0-V3, upload sketch Blynk, lalu uji slider dan switch.
- **OTA:** isi `template_config.h`, upload firmware 1.0.0 lewat USB, lakukan provisioning, lalu kirim firmware 1.0.1 melalui Blynk.Air. Bukti keberhasilan adalah versi baru yang terbaca setelah perangkat reconnect.

## Laporan PDF

| Modul | PDF |
| --- | --- |
| Basic | [Laporan Modul 01](01_Basic_iMCLab/LAPORAN.pdf) |
| Python | [Laporan Modul 02](02_Python_iMCLab/LAPORAN.pdf) |
| Blynk | [Laporan Modul 03](03_Blynk_iMCLab/LAPORAN.pdf) |
| OTA | [Laporan Modul 04](04_OTA_Blynk/LAPORAN.pdf) |

PDF Modul 01-02 sudah berisi **hasil uji awal**, termasuk perbedaan hasil antar sesi dan batas kalibrasi sensor. Modul 03-04 masih **draf**. Tambahkan identitas, foto susunan praktik, dan hasil baru pada sumber Markdown, kemudian ekspor ulang. Cara ekspor ada di [tools/README.md](tools/README.md).

Rujukan cara upload dan pemilihan board/port: [Arduino Help Center](https://support.arduino.cc/hc/en-us/articles/4733418441116-Upload-a-sketch-in-Arduino-IDE). Pilihan pin serta protokol perintah mengikuti program paket UTS ini.
