# Panduan uji manual Modul 01 — Basic iMCLab

Panduan ini mengikuti `program/imclab_basic/ImcCore.h`. Program basic sudah diunggah pada sesi sebelumnya. Tidak perlu memasang ulang driver atau mengunggah ulang selama firmware belum diganti. Port terakhir adalah COM5.

Pada sesi sebelumnya, PWM 200 pernah menghasilkan gerakan dan pulsa, tetapi kemudian gagal memulai gerak. Karena itu, lakukan pemeriksaan singkat pada langkah 3 sebelum pengujian panjang. Hasil gagal tetap dicatat sebagai hasil eksperimen.

## 1. Persiapan

1. Letakkan kit di meja, dengan piringan/poros bebas bergerak dan kabel tidak menyentuh bagian berputar.
2. Sambungkan USB. Untuk pemeriksaan awal, adaptor motor belum perlu dipasang.
3. Di Arduino IDE buka [imclab_basic.ino](program/imclab_basic/imclab_basic.ino). `ImcCore.h` tetap berada di folder yang sama.
4. Pastikan board **ESP32 Dev Module**, port **COM5**. Jika nomor port berubah setelah USB dipasang ulang, gunakan port milik kit yang muncul.
5. Buka **Serial Monitor**. Pilih **115200 baud** dan **New Line/Newline**.
6. Ketik satu perintah di kolom kirim, lalu tekan Enter. Jangan tempel beberapa perintah sekaligus.

Firmware ini **tidak memiliki timer otomatis untuk mematikan motor**. Waktu 2, 5, atau 15 detik di bawah harus kamu pantau sendiri. Jika perintah `0` gagal menghentikan motor, cabut adaptor motor.

## 2. Cek komunikasi dan setpoint saat OFF

Kirim berurutan:

| Perintah | Respons yang diperiksa |
| --- | --- |
| `0` | Ada `ACK PWM=0`; motor diam. |
| `PWM:200` | Ada `ACK PWM=0 SET=200`; motor tetap OFF. |
| `R` | Ada `STATUS PWM=0 SET=200`. |

Tunggu sekitar 3 detik. Simpan screenshot atau salin respons beserta beberapa baris `DATA`. Jika ACK tidak muncul atau tulisan tidak terbaca, berhenti di sini dan kirim tampilannya.

`SET` adalah target yang disimpan. `PWM` adalah keluaran yang dilaporkan firmware, bukan pengukuran tegangan. Target 200 saat OFF tetap menghasilkan `PWM=0`.

## 3. Pemeriksaan gerak singkat — PWM 200

1. Pasang adaptor bawaan berlabel **5 V 2 A** ke kit dan listrik. Pastikan piringan tetap bebas.
2. Kirim `0`, lalu `PWM:200`, masing-masing dengan Enter.
3. Kirim `1`. Amati motor dan LED selama sekitar **2 detik**.
4. Segera kirim `0`, baik motor berputar maupun tetap diam. Tunggu sampai piringan berhenti dan amati beberapa baris `DATA` setelah OFF.
5. Catat: berputar normal / hanya bergetar / tetap diam; perubahan LED; apakah berhenti setelah `0`; respons `ACK` dan `DATA`.

**Jika motor diam atau tersendat, jangan lanjutkan langkah 4–5.** Kirim hasil langkah 1–3 untuk diperiksa. Jika motor terlihat berputar tetapi `PULSES` tetap nol pada beberapa sampel, kirim hasil tersebut juga sebelum tes panjang. LED menyala sendiri tidak membuktikan motor berputar.

## 4. Uji ON/OFF tiga kali

Lanjut hanya jika pemeriksaan singkat berhasil: motor berputar, pulsa terdeteksi, dan motor berhenti setelah OFF.

Untuk setiap pengulangan, kirim `0`, `PWM:200`, lalu `1`. Amati paling lama **5 detik**, kemudian kirim `0`. Tunggu motor benar-benar berhenti, lalu beri jeda sekitar 10 detik sebelum pengulangan berikutnya. Lakukan tiga pengulangan dengan urutan sama.

Jika suatu pengulangan tidak mulai berputar dalam sekitar 2 detik, kirim `0` dan hentikan rangkaian tes. Catat pengulangan yang gagal; jangan menaikkan PWM untuk menutupi kegagalan.

Salin log tiap pengulangan, mulai dari perintah/ACK sampai beberapa baris DATA setelah OFF. Catat pengamatan fisik secara terpisah dari data sensor.

## 5. Uji variasi PWM

Lanjut hanya jika ketiga uji ON/OFF berhasil. Setiap kondisi harus dimulai dari motor berhenti/OFF; jangan mengubah metode menjadi menurunkan PWM saat motor masih berjalan.

| Kondisi | Urutan perintah, satu per satu | Durasi saat ON |
| --- | --- | --- |
| PWM 80 | `0` → `PWM:80` → `1` → amati → `0` | Maksimal 15 detik jika berputar normal |
| PWM 120 | `0` → `PWM:120` → `1` → amati → `0` | Maksimal 15 detik jika berputar normal |
| PWM 160 | `0` → `PWM:160` → `1` → amati → `0` | Maksimal 15 detik jika berputar normal |
| PWM 200 | `0` → `PWM:200` → `1` → amati → `0` | Maksimal 15 detik jika berputar normal |

Jika pada suatu kondisi motor tetap diam atau hanya bergetar sekitar **2 detik**, segera kirim `0`. Catat durasi pendek tersebut dan kondisi motor; jangan menunggu 15 detik. Setelah berhenti dan jeda sekitar 10 detik, boleh mencoba kondisi berikutnya dalam tabel. Jika PWM 200 kembali gagal, hentikan pengujian motor dan laporkan.

Jika motor berputar tetapi pembacaan pulsa terus nol, hentikan pengujian untuk memeriksa sensor. Jangan menyebut RPM nol sebagai bukti motor diam tanpa melihat poros.

Salin seluruh log tiap kondisi setelah motor OFF. Jangan hanya mengambil satu angka RPM atau hanya baris ACK. Tidak semua uji 15 detik otomatis menghasilkan kondisi stabil; pemilihan sampel akan dijelaskan saat analisis.

## 6. Uji perintah dan batas nilai tanpa menyalakan motor

Kirim `0`, tunggu motor berhenti, lalu **cabut adaptor motor dari listrik**; USB tetap terpasang. Semua perintah di tabel berikut dilakukan saat OFF. Jangan mengirim `1` pada bagian ini.

| Perintah | Respons yang diharapkan |
| --- | --- |
| `PWM:200` | `ACK PWM=0 SET=200` |
| `-` | `ACK PWM=0 SET=190` |
| `+` | `ACK PWM=0 SET=200` |
| `PWM:0` | `ACK PWM=0 SET=0` |
| `PWM:255` | `ACK PWM=0 SET=255` |
| `PWM:256` | `ERR PWM must be 0..255`; target sebelumnya tetap 255 |
| `abc` | `ERR use 0, 1, +, -, PWM:0..255, R` |
| `PWM:200` | Kembalikan target: `ACK PWM=0 SET=200` |
| `0` | Pastikan tetap OFF |

PWM 255 di sini hanya menguji penerimaan nilai saat OFF, **bukan** eksperimen motor dengan daya penuh. Dalam firmware ini, perintah `1` ketika target nol akan mengganti target menjadi 200; `PWM:0` bukan pengunci motor.

## 7. Bukti dan hasil untuk laporan

Ambil satu foto kit saat pengujian yang memperlihatkan sambungan USB dan adaptor. Tambahkan screenshot Serial Monitor saat OFF, saat PWM aktif, serta hasil penolakan perintah. Jika merekam video singkat gerakan motor, siapkan perekaman sebelum ON agar perintah OFF tidak terlambat.

Simpan bukti di [bukti/](bukti/README.md), atau kirim langsung ke chat. Untuk data angka, salin teks Serial Monitor jika memungkinkan. Baris `DATA` dipakai untuk perhitungan; `ACK` dan `STATUS` dapat mengulang sampel terakhir sehingga bukan sampel pengukuran tambahan. RPM masih memakai asumsi 2 pulsa per putaran dan belum dikalibrasi.

Isi format berikut sesuai yang benar-benar dikerjakan. Tulis **belum diuji** untuk tahapan yang dilewati, bukan angka nol.

```text
Tanggal/jam pengujian:
Board dan port:
Catu: adaptor berlabel ... V ... A; terpasang/tidak:

Cek OFF: ACK ...; motor ...
Setpoint saat OFF: ACK ...; motor ...
Tes singkat PWM 200 (sekitar 2 detik):
  Motor: berputar / bergetar / diam
  LED:
  Setelah 0:
  Log/screenshot:

ON/OFF PWM 200:
  Ulangan 1: durasi ...; gerakan ...; setelah OFF ...
  Ulangan 2: durasi ...; gerakan ...; setelah OFF ...
  Ulangan 3: durasi ...; gerakan ...; setelah OFF ...
  Log tiap ulangan:

Variasi PWM:
  80: durasi ...; motor ...; log ...
  120: durasi ...; motor ...; log ...
  160: durasi ...; motor ...; log ...
  200: durasi ...; motor ...; log ...

Uji perintah saat OFF: hasil/screenshot ...
Foto kit:
Catatan lain:
```

Analisis dan PDF diperbarui dari log serta pengamatan tersebut. Hasil gagal dicantumkan bersama hasil berhasil; hubungan PWM–RPM dan ambang awal gerak tidak disimpulkan dari satu percobaan saja.
