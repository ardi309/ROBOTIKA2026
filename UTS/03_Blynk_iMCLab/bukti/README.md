# Bukti konfigurasi dan eksperimen Blynk iMCLab

Pembaruan **19 Oktober 2026**. Konfigurasi cloud dan kompilasi selesai; **belum ada hasil upload, koneksi kit atau uji motor Modul 03**. Lihat [progres 03–04](../../PROGRES_03_04.md).

| Berkas | Isi / asal | Batas penggunaan |
| --- | --- | --- |
| [02-setting-switch-v3.jpg](02-setting-switch-v3.jpg) | Screenshot modal Switch Settings: Motor ON/OFF, V3, ON=1, OFF=0. | Konfigurasi, bukan motor berputar. |
| [03-setting-slider-v2.jpg](03-setting-slider-v2.jpg) | Screenshot Slider Settings: V2, send on release, fine step 10. | Preview bukan telemetri. |
| [04-setting-rpm-v0.jpg](04-setting-rpm-v0.jpg) | Screenshot Label Settings: RPM estimasi, V0, rata tengah. | Bukan pengukuran sensor. |
| [05-setting-pwm-v1.jpg](05-setting-pwm-v1.jpg) | Screenshot Label Settings: PWM aktual, V1, rata tengah. | Bukan bukti keluaran motor. |
| [compile_blynk_20261019.txt](compile_blynk_20261019.txt) | Kompilasi awal gagal ekstraksi VCRUNTIME140.dll karena izin runtime. | Kegagalan lingkungan dipertahankan. |
| [compile_blynk_20261019_host.txt](compile_blynk_20261019_host.txt) | Kompilasi host berhasil, exit 0. | Bukan bukti upload atau koneksi. |

| [upload_blynk_20261019.txt](upload_blynk_20261019.txt) | Log upload firmware imclab_blynk ke ESP32 pada COM5 (exit 0). | Bukti upload flash. |
| [06-dashboard-blynk-off.png](06-dashboard-blynk-off.png) | Screenshot dashboard actual device iMCLab Modul 03 Online, switch OFF, Setpoint 200, PWM aktual 0, RPM 0. | Bukti startup aman dan koneksi cloud. |
| [07-dashboard-blynk-slider-off160.png](07-dashboard-blynk-slider-off160.png) | Screenshot dashboard actual device saat slider digeser ke 160 dalam kondisi switch OFF; PWM aktual tetap 0, RPM 0. | Bukti pemisahan setpoint dan status ON. |
| [08-dashboard-blynk-on200.png](08-dashboard-blynk-on200.png) | Screenshot dashboard actual device saat switch ON, Setpoint 200, PWM aktual 200, RPM estimasi 8.940 rpm. | Bukti aktuasi cloud dan umpan balik sensor aktif. |
| [09-terminal-ide-telemetri-on200.png](09-terminal-ide-telemetri-on200.png) | Screenshot IDE Antigravity dengan sketch aktif dan terminal logger serial pasif yang mencatat DATA telemetri riil (sinkron pada RPM 8.940). | Bukti integritas telemetri hardware-cloud. |

Keempat JPEG setting awal dan empat PNG hasil pengujian disimpan tanpa rekayasa dari lingkungan kerja operator. Nilai telemetri pada dashboard terbukti sinkron 1:1 dengan sampel baris serial pada detik yang sama (23:12:25 WIB).

## Status bukti

- [x] Upload sketch imclab_blynk terverifikasi pada COM5 ([upload_blynk_20261019.txt](upload_blynk_20261019.txt)).
- [x] Actual device Online; dashboard standby OFF ([06-dashboard-blynk-off.png](06-dashboard-blynk-off.png)).
- [x] Pengujian slider saat OFF tidak mengaktifkan motor ([07-dashboard-blynk-slider-off160.png](07-dashboard-blynk-slider-off160.png)).
- [x] Actual device ON pada PWM 200 dengan pembacaan RPM sensor ([08-dashboard-blynk-on200.png](08-dashboard-blynk-on200.png)).
- [x] Log serial pasif bertimestamp dan screenshot terminal IDE ([09-terminal-ide-telemetri-on200.png](09-terminal-ide-telemetri-on200.png)).
- [ ] Uji pemutusan jaringan (disconnect/reconnect) terukur secara terpisah bila diperlukan.

