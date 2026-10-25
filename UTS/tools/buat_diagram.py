"""Membuat ilustrasi SVG asli untuk laporan (tanpa data eksperimen)."""
from html import escape
from pathlib import Path
from math import hypot

ROOT = Path(__file__).resolve().parents[1]
BLUE, INK, TEAL = '#2159b8', '#172b49', '#087d82'


def text(x, y, value, size=18, color=INK, anchor='start', weight='400'):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')


def box(x, y, w, title, lines=(), color=BLUE):
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="118" rx="14" fill="white" stroke="{color}" stroke-width="2"/>',
             text(x+20,y+34,title,21,color,weight='700')]
    parts += [text(x+20,y+63+i*24,line,17) for i,line in enumerate(lines)]
    return ''.join(parts)


def arrow(x1,y1,x2,y2,label='',label_y=None,color=BLUE):
    length=hypot(x2-x1,y2-y1)
    ux,uy=(x2-x1)/length,(y2-y1)/length
    bx,by=x2-13*ux,y2-13*uy
    s=f'<path d="M {x1} {y1} L {bx} {by}" stroke="{color}" stroke-width="3" fill="none"/>'
    s+=f'<polygon points="{x2},{y2} {bx-6*uy},{by+6*ux} {bx+6*uy},{by-6*ux}" fill="{color}"/>'
    if label: s+=text((x1+x2)/2,label_y if label_y is not None else (y1+y2)/2-12,label,16,color,'middle')
    return s


def save(module,name,title,subtitle,body,height=620):
    out=ROOT/module/'gambar'/name
    out.parent.mkdir(parents=True,exist_ok=True)
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}">'
         f'<title>{escape(title)}</title>'
         '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">'
         f'<path d="M0,0 L0,6 L8,3 z" fill="{BLUE}"/></marker></defs>'
         f'<rect width="1200" height="{height}" fill="#f2f6fc"/>'
         '<g font-family="Helvetica,sans-serif">'
         +text(42,53,title,30,INK,weight='700')+text(42,88,subtitle,18)
         +body+text(42,height-30,'ILUSTRASI RANCANGAN | Bukan foto, screenshot, atau hasil ukur.',15,'#566984')+'</g></svg>')
    out.write_text(svg,encoding='utf-8')


body=box(45,160,245,'Serial Monitor',['115200 baud + newline','0 / 1 / PWM:120'])
body+=box(445,160,280,'ESP32 iMCLab',['Parser + PWM 30 kHz','GPIO12 / GPIO27 / 26'])
body+=box(890,160,265,'Driver + motor',['Catu sesuai kit','Satu arah putaran'])
body+=arrow(290,215,445,215,'Perintah')+arrow(725,215,890,215,'PWM + arah')
body+=box(445,370,280,'Sensor pulsa',['GPIO13, FALLING','PPR perlu dikalibrasi'],TEAL)
body+=arrow(1020,278,1020,427)+arrow(1020,427,725,427,'Gerak -> pulsa',410)
body+=arrow(585,370,585,278)+text(610,335,'Monitoring RPM',17,TEAL)
body+=text(45,535,'RPM dipantau; belum ada pengendali yang mengoreksi PWM terhadap target RPM.',20)
save('01_Basic_iMCLab','arsitektur.svg','01 / Kendali dasar motor','Pemetaan sinyal mengikuti kode kelas iMCLab.',body)

body=''
for y,duty,label in [(160,.25,'25% duty (ilustrasi)'),(265,.75,'75% duty (ilustrasi)')]:
    body+=text(45,y-35,label,22,BLUE,weight='700')
    points=[(360,y+40)]
    for cycle in range(4):
        x=360+cycle*180
        points.extend([(x,y+40),(x,y-50),(x+180*duty,y-50),(x+180*duty,y+40),(x+180,y+40)])
    body+=f'<polyline points="{" ".join(f"{x},{yy}" for x,yy in points)}" fill="none" stroke="{TEAL}" stroke-width="4"/>'
    body+=text(300,y-44,'HIGH',15)+text(306,y+45,'LOW',15)
body+=text(45,340,'Periode dan amplitudo sama; proporsi HIGH berubah. PWM 8 bit: duty nominal = nilai / 255.',20)
save('01_Basic_iMCLab','pwm.svg','01 / Memahami duty cycle','Sinyal teoritis; bukan hasil pengukuran osiloskop.',body,height=400)

body=box(45,170,300,'Python di komputer',['Validasi + pilih COM','Kirim perintah, tunggu ACK'])
body+=box(785,170,370,'ESP32 + driver + motor',['Firmware Modul 01','PWM dan sensor dijalankan lokal'])
body+=arrow(345,205,785,205,'USB serial: PWM:120 + newline',188)
body+=arrow(785,258,345,258,'ACK / DATA / STATUS',296)
body+=box(45,390,450,'Log CSV dari serial',['Waktu terima, TX/RX, teks asli','PWM, setpoint, RPM, pulsa, durasi'],TEAL)
body+=arrow(195,288,195,390)
body+=text(555,427,'ACK = perintah diproses.',22,BLUE,weight='700')
body+=text(555,461,'Gerak dan RPM tetap perlu diamati.',20)
save('02_Python_iMCLab','arsitektur.svg','02 / Python sebagai antarmuka kendali','Python berjalan di komputer; firmware motor tetap di ESP32.',body)

body=box(45,170,280,'Dashboard Blynk',['V2: setpoint PWM','V3: enable OFF / ON'])
body+=box(465,170,270,'Blynk.Cloud',['Datastream per device','Perintah dan telemetri'])
body+=box(875,170,280,'ESP32 + iMCLab',['Wi-Fi + PWM + sensor','Keluaran awal OFF'])
body+=arrow(325,212,465,212,'Internet')+arrow(735,212,875,212,'Wi-Fi')
body+=arrow(1015,288,1015,402)+arrow(1015,402,185,402,'V0: RPM | V1: PWM aktual | V2: setpoint | V3: enable',380)+arrow(185,402,185,288)
body+=text(45,482,'V2 positif saat OFF menyimpan setpoint; V1 tetap nol.',23,BLUE,weight='700')
body+=text(45,524,'Koneksi putus terdeteksi -> motor OFF. Reconnect -> perlu ON kembali.',20)
save('03_Blynk_iMCLab','arsitektur.svg','03 / Kendali dan monitoring melalui cloud','Pin virtual Blynk berbeda dari pin GPIO pada board.',body)

body=box(45,165,300,'01. Firmware awal',['Upload USB: 1.0.0','Provisioning + online'])
body+=box(450,165,300,'02. Siapkan pembaruan',['Build 1.0.1: aplikasi .bin','Pilih device di Blynk.Air'])
body+=box(855,165,300,'03. Proses OTA',['Motor OFF dan dikunci','Unduh -> tulis -> reboot'])
body+=arrow(345,220,450,220)+arrow(750,220,855,220)
body+=arrow(1005,283,1005,374)+arrow(1005,374,600,374)+arrow(600,374,600,405)
body+=box(360,405,480,'04. Buktikan versi dan fungsi',['Online + V4 / Serial menunjukkan 1.0.1','Uji ON/OFF lagi; simpan bukti asli'],TEAL)
save('04_OTA_Blynk','arsitektur.svg','04 / Pembaruan firmware melalui Blynk.Air','USB hanya untuk pemasangan awal pada skenario uji ini.',body)
print('5 diagram SVG dibuat.')
