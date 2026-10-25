# Memperbarui gambar dan PDF

Sumber laporan adalah `LAPORAN.md` di setiap folder modul. Modul 01-02 sudah berisi hasil uji awal; Modul 03-04 masih draf sebelum eksperimen.

Untuk regenerasi dari root repositori:

```powershell
python UTS/tools/buat_diagram.py
python UTS/tools/buat_pdf.py
```

Untuk mengolah log Modul 01 dan mengekspor hanya PDF modul tersebut:

```powershell
python UTS/tools/analisis_basic.py
python UTS/tools/buat_pdf.py --modul 01
```

Analisis membaca seluruh log asli menjadi CSV DATA dan indeks; grafik serta ringkasan fase memakai sesi `basic_variasi-berjalan_20261019_012135.log`. Skrip tidak membuka port serial. Paket grafik yang dipakai adalah ReportLab.

Untuk Modul 02:

```powershell
python UTS/tools/analisis_python.py
python UTS/tools/buat_pdf.py --modul 02
```

Analisis Python membaca empat CSV `python_*.csv`, mengecualikan ACK/STATUS, memeriksa kolom terhadap teks raw, dan membentuk grafik sesi `python_sweep_20261019_061241.csv`. Hasil lima sampel akhir tetap diberi label tidak stabil bila rentang relatif melebihi 5%. Skrip ini tidak membuka port. Dependensi `.venv` untuk kendali serial hanya pySerial; analisis/generasi PDF memakai runtime dengan ReportLab dan svglib.

Di workspace ini dependensi PDF sudah tersedia dalam `.tools/pdf-python`. Pada komputer lain, pasang `reportlab` dan `svglib` di virtual environment terlebih dahulu. Pembuat PDF memakai Calibri Windows, atau DejaVu Sans pada Linux.

Output utama berada di `output/pdf/`. Salinan identik juga ditulis ke `UTS/<modul>/LAPORAN.pdf` agar dapat dikumpulkan bersama folder modul. Perintah ekspor akan mengganti PDF sebelumnya, tetapi tidak mengubah sumber Markdown.

Identitas dibaca dari `UTS/IDENTITAS.md`; nilai kosong dicetak sebagai garis isian. Tambahkan foto PNG/JPG atau diagram SVG ke Markdown memakai sintaks gambar biasa. Eksportir menjaga gambar dan caption yang diawali `**Gambar` pada halaman yang sama.

Status dapat dicantumkan pada sumber Markdown dengan `Status laporan: **...**`. Tanggal uji dibaca dari `Tanggal eksperimen: **...**`; identitas lainnya tetap dibaca dari berkas identitas. Tanpa status hasil uji, eksportir mempertahankan keterangan draf. `<!-- pagebreak -->` memberi pemisah halaman eksplisit pada PDF.

Direktori `.tools/pdf-python` dipakai sebagai fallback setelah paket runtime aktif agar paket biner dari versi Python lain tidak menimpa paket runtime yang cocok.

## Skrip pengujian kit

`uji_basic_serial.ps1` memiliki mode `perintah` (default, tetap OFF) dan `variasi-berjalan` (menyalakan motor). Tutup Serial Monitor sebelum menjalankan skrip; pastikan operator siap dan poros bebas. Mode variasi menurunkan PWM 200 -> 160 -> 120 -> 80, maksimal 15 detik per fase, dan menghentikan rangkaian jika tidak ada pulsa selama 3 detik. Skrip mencoba mengirim OFF di blok finally. Putusnya koneksi tetap dapat menggagalkan OFF; firmware tidak memiliki watchdog motor, sehingga operator harus dapat mencabut catu.

Sesudah ekspor, periksa semua halaman PDF: teks, gambar, tabel, caption, sumber, dan nomor halaman. PDF yang berhasil dibuat belum tentu memiliki tata letak yang baik.
