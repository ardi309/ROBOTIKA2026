# Bukti Eksperimen - OTA Blynk.Air (Modul 04)

Seluruh bukti eksperimen fisik dan tangkapan layar konsol cloud disimpan pada folder ini:

1. `01-setting-v4-firmware-version.png`: Konfigurasi Datastream virtual pin V4 (`Firmware Version`, tipe String, default `1.0.0`) pada Template `iMCLab UTS` (`TMPL6YpVE_Y1G`).
2. `02-blynkair-shipping-create-100-to-101.png`: Halaman formulir *New Shipping* di Blynk.Air yang menampilkan deteksi otomatis firmware perangkat berjalan pada versi `1.0.0` dan berkas biner pembaruan `imclab_ota_v101.bin` versi `1.0.1` (995.344 byte, MD5 `36101394FEF84E8145460BAFFFA4C4F0`).
3. `03-dashboard-sebelum-ota.png`: Kondisi dashboard perangkat `iMCLab Modul 03` sebelum OTA dieksekusi (status Online, motor OFF aman, setpoint slider 200).
4. `04-blynkair-shipping-in-progress-updated1.png`: Dialog modal *Shipping In Progress* dengan bilah kemajuan hijau penuh (Target: 1 Device, Updated: 1 Device) membuktikan proses pengiriman sukses.
5. `05-blynkair-shipments-completed-v101.png`: Riwayat tabel *Shipments* (ID 51159) di Blynk.Console yang mencatat status pembaruan aktif (*Live / Finished*) dengan versi firmware tujuan `1.0.1`.
6. `upload_ota_100_20261019.txt`: Rekaman log instalasi firmware baseline versi 1.0.0 melalui kabel USB COM5 menggunakan `arduino-cli`.
7. `ota_shipping_log_20261020.txt`: Rekaman telemetri dan log serial UART selama proses OTA berlangsung secara nirkabel, mencatat waktu penerimaan sinyal OTA, unduhan biner (17,56 detik), verifikasi MD5, *software reset*, hingga *bootloader* menjalankan firmware 1.0.1 pada partisi baru dengan motor tetap OFF aman.
