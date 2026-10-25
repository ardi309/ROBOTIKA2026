# Indeks log dan ringkasan otomatis

Dibuat oleh `UTS/tools/analisis_basic.py`. Log mentah tidak diubah. RPM memakai asumsi PPR=2.

| Log | Durasi ON (s) | DATA aktif | Pulsa maksimum per jendela saat aktif | Penghentian dini |
| --- | --- | --- | --- | --- |
| [basic_perintah_20261019_012248.log](basic_perintah_20261019_012248.log) | - | 0 | - | Tidak |
| [basic_variasi-berjalan_20261019_012135.log](basic_variasi-berjalan_20261019_012135.log) | 41.025 | 41 | 283 | Ya |
| [motor_pwm120_20261019_005007.log](motor_pwm120_20261019_005007.log) | 5.068 | 5 | 0 | Tidak |
| [motor_pwm120_20261019_005754.log](motor_pwm120_20261019_005754.log) | 3.110 | 3 | 0 | Ya |
| [motor_pwm160_20261019_005801.log](motor_pwm160_20261019_005801.log) | 3.134 | 3 | 0 | Ya |
| [motor_pwm200_20261019_005512.log](motor_pwm200_20261019_005512.log) | 2.150 | 2 | 199 | Tidak |
| [motor_pwm200_20261019_005723.log](motor_pwm200_20261019_005723.log) | 5.167 | 5 | 259 | Tidak |
| [motor_pwm200_20261019_005731.log](motor_pwm200_20261019_005731.log) | 5.067 | 6 | 259 | Tidak |
| [motor_pwm200_20261019_005740.log](motor_pwm200_20261019_005740.log) | 5.091 | 5 | 274 | Tidak |
| [motor_pwm200_20261019_005807.log](motor_pwm200_20261019_005807.log) | 3.091 | 4 | 0 | Ya |
| [motor_pwm200_20261019_010055.log](motor_pwm200_20261019_010055.log) | 3.198 | 3 | 0 | Ya |
| [motor_pwm200_20261019_011923.log](motor_pwm200_20261019_011923.log) | 2.024 | 2 | 84 | Tidak |
| [motor_pwm80_20261019_005748.log](motor_pwm80_20261019_005748.log) | 3.109 | 3 | 0 | Ya |
| [usb_motor_off_20261018_213758.log](usb_motor_off_20261018_213758.log) | - | 0 | - | Tidak |

Durasi menggunakan jarak timestamp TX ON sampai TX OFF pada komputer; bukan pengukuran waktu gerak mekanis.
DATA aktif dipilih dari PWM yang dilaporkan firmware. Sampel pertama setelah perubahan dapat meliputi kondisi sebelumnya.
ACK/STATUS tidak masuk jumlah sampel. Laju pulsa dihitung memakai DT_MS, bukan menganggap interval selalu tepat satu detik.
