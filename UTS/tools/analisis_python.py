"""Analisis CSV asli Modul 02, tanpa membuka port atau menjalankan motor."""
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
MODULE = ROOT / 'UTS/02_Python_iMCLab'
DATA = MODULE / 'data'
SWEEP = 'python_sweep_20261019_061241.csv'
PATTERN = re.compile(r'^DATA PWM=(\d+) SET=(\d+) RPM=([\d.]+) PULSES=(\d+) DT_MS=(\d+)$')


def read_log(path):
    with path.open(encoding='utf-8', newline='') as handle:
        events = list(csv.DictReader(handle))
    samples = []
    for row in events:
        values = PATTERN.fullmatch(row['raw']) if row['direction'] == 'RX' else None
        if not values:
            continue
        if tuple(row[k] for k in ('pwm', 'set_pwm', 'rpm', 'pulses', 'dt_ms')) != values.groups():
            raise ValueError(f'Kolom CSV tidak sesuai raw: {path.name}')
        pwm, target, rpm, pulses, dt = values.groups()
        if int(dt) <= 0:
            raise ValueError(f'Interval DATA tidak valid: {path.name}')
        hz = int(pulses) * 1000 / int(dt)
        if abs(float(rpm) - hz * 30) > .06:
            raise ValueError(f'RPM tidak sesuai PPR=2: {path.name}')
        samples.append(dict(source=path.name, timestamp=row['timestamp'], pwm=int(pwm),
                            setpoint=int(target), rpm_reported=float(rpm), pulses=int(pulses),
                            dt_ms=int(dt), pulse_hz=hz))
    return events, samples


def when(row):
    return datetime.fromisoformat(row['timestamp'])


def phases_from(events, samples):
    on = next(when(r) for r in events if r['direction'] == 'TX' and r['raw'] == '1')
    off = next(when(r) for r in events if r['direction'] == 'TX' and r['raw'] == '0' and when(r) > on)
    changes = [(on, 200)] + [(when(r), int(r['raw'].split(':')[1])) for r in events
                            if r['direction'] == 'TX' and r['raw'].startswith('PWM:') and on < when(r) < off]
    changes.append((off, 0))
    phases = []
    for (start, pwm), (end, _) in zip(changes, changes[1:]):
        phase = [s for s in samples if s['pwm'] == pwm and start <= when(s) < end]
        selected = [s for s in phase if (when(s)-start).total_seconds() >= 5 + s['dt_ms']/1000][-5:]
        values = [s['pulse_hz'] for s in selected]
        avg = mean(values) if values else None
        spread = (max(values)-min(values))/avg*100 if avg else None
        # Program maju ke fase berikutnya/OFF normal hanya setelah timer
        # monotonic selesai. Timestamp kalender bukan timer itu; jangan
        # membatalkan fase hanya karena selisih jam komputer sedikit <15 s.
        complete = not any(r['direction'] == 'EVENT' and
                           r['raw'].startswith(('ERROR ', 'INTERRUPTED')) and
                           start <= when(r) < end for r in events)
        stable = complete and len(selected) == 5 and min(values) > 0 and spread <= 5
        phases.append(dict(pwm=pwm, duration_s=round((end-start).total_seconds(), 6),
                           completed=complete, data_samples=len(phase), tail_n=len(selected),
                           tail_mean_pulse_hz=round(avg, 4) if avg is not None else None,
                           tail_sd_pulse_hz=round(stdev(values), 4) if len(values) > 1 else None,
                           tail_range_percent=round(spread, 4) if spread is not None else None,
                           tail_min_pulse_hz=min(values) if values else None,
                           tail_max_pulse_hz=max(values) if values else None,
                           stable=stable,
                           tail_rpm_assumed_ppr2=round(avg*30, 2) if avg is not None else None,
                           selected_timestamps=[s['timestamp'] for s in selected]))
    return on, changes, phases


def plot(on, changes, samples):
    points = [((when(s)-on).total_seconds(), s['pulse_hz']) for s in samples if when(s) >= on]
    end = points[-1][0]
    steps = [(0, 200)]
    for stamp, pwm in changes[1:]:
        elapsed = (stamp-on).total_seconds()
        steps.extend([(elapsed, steps[-1][1]), (elapsed, pwm)])
    steps.append((end, 0))
    drawing = Drawing(720, 400)
    navy, muted, blue, teal = [colors.HexColor(s) for s in ('#183047', '#566675', '#245aa6', '#087d82')]
    drawing.add(String(14, 378, 'Kendali Python: respons PWM 200, 160, dan 120',
                       fontName='Helvetica-Bold', fontSize=16, fillColor=navy))
    drawing.add(String(14, 357, '19 Oktober 2026, 06:12 WIB | COM5, 115200 baud | hanya baris DATA asli',
                       fontName='Helvetica', fontSize=10, fillColor=muted))

    def add_chart(values, y, height, maximum, tick, color, markers=False):
        chart = LinePlot()
        chart.x, chart.y, chart.width, chart.height = 68, y, 624, height
        chart.data = [values]
        chart.xValueAxis.valueMin, chart.xValueAxis.valueMax, chart.xValueAxis.valueStep = 0, 50, 5
        chart.yValueAxis.valueMin, chart.yValueAxis.valueMax, chart.yValueAxis.valueStep = 0, maximum, tick
        for axis in (chart.xValueAxis, chart.yValueAxis):
            axis.labels.fontName, axis.labels.fontSize, axis.strokeColor = 'Helvetica', 10, muted
        chart.lines[0].strokeColor, chart.lines[0].strokeWidth = color, 1.7
        if markers:
            chart.lines[0].symbol = makeMarker('FilledCircle')
            chart.lines[0].symbol.size, chart.lines[0].symbol.fillColor = 3, color
        drawing.add(chart)

    add_chart(steps, 264, 62, 240, 80, blue)
    drawing.add(String(14, 337, 'PWM (0-255)', fontName='Helvetica', fontSize=10, fillColor=blue))
    for index, (stamp, pwm) in enumerate(changes):
        left = (stamp-on).total_seconds()
        right = (changes[index+1][0]-on).total_seconds() if index+1 < len(changes) else end
        drawing.add(String(68+(left+right)/2/50*624, 264+pwm/240*62+10,
                           str(pwm) if pwm else 'OFF', textAnchor='middle', fontName='Helvetica',
                           fontSize=10, fillColor=blue))
    add_chart(points, 66, 150, 300, 50, teal, True)
    drawing.add(String(14, 229, 'Pulsa per detik', fontName='Helvetica', fontSize=10, fillColor=teal))
    for stamp, _ in changes[1:]:
        x = 68+(stamp-on).total_seconds()/50*624
        drawing.add(Line(x, 66, x, 216, strokeColor=colors.HexColor('#bdc9d6'),
                         strokeWidth=.7, strokeDashArray=[3, 3]))
    drawing.add(String(380, 29, 'Waktu sejak perintah ON (detik, timestamp komputer)',
                       textAnchor='middle', fontName='Helvetica', fontSize=11, fillColor=navy))
    drawing.add(String(14, 8, 'Garis menghubungkan sampel; setiap tahap berlangsung sekitar 15 detik, diikuti OFF.',
                       fontName='Helvetica', fontSize=9, fillColor=muted))
    path = MODULE/'gambar/hasil_python.svg'
    renderSVG.drawToFile(drawing, str(path))
    path.write_text(path.read_text(encoding='utf-8').replace('fill: None;', 'fill: none;'), encoding='utf-8')


def main():
    raw, all_samples, runs = {}, [], []
    for path in sorted(DATA.glob('python_*.csv')):
        events, samples = read_log(path)
        raw[path.name] = (events, samples)
        all_samples.extend(samples)
        on = next((when(r) for r in events if r['direction'] == 'TX' and r['raw'] == '1'), None)
        off = next((when(r) for r in events if r['direction'] == 'TX' and r['raw'] == '0' and on and when(r) > on), None)
        runs.append(dict(source=path.name, data_samples=len(samples),
                         active_samples=sum(s['pwm'] > 0 for s in samples),
                         on_duration_s=round((off-on).total_seconds(), 6) if on and off else None,
                         errors=[r['raw'] for r in events if r['direction'] == 'EVENT' and r['raw'].startswith('ERROR')]))
    all_samples.sort(key=when)
    with (DATA/'sampel_serial.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(all_samples[0]))
        writer.writeheader()
        writer.writerows(all_samples)
    on, changes, phases = phases_from(*raw[SWEEP])
    baseline = json.loads((ROOT/'UTS/01_Basic_iMCLab/data/hasil_analisis.json').read_text(encoding='utf-8'))
    comparisons = []
    for phase in phases:
        basic = next(p for p in baseline['phases'] if p['pwm'] == phase['pwm'])
        if basic['stable'] and phase['stable']:
            comparisons.append(dict(pwm=phase['pwm'], basic_hz=basic['mean_pulse_hz'],
                                    python_hz=phase['tail_mean_pulse_hz'],
                                    difference_percent=round((phase['tail_mean_pulse_hz']/basic['mean_pulse_hz']-1)*100, 4)))
    result = dict(ppr_assumed=2, rpm_calibrated=False, raw_log_count=len(raw),
                  data_sample_count=len(all_samples), runs=runs, sweep_source=SWEEP, phases=phases,
                  selection='Last 5 full DATA windows after 5 seconds settling; completed 15 s phase; positive pulses; range/mean <=5%. Same descriptive criterion as Module 01. Nonqualifying tails are explicitly labelled not stable.',
                  comparisons=comparisons)
    (DATA/'hasil_analisis.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    plot(on, changes, raw[SWEEP][1])
    lines = ['# Indeks data asli Modul 02', '',
             'Dibuat oleh `UTS/tools/analisis_python.py`. Berkas python_*.csv adalah log asli; sampel_serial.csv hanya turunan baris DATA.', '',
             '| Log | DATA | DATA dengan PWM > 0 | Durasi TX ON-OFF (s) |', '| --- | --- | --- | --- |']
    for run in runs:
        duration = str(run['on_duration_s']) if run['on_duration_s'] is not None else '-'
        lines.append(f"| [{run['source']}]({run['source']}) | {run['data_samples']} | {run['active_samples']} | {duration} |")
    lines += ['', 'Durasi berasal dari waktu komputer; bukan pengukuran langsung lama gerak mekanis. ACK/STATUS tidak dihitung sebagai sampel baru.',
              'Dua baris DATA pada uji OFF pertama berisi satu pulsa. Angka dipertahankan; penyebab belum diketahui.', '']
    (DATA/'ringkasan_log.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
