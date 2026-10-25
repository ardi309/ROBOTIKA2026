# Bukti eksperimen - Basic iMCLab

## Foto dan screenshot asli

| Berkas | Keterangan dan batas bukti |
| --- | --- |
| [Foto identifikasi kit](00-foto-identifikasi-kit.png) | Foto awal yang diberikan pengguna, disalin tanpa mengubah gambar. Bukan foto susunan pengukuran di meja. |
| [Serial Monitor OFF awal](01-serial-monitor-off.jpg) | Bukti awal COM5, 115200 baud, New Line, PWM=0 SET=200. |
| [Serial Monitor OFF akhir](02-serial-monitor-akhir-off.jpg) | Screenshot asli sesudah seluruh rangkaian, 19 Oktober 2026. Seluruh imclab_basic.ino terlihat, ESP32 Dev Module, COM5, New Line, 115200 baud, data PWM=0 SET=200 RPM=0 PULSES=0. Timestamp yang ditampilkan IDE sekitar 05:54, berbeda dari waktu rangkaian motor 01:21 karena screenshot diambil kemudian. Tampilan diperbesar 150%, bukan angka data yang diedit. |

Lokasi sketch aktif diperiksa melalui menu **Sketch > Show Sketch Folder** dan menunjuk ke `D:/ryudev_area/robotika/UTS/01_Basic_iMCLab/program/imclab_basic`. Foto/screenshot disimpan sebagai bukti asli; tidak ada screenshot motor ON yang direkayasa dari data OFF.

![Screenshot kondisi akhir OFF](02-serial-monitor-akhir-off.jpg)

## Bukti ketika motor berjalan

Rangkaian otomatis direkam langsung ke [log mentah](../data/ringkasan_log.md). Saat itu port dimiliki skrip pengukuran, sehingga bukti kuantitatif utamanya adalah log, bukan tampilan Serial Monitor yang dibuka bersamaan. Grafik di [hasil_variasi.svg](../gambar/hasil_variasi.svg) berasal dari DATA asli, bukan screenshot alat ukur.

Konfirmasi operator mengenai gerakan, bantuan putaran manual, LED, dan berhenti setelah OFF tercatat di [pengamatan.md](../data/pengamatan.md).

- [x] Foto identifikasi kit.
- [x] Screenshot sketch yang tepat dan data OFF.
- [x] Log ON/OFF, variasi saat berjalan, serta pemeriksaan parser.
- [x] Grafik dan analisis data.
- [ ] Foto susunan kit di meja saat praktik, memperlihatkan USB dan catu.
- [ ] Kalibrasi jumlah pulsa per putaran.

Foto susunan praktik masih menunggu pengguna. Jika diterima, tambahkan caption sesuai keadaan sebenarnya; jangan menyatakan motor ON bila foto diambil saat OFF.