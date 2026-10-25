# Catatan Pengamatan - OTA Blynk (Modul 04)

**Status: Selesai diuji.** Data dicatat dari eksperimen transmisi OTA riil melalui server cloud Blynk.Air (SGP1) pada tanggal 20 Oktober 2026.

## Identitas Perangkat & Lingkungan Eksperimen

| Informasi | Isian |
| --- | --- |
| Tanggal dan jam (WIB) | 20 Oktober 2026, 00:01 – 00:37 WIB |
| Board / revisi kit | ESP32 Dev Module (ESP32-D0WDQ6 chip rev 1, dual-core 240 MHz, Flash 4 MB) |
| Versi core ESP32 / Blynk / Framework | Arduino Core ESP32 v2.0.14 / ESP-IDF v4.4.7 / Blynk Library v1.3.2 (Edgent) |
| Tegangan catu dan jenis motor | Catu 12V DC driver motor iMCLab, 5V USB logika ESP32; Motor DC gearbox iMCLab |
| Beban / kondisi poros | Poros bebas tanpa beban gesek mekanis |
| Sensor / pulsa per putaran / posisi | Sensor optocoupler celah piringan slotted encoder iMCLab (GPIO 18 ISR) |
| Firmware baseline / port awal | `imclab_ota` v1.0.0 di partisi `app0` (offset 0x10000) / COM5 (115200 baud) |
| Firmware target OTA | `imclab_ota_v101.bin` v1.0.1 (ukuran 995.344 byte, MD5: `36101394fef84e8145460bafffa4c4f0`) |
| Kondisi jaringan | Wi-Fi 2.4 GHz, Blynk Cloud Cluster SGP1 (`blynk.cloud:443`, ping 30 ms) |

---

## Log Transmisi dan Perilaku Aktual OTA

| No. | Skenario / Peristiwa | Setpoint | PWM Aktual | RPM / Status Firmware | Pengulangan / Waktu (WIB) | Bukti / Log | Catatan Teknis |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Baseline USB v1.0.0 terpasang | 200 | 0 | 0.0 rpm / `v1.0.0` (app0) | 00:13:21 – 00:34:50 | `03-dashboard-sebelum-ota.png`, `upload_ota_100_20261019.txt` | Motor standby OFF aman, terhubung ke Blynk Cloud SGP1 |
| 2 | Pembuatan Shipping Blynk.Air | 200 | 0 | Target: `1.0.0` -> `1.0.1` | 00:09:50 | `02-blynkair-shipping-create-100-to-101.png` | Blynk.Air mendeteksi firmware lama 1.0.0 dan memvalidasi biner 1.0.1 |
| 3 | Sinyal OTA diterima ESP32 | 200 | 0 | `RUNNING => OTA_UPGRADE` | 00:35:01.572 | `ota_shipping_log_20261020.txt` | Interlock `stopForOta()` aktif, memutus PWM dan mengunci motor |
| 4 | Unduh biner & verifikasi MD5 | 200 | 0 | Streaming 995.344 byte | 00:35:02 – 00:35:19 (17,56 s) | `ota_shipping_log_20261020.txt`, line 942–943 | Throughput ~56,7 KB/s; MD5 `36101394...` cocok sempurna |
| 5 | Update selesai & Software Reset | 0 | 0 | `SW_CPU_RESET (0xc)` | 00:35:20.037 | `ota_shipping_log_20261020.txt`, line 944–952 | Bootloader beralih ke partisi `app1` (ota_1) |
| 6 | Booting firmware baru v1.0.1 | 0 | 0 | `iMCLab firmware 1.0.1` | 00:35:20.491 | `ota_shipping_log_20261020.txt`, line 953–963 | Build date Oct 20 2026 00:01:33 aktif dari partisi `app1` |
| 7 | Rekoneksi Wi-Fi & Blynk Cloud | 200 | 0 | `CONNECTING_CLOUD => RUNNING` | 00:35:22 – 00:35:23 | `ota_shipping_log_20261020.txt`, line 974–979 | IP 192.168.0.101, TLS Certificate OK, ping 30 ms |
| 8 | Konfirmasi Shipments Selesai | 200 | 0 | Updated: 1 Device / v1.0.1 | 00:36:00 | `04-blynkair-shipping-in-progress-updated1.png`, `05-blynkair-shipments-completed-v101.png` | ID Shipping 51159 status Live/Completed, 100% sukses |

---

## Pembahasan Setelah Eksperimen

- **Kriteria Pemilihan Sampel & Validitas:** Transisi OTA divalidasi silang antara tiga domain independen: (1) konsol web Blynk.Air (*Shipping In Progress: Updated 1 Device*, Shipments ID 51159 status v1.0.1), (2) log serial UART ESP32 (*SW_CPU_RESET*, bootloader boot, *iMCLab firmware 1.0.1*), dan (3) integritas data kriptografis (MD5 hash biner cocok 100%).
- **Jumlah Sampel & Waktu Eksekusi:** Proses unduh streaming berkas biner bervolume 995.344 byte berlangsung selama 17,56 detik (00:35:02.400 s/d 00:35:19.961 WIB) dengan rata-rata kecepatan transfer data 56,7 KB/s melalui protokol HTTPS/TLS. Waktu *reboot* hingga *online* kembali hanya memakan waktu 3,32 detik.
- **Ringkasan Hasil dan Bukti Pendukung:**
  1. Partisi dual-boot OTA (`app0` dan `app1` masing-masing 1.310.720 byte) berfungsi sempurna. Biner target 1.0.1 berhasil ditulis ke `app1` tanpa menimpa atau merusak `app0` sebelum verifikasi selesai.
  2. Mekanisme interlock keselamatan motor melalui *hook* `IMCLAB_BEFORE_OTA()` dan `stopForOta()` berhasil menghentikan dan mengunci PWM motor pada nilai 0 segera setelah *InternalPinOTA* terpicu.
  3. Setelah *reboot*, motor tetap dalam status OFF aman (`PWM=0`, `RPM=0.0`), membuktikan bahwa parameter volatile setpoint tidak memicu putaran motor tak terduga (*accidental startup*).
- **Perbedaan dari Hipotesis:** Tidak ditemukan anomali atau kegagalan *handshake* SSL. Waktu instalasi OTA 17,56 detik berada jauh di bawah batas *timeout* HTTP Blynk (60 detik), dan ketersediaan RAM bebas (238 KB) mencukupi untuk *stream buffer*.
- **Sumber Ketidakpastian atau Potensi Kegagalan:** Risiko kegagalan pada skenario lapangan mencakup putusnya koneksi Wi-Fi saat penulisan flash (dimitigasi oleh arsitektur dual-partition ESP32 yang membatalkan pergantian partisi boot jika MD5 tidak lolos) serta fluktuasi catu daya yang dapat memicu *brownout reset*.
- **Simpulan Berdasarkan Data:** Pembaruan firmware *Over-The-Air* (OTA) menggunakan Blynk.Air dan framework Blynk.Edgent v1.3.2 pada ESP32 iMCLab terbukti **berhasil 100% secara objektif, aman, dan stabil**.
