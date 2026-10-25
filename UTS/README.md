# UTS Robotika - Eksperimen Kit iMCLab

**Status:** Rangkaian eksperimen UTS Robotika (Modul 01 s/d 04) telah selesai penuh (**100% Selesai**). Seluruh modul memuat hasil pengujian fisik riil pada kit iMCLab ESP32, telemetri empiris, pembuktian keselamatan motor, tangkapan layar asli, dan dokumen laporan akademik PDF format standar dengan identitas mahasiswa lengkap: **Hidayat Nur Tauhid** (NIM: **24081010133**, Kelas: **Robotika A081**).

Untuk riwayat detail dan dokumentasi pengujian, baca [PROGRES_03_04.md](PROGRES_03_04.md), [VERIFIKASI.md](VERIFIKASI.md), dan [CHECKLIST.md](CHECKLIST.md).

Rangkaian eksperimen ini mengembangkan kendali motor DC secara bertahap mulai dari kendali lokal serial Arduino, komunikasi antarmuka GUI Python, pemantauan dan kendali jarak jauh IoT Blynk Cloud, hingga pembaruan firmware nirkabel skala armada (*Fleet OTA*) melalui Blynk.Air.

## Modul dan Status Pengujian

| Syarat UTS | Berkas Laporan | Dokumen PDF | Status Pengujian Fisik | Bukti Empiris Utama |
| --- | --- | --- | --- | --- |
| Basic robotika dengan Kit iMCLab | [01 - Laporan basic](01_Basic_iMCLab/LAPORAN.md) | [01 - PDF (6 hal)](01_Basic_iMCLab/LAPORAN.pdf) | Selesai | 14 log asli, 135 sampel DATA, uji parser & PWM |
| iMCLab menggunakan Python | [02 - Laporan Python](02_Python_iMCLab/LAPORAN.md) | [02 - PDF (8 hal)](02_Python_iMCLab/LAPORAN.pdf) | Selesai | 4 CSV asli, 67 DATA, screenshot terminal & foto kit |
| iMCLab berbasis Blynk | [03 - Laporan Blynk](03_Blynk_iMCLab/LAPORAN.md) | [03 - PDF (8 hal)](03_Blynk_iMCLab/LAPORAN.pdf) | Selesai | 4 screenshot setting, 62 data aktif, sinkron 1:1, pilot & run 63s |
| OTA berbasis Blynk.Air | [04 - Laporan OTA](04_OTA_Blynk/LAPORAN.md) | [04 - PDF (9 hal)](04_OTA_Blynk/LAPORAN.pdf) | Selesai | 5 screenshot konsol, log serial UART OTA 17,56s, MD5 valid, reboot v1.0.1 |

## Ringkasan Struktur Direktori

```text
Robotika/
  UTS/
    IDENTITAS.md         # Template identitas mahasiswa
    PANDUAN_PRAKTIK.md   # Panduan teknis pengoperasian kit
    REFERENSI.md         # Kajian teori dan pemetaan modul
    CHECKLIST.md         # Lembar checklist verifikasi
    PROGRES_03_04.md     # Catatan riwayat rekayasa 03 dan 04
    VERIFIKASI.md        # Verifikasi teknis hardware dan software
    01_Basic_iMCLab/     # Modul 01: Laporan, program, data, bukti
    02_Python_iMCLab/    # Modul 02: Laporan, program GUI, data, bukti
    03_Blynk_iMCLab/     # Modul 03: Laporan, program IoT, data, bukti
    04_OTA_Blynk/        # Modul 04: Laporan, program Edgent OTA, data, bukti
    tests/               # Unit testing perangkat lunak
    tools/               # Generator diagram dan generator PDF
  UAS/
    README.md
```

## Laporan Versi PDF

Dokumen PDF formal tersedia di masing-masing direktori modul dan telah divalidasi tata letaknya secara visual (tanpa halaman yatim, tabel presisi, dan gambar beresolusi tinggi):

- [Modul 01 - Laporan Basic (PDF)](01_Basic_iMCLab/LAPORAN.pdf)
- [Modul 02 - Laporan Python (PDF)](02_Python_iMCLab/LAPORAN.pdf)
- [Modul 03 - Laporan Blynk IoT (PDF)](03_Blynk_iMCLab/LAPORAN.pdf)
- [Modul 04 - Laporan Blynk.Air OTA (PDF)](04_OTA_Blynk/LAPORAN.pdf)

Versi Markdown dipertahankan agar laporan dapat disunting atau disesuaikan dengan mudah.
