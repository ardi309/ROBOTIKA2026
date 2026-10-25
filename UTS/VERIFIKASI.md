# Verifikasi perangkat lunak dan kit

Tanggal pemeriksaan awal: **18 Oktober 2026**. Pembaruan fisik akhir: **20 Oktober 2026**.

## Kompilasi Arduino

Lingkungan: Windows, Arduino CLI 1.3.1, ESP32 core 2.0.17, FQBN `esp32:esp32:esp32`, Blynk 1.3.2. Sketch disalin ke direktori build sementara; `secrets.h` dan `template_config.h` hanya berisi placeholder dari berkas contoh. Tidak menggunakan token/password materi dosen.

| Sketch | Hasil | Ukuran program / batas slot | RAM global |
| --- | --- | --- | --- |
| `imclab_basic` | Lulus kompilasi | 275.885 / 1.310.720 byte | 22.084 byte |
| `imclab_blynk` | Lulus kompilasi | 889.349 / 1.310.720 byte | 47.456 byte |
| `imclab_ota` | Lulus kompilasi | 985.025 / 1.310.720 byte | 51.020 byte |

---

## Python

Sembilan tes otomatis lulus dengan Python 3.12:
1. Batas PWM dan penolakan perintah tidak valid/multi-baris.
2. Penolakan pemilihan port otomatis yang ambigu.
3. Newline dan penerimaan ACK setelah baris telemetri.
4. Error perangkat atau timeout tidak dianggap sukses.
5. Parsing data mempertahankan durasi sampel aktual.
6. Sesi capture OFF pasif.
7. Penolakan durasi non-finite.
8. Kehilangan data dan penanganan timeout.
9. Validasi respons framing.

---

## Pembaruan Modul 01 - 18–19 Oktober 2026 (Pengujian Kit Berhasil)

- Kit terhubung pada port COM5 (Silicon Labs CP210x). Firmware basic diunggah dengan hash flash terverifikasi.
- Tersimpan 14 log asli dan 135 sampel DATA, termasuk hasil gagal start dan penghentian dini.
- Pengujian PWM 200 dan 160 diselesaikan selama ~15 detik. Analisis mengecualikan ACK/STATUS dan memeriksa konsistensi RPM terhadap pulsa, DT_MS, serta asumsi PPR=2.
- PDF Modul 01 terdiri dari 6 halaman utuh dan terverifikasi render PNG.

---

## Pembaruan Modul 02 - 19 Oktober 2026 (Pengujian GUI Python Berhasil)

- Python 3.12 dan pySerial 3.5 dijalankan via `.venv`. Port COM5 terdeteksi secara otomatis.
- Empat sesi pengujian selesai: OFF, pilot PWM 200, sweep 200/160/120, serta uji masukan saat OFF.
- Empat berkas CSV asli memuat 67 baris DATA.
- Dua screenshot dan satu foto fisik diverifikasi SHA256. PDF Modul 02 terdiri dari 8 halaman utuh.

---

## Pembaruan Modul 03 — 19 Oktober 2026 (Pengujian Cloud IoT Blynk Berhasil)

- Firmware `imclab_blynk` versi 1.0.0 diunggah ke COM5 (timeout SSL disetel ke 3.500 ms agar koneksi SGP1 stabil).
- Standby OFF terverifikasi, motor diam aman, dan status Online di Blynk Console.
- Pengujian slider saat OFF (160, 180, 200) membuktikan pemisahan kendali aman (PWM aktual tetap 0).
- Run aktif PWM 200 selama 63 detik (62 sampel) menghasilkan kecepatan rata-rata 9.005,7 rpm (300,2 pulsa/s).
- Sinkronisasi telemetri dua arah 1:1 terbukti presisi pada pukul 23:12:25 WIB (8.940 rpm).
- PDF Modul 03 terdiri dari 8 halaman utuh dan diverifikasi via render PNG.

---

## Pembaruan Modul 04 — 20 Oktober 2026 (Pengujian Blynk.Air OTA Berhasil)

- Datastream V4 (*Firmware Version*, String) ditambahkan pada Template `iMCLab UTS` (`TMPL6YpVE_Y1G`). Bukti: `01-setting-v4-firmware-version.png`.
- Firmware baseline `imclab_ota` v1.0.0 di-flash via USB COM5 ke partisi `app0`. Kredensial tersimpan di NVS, device Online di cluster SGP1, motor standby OFF.
- Firmware target `imclab_ota` v1.0.1 dikompilasi secara independen menjadi `imclab_ota_v101.bin` (995.344 byte, MD5 `36101394FEF84E8145460BAFFFA4C4F0`).
- Kampanye pengiriman *New Shipping* dibuat di Blynk.Air; sistem mendeteksi firmware aktif 1.0.0 dan biner target 1.0.1 (`02-blynkair-shipping-create-100-to-101.png`, `03-dashboard-sebelum-ota.png`).
- Logger serial pasif UART (`logger_ota.py`) merekam seluruh proses transmisi OTA riil (`ota_shipping_log_20261020.txt`):
  - Penerimaan URL OTA: 00:35:01 WIB.
  - Interlock `IMCLAB_BEFORE_OTA()` aktif seketika mengunci motor pada `PWM=0`.
  - Unduhan biner 995.344 byte via HTTPS selama 17,56 detik (throughput 56,68 KB/s).
  - Verifikasi MD5 cocok 100% dan penulisan flash ke partisi `app1` tuntas.
  - Software reset `SW_CPU_RESET (0xc)` memicu bootloader boot ke firmware baru: `iMCLab firmware 1.0.1 (build Oct 20 2026 00:01:33)`.
  - Rekoneksi Wi-Fi dan SSL Cloud SGP1 dalam 3,32 detik; status `RUNNING`.
  - Motor tetap dalam kondisi OFF aman pasca-reboot.
- Konsol Blynk.Air mengonfirmasi status sukses: dialog modal *Shipping In Progress* (*Updated: 1 Device*) (`04-blynkair-shipping-in-progress-updated1.png`) dan tabel riwayat *Shipments* ID 51159 status *Live / Finished* pada versi 1.0.1 (`05-blynkair-shipments-completed-v101.png`).
- Lembar pengamatan `UTS/04_OTA_Blynk/data/pengamatan.md` dan laporan riset `UTS/04_OTA_Blynk/LAPORAN.md` diperbarui lengkap.
- PDF Modul 04 diekspor ke `output/pdf/Laporan_UTS_04_OTA_Blynk.pdf` dan `UTS/04_OTA_Blynk/LAPORAN.pdf` (9 halaman, 696 KB). Seluruh 9 halaman telah dirender ke PNG dan diperiksa visual tanpa ada halaman yatim.
