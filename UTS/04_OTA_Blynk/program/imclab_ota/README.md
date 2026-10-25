# Program OTA dan asal dependensi

Buka `imclab_ota.ino` dari folder ini. Seluruh `.h` harus tetap berada bersama sketch. Pasang library Blynk 1.3.2; baseline core ESP32 adalah 2.0.17.

- Salin `template_config.example.h` menjadi `template_config.h`, lalu isi template sendiri.
- `BlynkEdgent.h`, `BlynkState.h`, `ConfigMode.h`, `ConfigStore.h`, `Console.h`, `Indicator.h`, `OTA.h`, dan `ResetButton.h` serta `Settings.h` berasal dari contoh Edgent_ESP32 v1.3.2.
- URL dan SHA-256 upstream sebelum adaptasi dicatat di `upstream.json`; lisensi asli ada di `LICENSE.Blynk`.
- Adaptasi `OTA.h`: memanggil hook `IMCLAB_BEFORE_OTA` sebelum menjadwalkan update.
- Adaptasi `BlynkEdgent.h`: hook `IMCLAB_LEAVE_RUNNING` saat masuk state selain MODE_RUNNING.
- `ImcCore.h` adalah kode motor paket UTS, sama dengan Modul 01/03.
- `USE_ESP32_DEV_MODULE` tidak mengalokasikan LED indikator Edgent, sehingga GPIO2 dipakai indikator motor. Warning LED Edgent tidak dikonfigurasi memang diharapkan.

Konsol serial dikelola Edgent, sehingga perintah motor Modul 01 tidak tersedia pada sketch OTA. Gunakan widget V2/V3. Jangan mengetik perintah reset konfigurasi di konsol tanpa memahami akibatnya. Token/Wi-Fi disimpan melalui provisioning; tidak menambahkan BLYNK_AUTH_TOKEN ke sketch.

Hasil kompilasi dan batas verifikasi terdapat di [VERIFIKASI.md](../../../VERIFIKASI.md). Tata cara demo dan pemilihan binary terdapat di [PANDUAN_PRAKTIK.md](../../../PANDUAN_PRAKTIK.md).
