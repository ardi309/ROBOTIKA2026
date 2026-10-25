# Catatan pengamatan - Python iMCLab

**Status: diuji pada kit, 19 Oktober 2026 pukul 06:10-06:14 WIB.** Identitas sengaja kosong.

| Informasi | Catatan |
| --- | --- |
| Kit / firmware | iMCLab ESP32, imclab_basic 1.0.0; core ESP32 2.0.17 |
| Python / library | Python 3.12.14, pySerial 3.5, virtual environment .venv |
| Port / protokol | COM5, Silicon Labs CP210x, 115200 baud, newline |
| Catu | Adaptor bawaan 5 V 2 A menurut informasi label dari operator; tidak diukur dengan multimeter |
| Posisi | Operator menyatakan USB/adaptor terpasang, kit di meja, piringan bebas bergerak |
| Sensor / RPM | GPIO13, FALLING, debounce 500 us; PPR=2 masih asumsi |
| Jaringan | Tidak diperlukan untuk kendali Python melalui USB |

## Sesi dan konfirmasi operator

1. Uji OFF 06:10:24: semua PWM=0. Dua dari lima DATA masing-masing berisi satu pulsa; penyebab belum diketahui. Tidak diklaim sebagai putaran motor yang diperintahkan.
2. Pilot PWM 200 06:10:43: dua DATA aktif berisi 101 dan 199 pulsa. Jarak TX ON-OFF 2,194 detik. Operator menjawab: **“Ya, berputar sendiri lalu berhenti”** terhadap pertanyaan tentang putaran tanpa bantuan tangan.
3. Rangkaian 06:12:41: PWM 200 -> 160 -> 120, sekitar 15 detik per tahap. Operator menjawab: **“Ya, tetap berputar pelan lalu berhenti; tanpa bantuan”** untuk tahap akhir. Setelah OFF, DATA berisi 19, 0, 0 pulsa. Tidak ada penghentian dini atau ERROR.
4. Uji perintah 06:14:13: pemilihan port otomatis, R, p200, -, +, p255, p0, p256, ON, p200, 0, q. Semua PWM aktual tetap 0. Nilai tidak valid ditolak di Python sebelum dikirim. Target akhir 200; motor OFF.

Sesi OFF dan pilot menggunakan program awal; rangkaian utama dan uji perintah memakai revisi dengan pemeriksaan ACK sesuai perintah, DTR/RTS false, guard tiga detik, dan pembacaan tiga detik setelah OFF. Firmware ESP32 tidak diubah.

## Pengolahan data

Empat CSV asli berisi 67 DATA; ACK/STATUS tidak diduplikasi sebagai sampel. Grafik dan angka berasal dari [analisis JSON](hasil_analisis.json), [CSV DATA turunan](sampel_serial.csv), serta [indeks sumber](ringkasan_log.md).

| PWM | Lima pulsa/detik terakhir terpilih | Rata-rata | Simpangan baku sampel | Rentang relatif | Stabil menurut kriteria |
| --- | --- | --- | --- | --- | --- |
| 200 | 262, 264, 266, 269, 275 | 267,2 | 5,0695 | 4,8653% | Ya |
| 160 | 132, 134, 132, 138, 133 | 133,8 | 2,4900 | 4,4843% | Ya |
| 120 | 21, 20, 22, 20, 21 | 20,8 | 0,8367 | 9,6154% | Tidak |

Kriteria sama dengan Modul 01: fase selesai normal, lima DATA terakhir dengan seluruh jendela setelah lima detik awal, pulsa positif, rentang/rata-rata <=5%. Kelima sampel bukan pengulangan independen. Fase selesai dinilai dari alur program yang berlanjut normal tanpa EVENT ERROR/INTERRUPTED; jam kalender CSV berbeda dari timer monotonic.

Pada PWM 200 dan 160, selisih terhadap rata-rata Modul 01 adalah -4,16% dan +1,52%. Pada PWM 120, sesi ini mempertahankan putaran sedangkan sesi Modul 01 berhenti. Pengujian tidak menetapkan ambang start atau menyimpulkan penyebab mekanis/kelistrikan.

## Yang belum diuji / dilengkapi

- Kalibrasi PPR dan tegangan catu saat berbeban.
- Replikasi independen dan start dari diam pada PWM 120.
- Latensi komunikasi terukur dan respons saat kabel terputus.
- Guard tanpa pulsa/telemetri diuji dengan port tiruan, belum terpicu dalam sesi fisik Modul 02.

## Dokumentasi tambahan - 19 Oktober 2026

- Pemeriksaan OFF pada 11:24:50 WIB: 9 DATA dengan PWM=0; tiga DATA terakhir berisi 1, 1, dan 2 pulsa. Penyebab belum diketahui dan data tidak diubah.
- Operator mengulang pemeriksaan OFF pada 11:28:27 WIB dan mengirim [screenshot terminal asli](../bukti/02-terminal-python-off.png). Semua DATA pada sesi ini melaporkan PWM=0 dan RPM=0; tidak ada TX ON.
- [Foto susunan kit](../bukti/03-foto-susunan-kit.png) diterima dari operator pada 19 Oktober 2026. Status putaran dan RPM tidak ditentukan dari foto tunggal.
- Percobaan ON pada 11:33:48 WIB gagal membuka COM5 (Access is denied). CSV hanya memuat EVENT ERROR; tidak ada perintah motor yang dikirim pada percobaan ini. Penyebab penguncian port tidak teridentifikasi.
- Operator mengulang ON pada 11:35:27 WIB dan mengirim [screenshot terminal](../bukti/04-terminal-python-on200.png), disertai pesan "oke bisa nih lalu?". CSV memuat 11 DATA: 3 sebelum ON, 5 aktif pada PWM 200, dan 3 setelah OFF. Pulsa aktif 69, 203, 250, 258, 268 per 1000 ms; RPM estimasi 2070, 6090, 7500, 7740, 8040. Jarak TX ON-OFF 5,198435 detik. DATA setelah OFF berisi 285, 3, 0 pulsa; DATA terakhir PWM=0 dan RPM=0. Pesan operator tidak dipakai sebagai konfirmasi tambahan tentang bantuan tangan pada sesi ini.
- Data dokumentasi tambahan terpisah dari 67 DATA pada empat sesi utama. Grafik dan tabel perbandingan tetap memakai sesi utama.
