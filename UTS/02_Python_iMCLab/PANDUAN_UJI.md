# Menjalankan ulang Modul 02

**Pengujian awal sudah selesai.** PDF, CSV, grafik, dan catatan operator tersimpan di folder ini. Langkah berikut untuk mengulangi eksperimen atau mengambil screenshot tambahan.

## Persiapan

1. Gunakan firmware Modul 01 yang sudah diunggah. Tidak perlu mengunggah Python ke ESP32.
2. Sambungkan USB. Untuk uji motor, pasang adaptor bawaan 5 V 2 A, letakkan kit di meja, dan pastikan piringan bebas.
3. Tutup Serial Monitor/Serial Plotter Arduino. Buka PowerShell di `D:\ryudev_area\robotika`.
4. Di komputer ini `.venv` dan pySerial 3.5 sudah siap. Pada komputer lain, buat dengan `python -m venv .venv`, lalu instal `requirements.txt` dari folder program.

## Periksa sambungan tanpa menyalakan motor

```powershell
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --list
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --port COM5 --capture 3 --pwm 0
```

COM5 adalah port saat eksperimen ini; ganti jika berbeda. Tunggu perintah selesai. Screenshot dapat diambil dengan terminal diperbesar agar perintah lengkap, ACK/DATA, dan lokasi CSV terbaca. Tidak perlu mengubah `.ino` untuk langkah ini.

## Dokumentasi layar yang sudah tersedia

Screenshot OFF, screenshot ON pada PWM 200, serta foto susunan kit sudah dimasukkan ke laporan. Untuk mengulang bukti ON bila diperlukan, buka PowerShell sendiri dan jalankan perintah berikut setelah kit siap:

```powershell
& 'D:\ryudev_area\robotika\.venv\Scripts\python.exe' 'D:\ryudev_area\robotika\UTS\02_Python_iMCLab\program\bukti_motor_on.py'
```

Program menyalakan PWM 200 selama sekitar lima detik, mengirim OFF, membaca telemetri tambahan, dan menyimpan CSV serta konsol teks dengan waktu baru. Ambil screenshot setelah selesai, dengan judul sesi, jalur program, DATA aktif, DATA terakhir, dan kode keluar terlihat. Jendela menunggu Enter. Foto susunan kit dapat diambil saat OFF; foto tidak digunakan untuk menaksir RPM.

Jika muncul `Access is denied` saat membuka COM5, tutup Serial Monitor/Serial Plotter dan akhiri sesi Python lain yang masih memakai port itu, lalu jalankan ulang. Jangan membuka dua pembaca serial sekaligus. Error saat membuka port berarti sesi tersebut belum mengirim perintah; log gagal tetap disimpan.

## Uji singkat saat siap mengamati motor

Perintah berikut menyalakan motor sekitar dua detik kemudian mengirim OFF:

```powershell
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --port COM5 --capture 2 --pwm 200
```

Amati apakah piringan mulai sendiri dan berhenti setelah tes. Jangan membantu memutar ketika catu motor aktif. Jika tidak berputar, catat hasil itu; jangan langsung mengulang tes panjang.

## Rangkaian otomatis untuk mengubah PWM

Setelah uji singkat berhasil dan operator siap, gunakan:

```powershell
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --port COM5 --capture 15 --sweep 200 160 120
```

Motor dimulai pada 200, lalu target menjadi 160 dan 120, sekitar 15 detik per tahap. Capture menghentikan rangkaian jika tidak ada pulsa atau DATA selama tiga detik. Setelah selesai/error, program mencoba mengirim OFF dan membaca DATA selama tiga detik tambahan. Pesan cutoff adalah hasil yang perlu dicatat, bukan alasan menghapus log.

Log otomatis memakai nama baru di `data/`; `--log` dapat memilih nama CSV sendiri, tetapi berkas yang sudah ada ditolak. EVENT berasal dari Python, sedangkan TX/RX adalah perintah dan respons serial asli.

## Perintah manual bila diperlukan

```powershell
.\.venv\Scripts\python.exe UTS/02_Python_iMCLab/program/kontrol_imclab.py --port COM5
```

| Input | Fungsi |
| --- | --- |
| p200 | Atur target 200; saat OFF motor tetap OFF |
| 1 | Aktifkan motor pada target |
| p160 | Ubah target menjadi 160 |
| + / - | Naik / turun 10 |
| R | Minta status |
| 0 | Matikan motor |
| q | Keluar dan kirim OFF |

**Utamakan capture otomatis untuk pencatatan berkala.** Mode manual menunggu input sehingga DATA dapat menumpuk; guard tiga detik hanya aktif saat capture dengan PWM > 0. Ctrl+C mencoba menghentikan sesi. Jika USB terlepas atau proses berhenti paksa, cabut catu motor karena firmware basic belum mempunyai watchdog komunikasi.

Untuk laporan, catat tanggal, adaptor, start tanpa bantuan, gerakan tiap PWM, dan keadaan setelah OFF. RPM masih estimasi hingga PPR dikalibrasi.
