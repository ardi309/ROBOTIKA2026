#!/usr/bin/env python3
"""
Logger Serial Pasif untuk Modul 04 OTA Blynk.Air iMCLab.
Merekam proses transisi OTA (URL download, status flash, reboot MCU, hingga startup versi 1.0.1).
"""

import argparse
import datetime
import os
import sys
import time
import serial

def main():
    parser = argparse.ArgumentParser(description="Logger Serial Modul 04 OTA Blynk.Air")
    parser.add_argument("--port", default="COM5", help="Port serial ESP32 (default: COM5)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--output", default=None, help="File tujuan log")
    parser.add_argument("--duration", type=float, default=3600.0, help="Durasi perekaman dalam detik (default: 3600s)")
    args = parser.parse_args()

    if not args.output:
        out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bukti"))
        os.makedirs(out_dir, exist_ok=True)
        args.output = os.path.join(out_dir, "ota_shipping_log_20261020.txt")

    print("=" * 60)
    print("  iMCLab Modul 04 - Logger Serial OTA Blynk.Air")
    print(f"  Port: {args.port} | Baud: {args.baud}")
    print(f"  Simpan log ke: {args.output}")
    print(f"  Batas durasi: {args.duration} detik")
    print("=" * 60)

    try:
        ser = serial.Serial(args.port, args.baud, timeout=0.5)
    except Exception as e:
        print(f"\n[ERROR] Gagal membuka port {args.port}: {e}", file=sys.stderr)
        sys.exit(1)

    start_time = time.time()
    last_idle_time = 0.0
    with open(args.output, "a", encoding="utf-8") as f_out:
        header = f"\n=== Log Serial OTA iMCLab - Mulai: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n"
        f_out.write(header)
        f_out.flush()
        print(header.strip())

        try:
            while True:
                if args.duration and (time.time() - start_time) > args.duration:
                    print(f"\n[INFO] Batas waktu perekaman ({args.duration}s) tercapai.")
                    break

                try:
                    line = ser.readline().decode("utf-8", errors="replace").strip()
                except Exception as read_err:
                    time.sleep(0.1)
                    continue

                if line:
                    now = time.time()
                    # Throttling status idle agar file log tidak penuh dengan baris identik
                    is_idle_data = line.startswith("DATA PWM=0 SET=200 RPM=0.0")
                    if is_idle_data:
                        if (now - last_idle_time) < 15.0:
                            continue
                        last_idle_time = now

                    ts = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    formatted = f"[{ts}] {line}"
                    print(formatted)
                    f_out.write(formatted + "\n")
                    f_out.flush()

        except KeyboardInterrupt:
            print("\n[INFO] Perekaman dihentikan pengguna.")
        finally:
            ser.close()
            footer = f"=== Log Serial OTA Selesai: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n"
            f_out.write(footer)
            f_out.flush()
            print(footer.strip())

if __name__ == "__main__":
    main()
