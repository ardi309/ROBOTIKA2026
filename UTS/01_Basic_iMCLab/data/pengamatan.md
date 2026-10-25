# Catatan pengamatan - Basic iMCLab

**Status: komunikasi USB, motor, variasi PWM saat berjalan, dan parser sudah diuji.** Start motor belum konsisten. Data mentah tidak diubah; hasil gagal tetap disertakan.

## Kondisi alat

| Informasi | Catatan |
| --- | --- |
| Tanggal | USB: 18 Oktober 2026, 21:37 WIB. Uji motor/parser: 19 Oktober 2026, 00:50-01:22 WIB. |
| Kit | iMCLab; ESP32-D0WDQ6 revisi v1.0; revisi PCB, tipe driver, dan spesifikasi motor belum dikonfirmasi. |
| Catu | Label adaptor bawaan menurut operator: 5 V 2 A. Tegangan berbeban dan arus tidak diukur. |
| Mekanik | Kit di meja dan piringan/poros bebas menurut operator. Sambungan adaptor serta kabel hijau terlihat kuat saat pemeriksaan visual. |
| Firmware | imclab_basic 1.0.0; ESP32 Dev Module; core 2.0.17; COM5 115200 baud. Unggah dan hash flash sebelumnya diverifikasi esptool. |
| Sensor | GPIO 13, FALLING, debounce 500 mikrodetik. Asumsi PPR=2 belum dikalibrasi. |
| Metode | Perintah otomatis lewat serial; operator mengamati gerak. Tidak memakai Blynk/jaringan pada Modul 01. |

## Hubungan log dengan pengamatan operator

| Log/skenario | Sensor | Pengamatan fisik dan batas bukti |
| --- | --- | --- |
| [USB OFF](usb_motor_off_20261018_213758.log) | 8 DATA, PWM=0 dan pulsa nol | Komunikasi serta status OFF berhasil. |
| [PWM 120 awal](motor_pwm120_20261019_005007.log) | Semua pulsa nol selama ON 5,068 s | Operator: tidak bergerak sama sekali. |
| [PWM 200 pilot](motor_pwm200_20261019_005512.log) | 82 dan 199 pulsa saat ON 2,150 s | Operator: berputar lalu berhenti. |
| Tiga pengulangan PWM 200 pukul 00:57 | Pulsa maksimum 259, 259, 274 per jendela 1 detik | Operator kemudian mengonfirmasi tes otomatis yang berhasil tidak dibantu tangan. Data akhir tiap tes kembali nol setelah OFF. |
| Start dari diam 80, 120, 160, 200 pukul 00:57-00:58 | Semua pulsa nol; cutoff sekitar 3 detik | Operator tidak mengamati seluruh rangkaian; adaptor dilaporkan tetap terpasang. Jangan menyamakan ini dengan konfirmasi visual per kondisi. |
| [PWM 200 ulang pukul 01:00](motor_pwm200_20261019_010055.log) | Semua pulsa nol | Operator: motor tetap diam; ada LED berubah. |
| Percobaan manual terpisah | Tidak ada log kuantitatif yang diserahkan | Operator melaporkan motor mau berputar setelah dipancing putaran awal dan berhenti dengan perintah 0. Pengamatan ini tidak dimasukkan ke perhitungan rata-rata atau dianggap penjelasan penyebab yang pasti. |
| [PWM 200 ulang pukul 01:19](motor_pwm200_20261019_011923.log) | 0 lalu 84 pulsa saat ON 2,024 s | Operator: mulai sendiri lalu berhenti, tanpa bantuan. |
| [Variasi saat berjalan](basic_variasi-berjalan_20261019_012135.log) | PWM 200 dan 160 selesai; pulsa turun hingga nol pada 120 | Operator: mulai sendiri, melambat, lalu berhenti; tanpa menyentuh/membantu piringan. Tahap 80 dilewati. |
| [Uji parser saat OFF](basic_perintah_20261019_012248.log) | 10 CHECK PASS, seluruh PWM=0 | Tidak mengirim ON. Nilai 255 hanya diuji sebagai setpoint saat OFF. |

## Hasil kuantitatif variasi saat berjalan

| PWM | Durasi fase | Pulsa/detik rata-rata | Simpangan baku sampel | RPM estimasi PPR=2 | n |
| --- | --- | --- | --- | --- | --- |
| 200 | 15,024 s | 278,8 | 4,38 | 8.364 | 5 |
| 160 | 15,199 s | 131,8 | 0,45 | 3.954 | 5 |
| 120 | 10,802 s, dihentikan dini | Tidak diringkas sebagai putaran stabil | Tidak dihitung | Tidak ditetapkan | 0 |
| 80 | Dilewati setelah cutoff | Tidak tersedia | Tidak tersedia | Tidak tersedia | 0 |

Kriteria deskriptif ditetapkan saat analisis: lima DATA terakhir pada fase 15 detik yang selesai, jendela sampel sepenuhnya melewati lima detik pertama, pulsa positif, rentang/rata-rata <=5%. Rentang PWM 200 adalah 3,5868%; PWM 160 adalah 0,7587%. Timestamp lima sampel terpilih tersedia di [hasil_analisis.json](hasil_analisis.json).

Pada PWM 120, urutan pulsa adalah 113, 54, 28, 18, 13, 11, 2, 1, 0, 0, 0. Sampel awal mencakup transisi dari PWM 160. Satu pulsa tercatat pada sampel pertama setelah OFF, kemudian nol. Tidak ada rata-rata RPM stabil untuk kondisi ini.

## Indikator dan ketidakpastian

Menurut operator, hijau tetap menyala menunjukkan catu adaptor, hijau berkedip menunjukkan deteksi RPM, merah menunjukkan USB, dan biru menunjukkan perintah ON. Keterangan warna/fungsi merupakan laporan operator, belum pemeriksaan skema listrik.

Start pada PWM 200 kadang berhasil dan kadang gagal. Penyebabnya belum terukur. Tegangan, arus, suhu, PPR, dan kondisi driver tidak direkam. Laju pulsa pada kondisi berjalan tidak dapat dipakai langsung untuk menyimpulkan ambang start dari diam.

## Berkas analisis

- [Indeks seluruh 14 log](ringkasan_log.md), termasuk durasi dan hasil gagal.
- [135 sampel DATA dalam CSV](sampel_serial.csv); ACK/STATUS dikecualikan agar tidak menghitung ulang sampel.
- [Hasil analisis dan timestamp pemilihan sampel](hasil_analisis.json).
- [Grafik laju pulsa](../gambar/hasil_variasi.svg).
- Skrip olah data: [analisis_basic.py](../../tools/analisis_basic.py). Tidak membuka port serial.