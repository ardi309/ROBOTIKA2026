# Catatan pengamatan - Blynk iMCLab

Pembaruan: **19 Oktober 2026, WIB**. Pengujian fisik Modul 03 telah dilakukan pada kit iMCLab ESP32 menggunakan koneksi Blynk Cloud dan logger pasif serial. Kredensial privat dan identitas mahasiswa tetap dikecualikan sesuai pedoman.

| Informasi | Isian |
| --- | --- |
| Tanggal dan jam (WIB) | 19 Oktober 2026, 22:50 - 23:14 WIB |
| Board / revisi kit | ESP32 Dev Module (ESP32-D0WDQ6 rev 1.0, 240 MHz) |
| Versi core ESP32 / Blynk / Python | Core 2.0.17 / Blynk 1.3.2 / Python 3.12.14, pySerial 3.5 |
| Tegangan catu dan jenis motor | Adaptor 5 V 2 A terpisah; USB CP210x untuk pemrograman/serial |
| Beban / kondisi poros | Motor DC tanpa beban (free running di atas meja) |
| Sensor / pulsa per putaran / posisi terhadap gearbox | Slotted optical sensor GPIO 13, asumsi PPR=2 (belum dikalibrasi) |
| Firmware / versi / port | `imclab_blynk` 1.0.0 pada COM5 (115200 baud) |
| Kondisi jaringan | Wi-Fi 2,4 GHz, Blynk Cloud server SGP1 (ping ~31 ms) |

| No. | Skenario / perintah | Setpoint | PWM aktual | RPM estimasi | Durasi / sampel | Bukti / log | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Boot & standby online | 200 | 0 | 0.0 | >30 s (kontinu) | `06-dashboard-blynk-off.png` | Firmware startup OFF, terkunci aman sampai cloud connected |
| 2 | Variasi slider saat switch OFF | 160, 180, 200 | 0 | 0.0 | ~60 s | `07-dashboard-blynk-slider-off160.png` | Setpoint tersimpan, PWM aktual konstan 0, motor tidak berputar |
| 3 | Pilot run 1 (PWM 200) | 200 | 200 | 330 -> 8280 | 6 s (6 DATA) | `serial_blynk_20261019_230428.log` | Mulai sendiri tanpa bantuan; switch OFF deselerasi 2 s ke 0 |
| 4 | Run aktif kontinu (PWM 200) | 200 | 200 | 8010 - 10260 (rata-rata 9005.7) | 63 s (62 DATA aktif) | `08-dashboard-blynk-on200.png`, `09-terminal-ide-telemetri-on200.png` | Sinkronisasi riil: pada 23:12:25 dashboard & terminal sama-sama 8.940 rpm |
| 5 | Penghentian (Switch OFF) | 200 | 0 | 8430 -> 960 -> 0.0 | 3 s (3 DATA) | `serial_blynk_20261019_230428.log` | PWM langsung 0; motor berhenti karena gesekan dan inersia |

## Pembahasan setelah eksperimen

- **Kriteria pemilihan sampel stabil**: Mengabaikan 4 sampel transisi awal saat percepatan motor dari diam (23:11:49 - 23:11:52), menyisakan 58 sampel stabil berturut-turut pada PWM 200.
- **Jumlah sampel yang dipakai**: 62 sampel aktif pada run utama (58 stabil + 4 transisi), ditambah 6 sampel pilot awal.
- **Ringkasan hasil dan bukti pendukung**: Motor berhasil dikendalikan secara nirkabel melalui dashboard Blynk web. Aktuasi switch V3 mengubah keluaran PWM menjadi 200, dan sensor pulsa mengirimkan umpan balik kecepatan secara real-time ke widget V0. Angka dashboard pada 23:12:25 WIB menunjukkan 8.940 rpm, identik dengan pembacaan sensor serial (298 pulsa/s) pada detik yang sama.
- **Perbedaan dari hipotesis**: Respon telemetri awalan membutuhkan waktu sekitar 2-4 detik untuk mencapai putaran puncak akibat inersia rotor dan selang publikasi 1 detik. Pengubahan slider saat OFF terbukti tidak memutar motor, sesuai fitur keamanan kode UTS.
- **Sumber ketidakpastian atau kegagalan**: PPR=2 masih berupa asumsi teoritis dan belum dikalibrasi terhadap tachometer standar. Fluktuasi kecepatan (8.010 - 10.260 rpm) dipengaruhi oleh fluktuasi catu daya 5V tanpa regulasi tertutup dan resolusi sampling 30 rpm per pulsa.
- **Simpulan berdasarkan data**: Sistem kendali IoT berbasis Blynk dan ESP32 berhasil diimplementasikan dengan pemisahan setpoint/enable yang andal, telemetri live dua arah yang sinkron, dan penghentian aman saat switch dimatikan.
