"""Ekspor empat LAPORAN.md ke PDF beserta diagram vektor.

Jalankan dari root: python UTS/tools/buat_pdf.py
Dependensi: reportlab, svglib. Font Calibri di Windows, DejaVu Sans di Linux.
PDF disimpan di output/pdf/ dan disalin sebagai LAPORAN.pdf pada setiap modul.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL_DEPS = ROOT / '.tools/pdf-python'
if LOCAL_DEPS.exists():
    # Utamakan paket yang cocok dengan runtime; direktori lokal juga memuat
    # paket biner dari Python lain dan hanya dipakai sebagai fallback.
    sys.path.append(str(LOCAL_DEPS))

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, Image, PageBreak,
)
from svglib.svglib import svg2rlg

OUTPUT = ROOT / 'output/pdf'
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 18 * mm
CONTENT_WIDTH = PAGE_WIDTH - MARGIN * 2
NAVY = colors.HexColor('#183047')
BLUE = colors.HexColor('#245aa6')
TEAL = colors.HexColor('#087d82')
MUTED = colors.HexColor('#566675')
LIGHT = colors.HexColor('#edf3f8')


def fonts():
    windows = Path('C:/Windows/Fonts')
    if (windows / 'calibri.ttf').exists():
        paths = [windows / name for name in ('calibri.ttf', 'calibrib.ttf', 'calibrii.ttf', 'calibriz.ttf')]
        mono = windows / 'consola.ttf'
    else:
        linux = Path('/usr/share/fonts/truetype/dejavu')
        paths = [linux / name for name in ('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf',
                                          'DejaVuSans-Oblique.ttf', 'DejaVuSans-BoldOblique.ttf')]
        mono = linux / 'DejaVuSansMono.ttf'
    for name, path in zip(('Report', 'Report-Bold', 'Report-Italic', 'Report-BoldItalic'), paths):
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily('Report', normal='Report', bold='Report-Bold',
                                 italic='Report-Italic', boldItalic='Report-BoldItalic')
    pdfmetrics.registerFont(TTFont('Mono', str(mono)))


fonts()
STYLES = {
    'title': ParagraphStyle('Title', fontName='Report-Bold', fontSize=24, leading=28,
                            textColor=NAVY, spaceAfter=10),
    'eyebrow': ParagraphStyle('Eyebrow', fontName='Report-Bold', fontSize=10, leading=14,
                              textColor=TEAL, spaceAfter=9),
    'h2': ParagraphStyle('Heading2', fontName='Report-Bold', fontSize=13, leading=17,
                         textColor=BLUE, spaceBefore=10, spaceAfter=6, keepWithNext=True),
    'body': ParagraphStyle('Body', fontName='Report', fontSize=10.25, leading=13.5,
                           textColor=NAVY, spaceAfter=6, alignment=TA_LEFT,
                           allowWidows=0, allowOrphans=0, splitLongWords=True),
    'small': ParagraphStyle('Small', fontName='Report', fontSize=9, leading=12,
                            textColor=MUTED, spaceAfter=6),
    'caption': ParagraphStyle('Caption', fontName='Report', fontSize=9, leading=12,
                              textColor=MUTED, spaceAfter=10),
    'cell': ParagraphStyle('Cell', fontName='Report', fontSize=9, leading=12,
                           textColor=NAVY, wordWrap='CJK'),
    'cellhead': ParagraphStyle('CellHead', fontName='Report-Bold', fontSize=9, leading=12,
                               textColor=colors.white),
    'code': ParagraphStyle('Code', fontName='Mono', fontSize=8, leading=11,
                           backColor=LIGHT, borderPadding=8, spaceAfter=8),
    'list': ParagraphStyle('List', fontName='Report', fontSize=10.25, leading=13.5,
                           textColor=NAVY, leftIndent=17, firstLineIndent=0,
                           bulletIndent=0, spaceAfter=4, allowWidows=0, allowOrphans=0),
}

BIBLIOGRAPHY = {
    '01': [
        'Rahmat, B., dan Muljono. (2024). *Pemrograman Internet of Things (IoT) dengan Arduino dan Python, Jilid 1*. Eureka Media Aksara. Bab 3, halaman PDF 60-65.',
        'Materi kelas Robotika: `on_off_Motor.ino`, `imclab_naik_turun.ino`, dan `imclab_Blynk_kelas.ino`. Berkas diberikan dosen dalam folder materi.',
    ],
    '02': [
        'Rahmat, B., dan Muljono. (2024). *Pemrograman Internet of Things (IoT) dengan Arduino dan Python, Jilid 1*. Eureka Media Aksara. Bagian Arduino-Python, halaman PDF 66-79.',
        'Materi kelas: `Test_Port_Serial.ipynb`, `Tes_IMCLab_pilih_port_otomatis.ipynb`, dan `Tes_IMCLab_naik_turun.ipynb`.',
        'pySerial. *API documentation*. https://pyserial.readthedocs.io/en/latest/pyserial_api.html (diakses 19 Oktober 2026).',
    ],
    '03': [
        'Rahmat, B. *Integrasi AI dan IoT pada Sistem Kendali Cerdas*. Slide materi kelas, slide 4-5 dan 17.',
        'Materi kelas Robotika: `imclab_Blynk_kelas.ino`. Pemetaan V0-V3, GPIO, sensor, dan PWM diadaptasi untuk paket UTS ini.',
    ],
    '04': [
        'Blynk. *OTA: Firmware Over-The-Air updates*. https://docs.blynk.io/en/blynk.edgent/updating-devices-firmwares-ota (diakses 18 Oktober 2026).',
        'Blynk. *Over-The-Air Firmware Updates API*. https://docs.blynk.io/en/blynk-library-firmware-api/ota-updates (diakses 18 Oktober 2026).',
        'Blynk Technologies. *Edgent_ESP32*, tag v1.3.2, repositori blynk-library di GitHub. Header upstream, lisensi MIT, dan catatan adaptasi disertakan dalam folder program/imclab_ota.',
    ],
}


def inline(value: str, directory: Path) -> str:
    value = value.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', '-')
    # Protect markup we produce from subsequent plain-text escaping.
    tokens = []

    def token(markup):
        tokens.append(markup)
        return f'ZZTOKEN{len(tokens)-1}ZZ'

    def code(match):
        return token('<font name="Mono" size="9">' + html.escape(match[1]) + '</font>')

    value = re.sub(r'`([^`]+)`', code, value)

    def link(match):
        label, target = match.groups()
        label = html.escape(label)
        if target.startswith(('https://', 'http://')):
            return token(f'<link href="{html.escape(target, quote=True)}" color="#245aa6">{label}</link>')
        target_path = (directory / target).resolve()
        try:
            relative = target_path.relative_to(ROOT)
        except ValueError:
            relative = Path(target)
        # Printed PDFs keep readable repository paths instead of host-only links.
        return token(f'<font color="#245aa6">{label}</font> '
                     f'<font size="8" color="#566675">({html.escape(relative.as_posix())})</font>')

    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, value)
    value = html.escape(value)
    value = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', value)
    value = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', value)
    for i in range(len(tokens)-1, -1, -1):
        value = value.replace(f'ZZTOKEN{i}ZZ', tokens[i])
    return value


def paragraph(value, directory, style='body', **kwargs):
    return Paragraph(inline(value, directory), STYLES[style], **kwargs)


def table(lines, directory):
    rows = []
    for line in lines:
        cells = [part.strip() for part in line.strip().strip('|').split('|')]
        if all(re.fullmatch(r':?-+:?', cell) for cell in cells):
            continue
        rows.append(cells)
    columns = len(rows[0])
    if columns == 2:
        widths = [CONTENT_WIDTH * .43, CONTENT_WIDTH * .57]
    elif columns == 5 and rows[0][0] == 'PWM':
        widths = [CONTENT_WIDTH * x for x in (.09, .23, .27, .25, .16)]
    elif columns == 5:
        widths = [CONTENT_WIDTH * x for x in (.28, .15, .18, .19, .20)]
    elif columns == 6:
        widths = [CONTENT_WIDTH * x for x in (.19, .14, .19, .16, .15, .17)]
    elif columns == 3:
        widths = [CONTENT_WIDTH * x for x in (.21, .25, .54)]
    else:
        widths = [CONTENT_WIDTH / columns] * columns
    content = [[paragraph(cell or ' ', directory, 'cellhead' if index == 0 else 'cell')
                for cell in row] for index, row in enumerate(rows)]
    result = Table(content, colWidths=widths, repeatRows=1, hAlign='LEFT',
                   minRowHeights=[0] + [25] * (len(content)-1))
    result.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BLUE),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT]),
        ('LINEBELOW', (0,0), (-1,-1), .4, colors.HexColor('#d4dfeb')),
    ]))
    return result


def blocks(text, directory):
    lines = text.strip().splitlines()
    result, i = [], 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == '<!-- pagebreak -->':
            result.append(PageBreak())
            i += 1
        elif line.startswith('## '):
            result.append(paragraph(line[3:], directory, 'h2'))
            i += 1
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(lines[i]); i += 1
            result += [table(rows, directory), Spacer(1,8)]
        elif line.startswith('!['):
            match = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)', line)
            if not match:
                raise ValueError(f'Invalid image: {line}')
            image_path = directory / match[2]
            if image_path.suffix.lower() == '.svg':
                drawing = svg2rlg(str(image_path))
                scale = CONTENT_WIDTH / drawing.width
                drawing.scale(scale, scale)
                drawing.width *= scale
                drawing.height *= scale
            else:
                drawing = Image(str(image_path))
                scale = min(CONTENT_WIDTH / drawing.imageWidth, 310 / drawing.imageHeight)
                drawing.drawWidth = drawing.imageWidth * scale
                drawing.drawHeight = drawing.imageHeight * scale
            drawing.hAlign = 'CENTER'
            i += 1
            while i < len(lines) and not lines[i].strip(): i += 1
            group = [Spacer(1,4), drawing, Spacer(1,7)]
            if i < len(lines) and lines[i].startswith('**Gambar'):
                group.append(paragraph(lines[i], directory, 'caption'))
                i += 1
            result.append(KeepTogether(group))
        elif re.match(r'^(\d+\.|-) ', line):
            match = re.match(r'^(\d+\.|-) (.*)', line)
            marker = match[1] if match[1] != '-' else '\u2022'
            result.append(paragraph(match[2], directory, 'list', bulletText=marker))
            i += 1
        elif line.startswith('```'):
            i += 1; code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(html.escape(lines[i])); i += 1
            i += 1
            result.append(Paragraph('<br/>'.join(code), STYLES['code']))
        else:
            parts = [line]; i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(## |\||!\[|```|\d+\. |- |<!-- pagebreak -->)', lines[i].strip()):
                parts.append(lines[i].strip()); i += 1
            result.append(paragraph(' '.join(parts), directory))
    return result


def chrome(label, footer='DRAF - hasil eksperimen dan identitas belum dilengkapi'):
    def draw(canvas, document):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#d4dfeb'))
        canvas.line(MARGIN, PAGE_HEIGHT-17*mm, PAGE_WIDTH-MARGIN, PAGE_HEIGHT-17*mm)
        canvas.setFont('Report-Bold', 8)
        canvas.setFillColor(BLUE)
        canvas.drawString(MARGIN, PAGE_HEIGHT-13.5*mm, 'ROBOTIKA / UTS')
        canvas.setFont('Report',8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_WIDTH-MARGIN, PAGE_HEIGHT-13.5*mm, label)
        canvas.line(MARGIN, 17*mm, PAGE_WIDTH-MARGIN, 17*mm)
        canvas.drawString(MARGIN,12*mm,footer)
        canvas.drawRightString(PAGE_WIDTH-MARGIN,12*mm,f'{document.page}')
        canvas.restoreState()
    return draw


def build(module):
    source = module / 'LAPORAN.md'
    markdown = source.read_text(encoding='utf-8')
    title = markdown.splitlines()[0].removeprefix('# ')
    number = module.name[:2]
    date_match = re.search(r'Tanggal eksperimen: \*\*(.+?)\*\*', markdown)
    status_match = re.search(r'Status laporan: \*\*(.+?)\*\*', markdown)
    body = markdown[markdown.index('## Ringkasan riset'):]
    body = body.split('## Rujukan')[0].rstrip()
    story = [paragraph('LAPORAN RISET EKSPERIMEN / MODUL ' + number, module, 'eyebrow'),
             paragraph(title.split(' - ',1)[1], module, 'title')]
    identity_values = {}
    for line in (ROOT/'UTS/IDENTITAS.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('|'):
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if len(cells) == 2:
                identity_values[cells[0]] = cells[1]
    def identity_field(label,key):
        value = identity_values.get(key) or '__________________________'
        if key == 'Tanggal pelaksanaan eksperimen' and date_match and date_match[1] != 'belum diisi':
            value = date_match[1]
        return Paragraph(f'{label}: {html.escape(value)}',STYLES['small'])
    identity = Table([
        [identity_field('Nama','Nama'),identity_field('NIM','NIM')],
        [identity_field('Kelas','Kelas'),identity_field('Tanggal uji','Tanggal pelaksanaan eksperimen')],
    ],colWidths=[CONTENT_WIDTH/2]*2)
    identity.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story += [identity, Spacer(1,7)]
    status_text = ('<b>Hasil uji awal.</b> ' + html.escape(status_match[1])) if status_match else (
        '<b>Status draf.</b> Disusun dari materi kelas dan kajian program. '
        'Foto, data alat, serta simpulan empiris dilengkapi setelah pengujian.')
    note = Table([[Paragraph(status_text, STYLES['small'])]],
                 colWidths=[CONTENT_WIDTH])
    note.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('BOX',(0,0),(-1,-1),.5,colors.HexColor('#d4dfeb')),
                              ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
                              ('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story += [note, Spacer(1,5)]
    story += blocks(body, module)
    story.append(paragraph('Rujukan', module, 'h2'))
    story += [paragraph(f'{i}. {reference}', module, 'small')
              for i,reference in enumerate(BIBLIOGRAPHY[number],1)]
    file = OUTPUT / f'Laporan_UTS_{module.name}.pdf'
    author_name = identity_values.get('Nama') or 'Mahasiswa'
    document = SimpleDocTemplate(str(file),pagesize=A4,rightMargin=MARGIN,leftMargin=MARGIN,
                                  topMargin=23*mm,bottomMargin=21*mm,
                                  title=title,author=author_name,
                                  subject='Laporan resmi eksperimen iMCLab untuk UTS Robotika')
    if identity_values.get('Nama') and identity_values.get('NIM'):
        footer = f"{identity_values['Nama']} ({identity_values['NIM']}) - {identity_values.get('Kelas', 'Robotika')}"
    else:
        footer = ('HASIL UJI AWAL - identitas dan kalibrasi RPM belum lengkap' if status_match else
                  'DRAF - hasil eksperimen dan identitas belum dilengkapi')
    document.build(story,onFirstPage=chrome('MODUL '+number, footer),onLaterPages=chrome('MODUL '+number, footer))
    shutil.copy2(file, module/'LAPORAN.pdf')
    print(file.relative_to(ROOT))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--modul', choices=['01', '02', '03', '04'], help='Ekspor satu modul saja')
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True,exist_ok=True)
    for directory in sorted((ROOT/'UTS').glob('[0-9][0-9]_*')):
        if (directory/'LAPORAN.md').exists() and (not args.modul or directory.name.startswith(args.modul+'_')):
            build(directory)
