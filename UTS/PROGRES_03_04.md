# Log progres Modul 03 dan Modul 04 (Lengkap & Selesai)

Pembaruan: **20 Oktober 2026, WIB**. Catatan rekayasa dan pengujian riil. Konteks dan instruksi lengkap: [HANDOFF_GEMINI.md](../HANDOFF_GEMINI.md).

## Status Pekerjaan

**Modul 01, 02, 03, dan 04 SELESAI PENUH (100%).**
Seluruh rangkaian eksperimen fisik pada kit iMCLab ESP32 telah terlaksana, data telemetri empiris dan log serial UART tercatat, seluruh tangkapan layar bukti otentik tersimpan, laporan riset akademik markdown lengkap, dan dokumen PDF formal telah diekspor serta diverifikasi secara visual melalui render PNG per halaman tanpa halaman yatim. Identitas mahasiswa (Nama, NIM, Kelas) tetap dibiarkan kosong sesuai instruksi.

---

## Riwayat Pekerjaan Modul 03 (Selesai — 19 Oktober 2026)

- [x] Template, datastream, dashboard dan actual device dibuat/disimpan di Blynk Console.
- [x] Konfigurasi lokal terisi; kompilasi berhasil.
- [x] Empat screenshot setting dan log kompilasi tersimpan.
- [x] Sambungkan USB; port COM5 terdeteksi CP210x.
- [x] Penyesuaian timeout koneksi SSL Blynk (3.500 ms) agar handshake `blynk.cloud` SGP1 tuntas.
- [x] Upload `imclab_blynk` ke ESP32 pada COM5; log upload tersimpan ([upload_blynk_20261019.txt](03_Blynk_iMCLab/bukti/upload_blynk_20261019.txt)).
- [x] Verifikasi startup OFF aman, Wi-Fi terhubung, device Online (`Ready (ping: 31ms)`).
- [x] Script logger serial pasif read-only ([logger_blynk.py](03_Blynk_iMCLab/program/logger_blynk.py)) dibuat.
- [x] Pengujian slider saat switch OFF: setpoint 160/180/200 tidak memicu motor berputar ([07-dashboard-blynk-slider-off160.png](03_Blynk_iMCLab/bukti/07-dashboard-blynk-slider-off160.png)).
- [x] Pilot run PWM 200 (6 s, max 8.280 rpm) dan run aktif kontinu 63 detik (62 data aktif, 58 data stabil rata-rata 9.005,7 rpm).
- [x] Dashboard ON PWM 200 ([08-dashboard-blynk-on200.png](03_Blynk_iMCLab/bukti/08-dashboard-blynk-on200.png)) dan terminal IDE ([09-terminal-ide-telemetri-on200.png](03_Blynk_iMCLab/bukti/09-terminal-ide-telemetri-on200.png)) sinkron 1:1 pada 8.940 rpm (23:12:25 WIB).
- [x] Deselerasi terukur saat switch OFF: 8.430 -> 960 -> 0 rpm dalam 2 detik.
- [x] Raw log tersimpan di [serial_blynk_20261019_230428.log](03_Blynk_iMCLab/data/serial_blynk_20261019_230428.log) dan lembar pengamatan di [pengamatan.md](03_Blynk_iMCLab/data/pengamatan.md).
- [x] Laporan [LAPORAN.md](03_Blynk_iMCLab/LAPORAN.md) diperbarui lengkap dan PDF 8 halaman diekspor serta diverifikasi render PNG.

---

## Riwayat Pekerjaan Modul 04 (Selesai — 20 Oktober 2026)

- [x] **Pemeriksaan Akses & Alur Blynk.Air:** Akun organisasi `8335PV` (SGP1) memiliki fitur Blynk.Air aktif dan kuota pengiriman tersedia.
- [x] **Konfigurasi Datastream Versi:** Menambahkan Datastream Virtual Pin V4 (`Firmware Version`, tipe String, default `1.0.0`) pada Template `iMCLab UTS` (`TMPL6YpVE_Y1G`). Bukti tersimpan di [01-setting-v4-firmware-version.png](04_OTA_Blynk/bukti/01-setting-v4-firmware-version.png).
- [x] **Pengamanan Interlock Firmware:** Mengimplementasikan hook `IMCLAB_BEFORE_OTA()` dan `stopForOta()` pada `imclab_ota.ino` untuk memutus PWM dan mengunci motor saat sinyal OTA diterima.
- [x] **Kompilasi & Upload Baseline 1.0.0 via USB:** Mengompilasi dan mengunggah firmware versi baseline 1.0.0 ke ESP32 pada port COM5 (partisi `app0`). Log upload: [upload_ota_100_20261019.txt](04_OTA_Blynk/bukti/upload_ota_100_20261019.txt).
- [x] **Kompilasi Biner Target 1.0.1 (Tanpa USB):** Mengompilasi firmware versi 1.0.1 secara terpisah ke `imclab_ota_v101.bin` (ukuran 995.344 byte, MD5 `36101394FEF84E8145460BAFFFA4C4F0`, SHA-256 `C22D8816C8997C08BF16FDBF018682889E4132EBEF1AE239FDF5B83EE0E1FCF4`).
- [x] **Inisiasi Shipping Blynk.Air:** Pengguna membuat kampanye pengiriman *New Shipping* di Blynk.Console, mengunggah `imclab_ota_v101.bin`, dan menargetkan perangkat `iMCLab Modul 03`. Halaman shipping mendeteksi firmware aktif 1.0.0 dan target baru 1.0.1. Bukti: [02-blynkair-shipping-create-100-to-101.png](04_OTA_Blynk/bukti/02-blynkair-shipping-create-100-to-101.png) dan dashboard sebelum OTA di [03-dashboard-sebelum-ota.png](04_OTA_Blynk/bukti/03-dashboard-sebelum-ota.png).
- [x] **Perekaman Telemetri Serial Real-time:** Menjalankan script pasif `logger_ota.py` pada COM5. Merekam proses transisi OTA: penerimaan URL, validasi MD5 header, proses unduh biner selama 17,56 detik (throughput 56,68 KB/s), penyelesaian flash, software reset CPU `SW_CPU_RESET (0xc)`, eksekusi partisi `app1`, dan booting firmware `iMCLab firmware 1.0.1`. Log lengkap tersanitasi: [ota_shipping_log_20261020.txt](04_OTA_Blynk/bukti/ota_shipping_log_20261020.txt).
- [x] **Verifikasi Keberhasilan Pengiriman:** Dialog *Shipping In Progress* menampilkan status hijau penuh (*Target: 1 Device, Updated: 1 Device*) ([04-blynkair-shipping-in-progress-updated1.png](04_OTA_Blynk/bukti/04-blynkair-shipping-in-progress-updated1.png)) dan tabel *Shipments* ID 51159 status *Live / Finished* pada versi 1.0.1 ([05-blynkair-shipments-completed-v101.png](04_OTA_Blynk/bukti/05-blynkair-shipments-completed-v101.png)).
- [x] **Verifikasi Motor Pasca-Reboot:** Motor terkonfirmasi tetap diam aman (`PWM=0`, `RPM=0.0`) tanpa ada perputaran tak terduga.
- [x] **Penyusunan Lembar Pengamatan & Laporan:** Lembar pengamatan [pengamatan.md](04_OTA_Blynk/data/pengamatan.md) dan laporan [LAPORAN.md](04_OTA_Blynk/LAPORAN.md) diperbarui secara komprehensif.
- [x] **Ekspor PDF & Verifikasi Visual:** Dokumen [LAPORAN.pdf](04_OTA_Blynk/LAPORAN.pdf) (9 halaman, 696 KB) berhasil dikompilasi via `buat_pdf.py` dan seluruh 9 halaman tervalidasi sempurna melalui render PNG resolusi tinggi di `tmp/pdfs/04/`.

---

## Ringkasan Berkas Bukti & Laporan

| Modul | Laporan Markdown | Laporan PDF | Status Pengujian | Jumlah Bukti Riil |
| --- | --- | --- | --- | --- |
| 01 - Basic | `01_Basic_iMCLab/LAPORAN.md` | `01_Basic_iMCLab/LAPORAN.pdf` (6 hal) | Selesai (Baseline) | Data serial riil |
| 02 - Python | `02_Python_iMCLab/LAPORAN.md` | `02_Python_iMCLab/LAPORAN.pdf` (8 hal) | Selesai (Serial GUI) | Data CSV & foto |
| 03 - Blynk | `03_Blynk_iMCLab/LAPORAN.md` | `03_Blynk_iMCLab/LAPORAN.pdf` (8 hal) | Selesai (Cloud IoT) | 4 screenshot + log |
| 04 - OTA | `04_OTA_Blynk/LAPORAN.md` | `04_OTA_Blynk/LAPORAN.pdf` (9 hal) | Selesai (Blynk.Air OTA) | 5 screenshot + 2 log |
