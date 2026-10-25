#!/usr/bin/env python3
"""
Logger Pasif Serial untuk Modul 03 Blynk iMCLab.
Hanya membaca (read-only) data serial dari ESP32 tanpa mengirim perintah motor apa pun.
Mencatat timestamp pada setiap baris dan menyimpan output ke file log sekaligus menampilkannya di terminal.
"""

import argparse
import datetime
import os
import sys
import time
import serial

def main():
    parser = argparse.ArgumentParser(description="Logger Pasif Serial Modul 03 Blynk iMCLab (Read-Only)")
    parser.add_argument("--port", default="COM5", help="Port serial ESP32 (default: COM5)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (default: 115200)")
    parser.add_argument("--output", default=None, help="File tujuan log (opsional)")
    parser.add_argument("--duration", type=float, default=None, help="Durasi perekaman dalam detik (opsional)")
    args = parser.parse_args()

    # Tentukan path file output default jika tidak diberikan
    if not args.output:
        now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        os.makedirs(out_dir, exist_ok=True)
        args.output = os.path.join(out_dir, f"serial_blynk_{now_str}.log")

    print("=" * 60)
    print("  iMCLab Modul 03 - Logger Pasif Serial (Read-Only)")
    print(f"  Port: {args.port} | Baud: {args.baud}")
    print(f"  Simpan log ke: {args.output}")
    print("  Tekan Ctrl+C untuk berhenti.")
    print("=" * 60)

    try:
        ser = serial.Serial(args.port, args.baud, timeout=1.0)
    except Exception as e:
        print(f"\n[ERROR] Gagal membuka port {args.port}: {e}", file=sys.stderr)
        print("Pastikan Serial Monitor di Arduino IDE atau aplikasi lain sudah ditutup.", file=sys.stderr)
        sys.exit(1)

    with open(args.output, "a", encoding="utf-8") as f_out:
        header = f"# Log Pasif Serial iMCLab Blynk - Mulai: {datetime.datetime.now().isoformat()}\n"
        f_out.write(header)
        f_out.flush()

        start_time = time.time()
        try:
            while True:
                if args.duration and (time.time() - start_time) >= args.duration:
                    print(f"\n[INFO] Durasi {args.duration} detik tercapai.")
                    break
                line_bytes = ser.readline()
                if not line_bytes:
                    continue
                try:
                    line_str = line_bytes.decode("utf-8", errors="replace").strip("\r\n")
                except Exception:
                    line_str = str(line_bytes)

                if line_str:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                    formatted = f"[{now}] {line_str}"
                    print(formatted, flush=True)
                    f_out.write(formatted + "\n")
                    f_out.flush()
        except KeyboardInterrupt:
            print("\n[INFO] Logger dihentikan oleh pengguna (Ctrl+C).")
        finally:
            ser.close()
            footer = f"# Selesai: {datetime.datetime.now().isoformat()}\n"
            with open(args.output, "a", encoding="utf-8") as f_end:
                f_end.write(footer)
            print(f"[INFO] Log tersimpan di: {args.output}")

if __name__ == "__main__":
    main()
