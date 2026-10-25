# Referensi dan pemetaan materi

## Materi dosen yang digunakan

Nomor halaman PDF di bawah dihitung dari halaman pertama berkas, termasuk sampul. Nomor cetak ditulis bila tersedia. Berkas materi tetap disimpan di folder lokal `materi/`.

| Sumber | Bagian relevan | Penggunaan |
| --- | --- | --- |
| Basuki Rahmat dan Muljono. 2024. *Pemrograman Internet of Things (IoT) dengan Arduino dan Python, Jilid 1*. Eureka Media Aksara. `EBook10_IoT_Jilid1.pdf` | Bab 3; PDF hlm. 60-65 / cetak 48-53; PDF hlm. 66-79 / cetak 54-67 | Konsep PWM dan integrasi Arduino-Python; objek buku adalah iTCLab suhu |
| Basuki Rahmat dan Muljono. 2024. *Pemrograman Internet of Things (IoT) dengan Arduino dan Python, Jilid 2*. `EBook11_IoT_Jilid2.pdf` | PDF hlm. 11 dan 131 / cetak 1 dan 121 | Peta lanjutan AI, deep learning, penalaan PID, untuk UAS |
| Basuki Rahmat. *Integrasi AI dan IoT pada Sistem Kendali Cerdas*. PDF materi kelas | Slide 3-5, 17, 19 | Arsitektur IoT, Blynk, perbedaan iTCLab/iMCLab, rujukan kode |
| `on_off_Motor.ino` | GPIO, PWM, perintah karakter `1`/`0` | Modul 01 eksperimen ON/OFF |
| `imclab_naik_turun.ino` | Newline, `+`, `-`, `PWM:xxx` | Modul 01 pengaturan PWM dan firmware pendamping Python |
| `Test_Port_Serial.ipynb` | COM11, 115200 baud, `write(b'1')` | Modul 02 komunikasi serial paling dasar |
| `Tes_IMCLab_pilih_port_otomatis.ipynb` | Deteksi port dan penutupan koneksi | Modul 02 pemilihan port |
| `Tes_IMCLab_naik_turun.ipynb` | Pengiriman newline, variasi PWM | Modul 02 kendali interaktif |
| `imclab_Blynk_kelas.ino` | V0..V3, GPIO13, HOLES=2, interrupt, timer | Modul 03; pin perangkat keras untuk seluruh paket |

`EBook10_IoT_Jilid1 copy.pdf` identik dengan versi tanpa kata `copy` berdasarkan SHA-256; tidak diperlakukan sebagai sumber tambahan. Dalam materi lokal yang diperiksa belum ada program OTA; Modul 04 merupakan pengembangan berdasarkan dokumentasi resmi.

## Dokumentasi resmi pelengkap

Diakses untuk penyusunan pada 18 Oktober 2026.

1. Espressif Systems. [Migration from 2.x to 3.0](https://docs.espressif.com/projects/arduino-esp32/en/latest/migration_guides/2.x_to_3.0.html). Perubahan LEDC dari channel ke pin.
2. pySerial. [Short introduction](https://pyserial.readthedocs.io/en/latest/shortintro.html). Serial, newline, timeout, dan daftar port.
3. Blynk. [OTA: Firmware Over-The-Air updates](https://docs.blynk.io/en/blynk.edgent/updating-devices-firmwares-ota). Alur Blynk.Air, versi, binary, dan shipping.
4. Blynk. [WiFi provisioning](https://docs.blynk.io/en/getting-started/activating-devices/blynk-edgent-wifi-provisioning). Konfigurasi perangkat menggunakan Edgent.
5. Blynk. [Over-The-Air Firmware Updates API](https://docs.blynk.io/en/blynk-library-firmware-api/ota-updates). Penerimaan permintaan di `InternalPinOTA`.
6. Blynk Technologies. [Edgent_ESP32 v1.3.2](https://github.com/Blynk-Technologies/blynk-library/tree/v1.3.2/examples/Blynk.Edgent/Edgent_ESP32). Berkas pendukung resmi yang disertakan dengan lisensi MIT dan catatan adaptasi.

## Batas penggunaan sumber

Pin iMCLab mengikuti program kelas, bukan pin pemanas iTCLab pada buku. Tidak ada tabel hasil pengukuran mahasiswa di materi yang dipakai sebagai hasil pribadi. Ilustrasi di laporan dibuat ulang sebagai diagram rancangan; foto asli dan bukti aplikasi harus berasal dari eksperimen mahasiswa.
