"""Olah log nyata Modul 01; tidak membuka port atau menjalankan motor.

CSV hanya berisi DATA. ACK/STATUS tidak dihitung sebagai sampel baru.
Grafik memakai laju pulsa agar tidak bergantung pada kalibrasi PPR.
"""
from __future__ import annotations

import csv
from datetime import datetime
import json
from pathlib import Path
import re
from statistics import mean, stdev

from reportlab.graphics import renderSVG
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing, Line, String
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib import colors

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / 'UTS/01_Basic_iMCLab'
DATA = MODULE / 'data'
PPR_ASSUMED = 2
SAMPLE_RE = re.compile(r'^RX DATA PWM=(\d+) SET=(\d+) RPM=([\d.]+) PULSES=(\d+) DT_MS=(\d+)$')


def read_log(path):
    events, samples = [], []
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        stamp, message = line.split(' ', 1)
        when = datetime.fromisoformat(stamp)
        events.append((when, message))
        match = SAMPLE_RE.fullmatch(message)
        if not match:
            continue
        pwm, target, rpm, pulses, dt = match.groups()
        sample = dict(source=path.name, timestamp_wib=stamp, pwm=int(pwm),
                      setpoint=int(target), rpm_reported=float(rpm),
                      pulses=int(pulses), dt_ms=int(dt))
        if sample['dt_ms'] <= 0:
            raise ValueError(f'Invalid sample interval: {path.name}: {line}')
        sample['pulse_hz'] = sample['pulses'] * 1000 / sample['dt_ms']
        if abs(sample['rpm_reported'] - sample['pulse_hz'] * 60 / PPR_ASSUMED) > .06:
            raise ValueError(f'RPM/PPR mismatch in {path.name}')
        samples.append(sample)
    on = next((t for t, m in events if m == 'TX 1'), None)
    off = next((t for t, m in events if m == 'TX 0' and on and t > on), None)
    active = [s for s in samples if s['pwm'] > 0]
    summary = dict(source=path.name, data_samples=len(samples), active_samples=len(active),
                   on_duration_s=round((off-on).total_seconds(), 6) if on and off else None,
                   active_peak_pulses=max((s['pulses'] for s in active), default=None),
                   active_last_rpm=active[-1]['rpm_reported'] if active else None,
                   early_stop=any(m.startswith('EARLY STOP') for _, m in events))
    return events, samples, summary


def sweep_stats(events, samples):
    on = next(t for t, m in events if m == 'TX 1')
    off = next(t for t, m in events if m == 'TX 0' and t > on)
    changes = [(on, 200)] + [(t, int(m.split(':')[1])) for t, m in events
                             if t > on and m.startswith('TX PWM:')] + [(off, 0)]
    result = []
    for (start, pwm), (end, _) in zip(changes, changes[1:]):
        complete = any(m == f'PHASE COMPLETE PWM={pwm}' for _, m in events)
        phase = [s for s in samples if s['pwm'] == pwm
                 and start <= datetime.fromisoformat(s['timestamp_wib']) < end]
        # Seluruh jendela sampel harus melewati 5 detik pertama fase.
        candidates = [s for s in phase if (datetime.fromisoformat(s['timestamp_wib']) - start).total_seconds()
                      >= 5 + s['dt_ms'] / 1000]
        tail = candidates[-5:]
        values = [s['pulse_hz'] for s in tail]
        average = mean(values) if values else 0
        spread_pct = (max(values)-min(values))/average*100 if average else None
        stable = complete and len(tail) == 5 and min(values) > 0 and spread_pct <= 5
        result.append(dict(pwm=pwm, duration_s=round((end-start).total_seconds(), 6),
                           completed=complete, data_samples=len(phase), stable=stable,
                           stable_n=5 if stable else 0,
                           selected_timestamps=[s['timestamp_wib'] for s in tail] if stable else [],
                           mean_pulse_hz=round(average, 4) if stable else None,
                           sample_sd_pulse_hz=round(stdev(values), 4) if stable else None,
                           range_percent=round(spread_pct, 4) if stable else None,
                           mean_rpm_assumed_ppr2=round(average*30, 2) if stable else None,
                           active_last_pulses=phase[-1]['pulses'] if phase else None))
    return on, changes, result


def plot_sweep(on, changes, samples):
    relevant = [s for s in samples if datetime.fromisoformat(s['timestamp_wib']) >= on]
    points = [((datetime.fromisoformat(s['timestamp_wib'])-on).total_seconds(), s['pulse_hz'])
              for s in relevant]
    end = points[-1][0]
    steps = [(0, 200)]
    for t, value in changes[1:]:
        x = (t-on).total_seconds()
        steps.extend([(x, steps[-1][1]), (x, value)])
    steps.append((end, 0))
    drawing = Drawing(720, 400)
    navy = colors.HexColor('#183047')
    muted = colors.HexColor('#566675')
    blue = colors.HexColor('#245aa6')
    teal = colors.HexColor('#087d82')
    drawing.add(String(14, 378, 'Respons ketika PWM diturunkan saat motor berjalan',
                       fontName='Helvetica-Bold', fontSize=16, fillColor=navy))
    drawing.add(String(14, 357, '19 Oktober 2026 | USB serial, 115200 baud | DATA asli, interval sekitar 1 detik',
                       fontName='Helvetica', fontSize=10, fillColor=muted))

    def lineplot(data, y, height, maximum, tick, color, symbol=False):
        chart = LinePlot()
        chart.x, chart.y, chart.width, chart.height = 68, y, 624, height
        chart.data = [data]
        chart.xValueAxis.valueMin, chart.xValueAxis.valueMax = 0, 45
        chart.xValueAxis.valueStep = 5
        chart.yValueAxis.valueMin, chart.yValueAxis.valueMax = 0, maximum
        chart.yValueAxis.valueStep = tick
        for axis in (chart.xValueAxis, chart.yValueAxis):
            axis.labels.fontName = 'Helvetica'
            axis.labels.fontSize = 10
            axis.strokeColor = muted
        chart.lines[0].strokeColor = color
        chart.lines[0].strokeWidth = 1.7
        if symbol:
            chart.lines[0].symbol = makeMarker('FilledCircle')
            chart.lines[0].symbol.size = 3
            chart.lines[0].symbol.fillColor = color
        drawing.add(chart)
        return chart

    lineplot(steps, 264, 62, 240, 80, blue)
    drawing.add(String(14, 337, 'PWM (0-255)', fontName='Helvetica', fontSize=10, fillColor=blue))
    for index, (start, pwm) in enumerate(changes):
        left = (start-on).total_seconds()
        right = (changes[index+1][0]-on).total_seconds() if index+1 < len(changes) else end
        midpoint = 68 + ((left+right)/2)/45*624
        drawing.add(String(midpoint, 264 + pwm/240*62 + 10,
                           'OFF' if pwm == 0 else str(pwm), textAnchor='middle',
                           fontName='Helvetica', fontSize=10, fillColor=blue))
    lineplot(points, 66, 150, 300, 50, teal, True)
    drawing.add(String(14, 229, 'Pulsa per detik', fontName='Helvetica', fontSize=10, fillColor=teal))
    for t, value in changes[1:]:
        x = 68 + (t-on).total_seconds()/45*624
        drawing.add(Line(x, 66, x, 216, strokeColor=colors.HexColor('#bdc9d6'),
                         strokeWidth=.7, strokeDashArray=[3, 3]))
    drawing.add(String(380, 29, 'Waktu sejak perintah ON (detik, timestamp komputer)',
                       textAnchor='middle', fontName='Helvetica', fontSize=11, fillColor=navy))
    drawing.add(String(14, 8, 'Garis menghubungkan sampel; tahap 80 dilewati setelah penghentian pada PWM 120.',
                       fontName='Helvetica', fontSize=9, fillColor=muted))
    target = MODULE/'gambar/hasil_variasi.svg'
    renderSVG.drawToFile(drawing, str(target))
    # ReportLab dapat menulis None sebagai warna CSS; normalkan untuk svglib.
    target.write_text(target.read_text(encoding='utf-8').replace('fill: None;', 'fill: none;'), encoding='utf-8')


def main():
    logs, all_samples, runs = {}, [], []
    for path in sorted(DATA.glob('*.log')):
        events, samples, summary = read_log(path)
        logs[path.name] = (events, samples)
        all_samples.extend(samples)
        runs.append(summary)
    all_samples.sort(key=lambda s: s['timestamp_wib'])
    with (DATA/'sampel_serial.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_samples[0]))
        writer.writeheader()
        writer.writerows(all_samples)
    sweep_file = 'basic_variasi-berjalan_20261019_012135.log'
    on, changes, phases = sweep_stats(*logs[sweep_file])
    result = dict(ppr_assumed=PPR_ASSUMED, rpm_calibrated=False, raw_log_count=len(logs),
                  data_sample_count=len(all_samples), runs=runs, sweep_source=sweep_file,
                  selection='Last 5 full DATA windows after 5 seconds settling; completed phase; positive pulses; range/mean <=5%. Descriptive rule chosen during analysis.',
                  phases=phases)
    (DATA/'hasil_analisis.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    plot_sweep(on, changes, logs[sweep_file][1])
    lines = ['# Indeks log dan ringkasan otomatis', '',
             'Dibuat oleh `UTS/tools/analisis_basic.py`. Log mentah tidak diubah. RPM memakai asumsi PPR=2.', '',
             '| Log | Durasi ON (s) | DATA aktif | Pulsa maksimum per jendela saat aktif | Penghentian dini |',
             '| --- | --- | --- | --- | --- |']
    for run in runs:
        duration = f"{run['on_duration_s']:.3f}" if run['on_duration_s'] is not None else '-'
        peak = str(run['active_peak_pulses']) if run['active_peak_pulses'] is not None else '-'
        filename = run['source']
        lines.append(f"| [{filename}]({filename}) | {duration} | {run['active_samples']} | {peak} | {'Ya' if run['early_stop'] else 'Tidak'} |")
    lines += ['', 'Durasi menggunakan jarak timestamp TX ON sampai TX OFF pada komputer; bukan pengukuran waktu gerak mekanis.',
              'DATA aktif dipilih dari PWM yang dilaporkan firmware. Sampel pertama setelah perubahan dapat meliputi kondisi sebelumnya.',
              'ACK/STATUS tidak masuk jumlah sampel. Laju pulsa dihitung memakai DT_MS, bukan menganggap interval selalu tepat satu detik.', '']
    (DATA/'ringkasan_log.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(dict(logs=len(logs), samples=len(all_samples), phases=phases), indent=2))


if __name__ == '__main__':
    main()
