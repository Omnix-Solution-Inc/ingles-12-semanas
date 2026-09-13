# -*- coding: utf-8 -*-
"""Genera las hojas de trabajo AUTOEDITABLES (fillable PDFs) para cada día definido en content/days.json"""
import json, os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(BASE, '') 
pdfmetrics.registerFont(TTFont('Inter', F+'Inter.ttf'))
pdfmetrics.registerFont(TTFont('InterB', F+'Inter-SemiBold.ttf'))
pdfmetrics.registerFont(TTFont('PlayB', F+'PlayfairDisplay-Bold.ttf'))
pdfmetrics.registerFont(TTFont('PlaySB', F+'PlayfairDisplay-SemiBold.ttf'))

INK   = HexColor('#3A3620')
TEAL  = HexColor('#C77A38')   # naranja kaki
TEALL = HexColor('#F2F7DE')   # verde limón claro
SAND  = HexColor('#FFFBEE')
GOLD  = HexColor('#D2894A')   # naranja kaki suave
GRAY  = HexColor('#857E5E')
BUTTER      = HexColor('#F7DE7A')
BUTTER_DEEP = HexColor('#8A6D1F')
LIME        = HexColor('#A9C23D')
W, H = letter

def field(c, name, x, y, w, h=15, tip='', fs=10):
    c.acroForm.textfield(name=name, tooltip=tip, x=x, y=y, width=w, height=h,
        borderWidth=0, forceBorder=False, fontName='Helvetica', fontSize=fs,
        textColor=INK, fillColor=None, borderColor=None)

def hline(c, x1, x2, y, w=0.7, col='#D6CFAE'):
    c.setStrokeColor(HexColor(col)); c.setLineWidth(w); c.line(x1, y, x2, y)

def section(c, y, num, title, sub=''):
    c.setFillColor(GOLD); c.circle(58, y+4, 10.5, fill=1, stroke=0)
    c.setFillColor(HexColor('#FFFFFF')); c.setFont('InterB', 11)
    c.drawCentredString(58, y, str(num))
    c.setFillColor(INK); c.setFont('InterB', 12)
    c.drawString(78, y, title.upper())
    if sub:
        c.setFont('Inter', 9); c.setFillColor(GRAY)
        c.drawString(78, y-13, sub)
        return y - 26
    return y - 16

def build_day(d, outdir):
    c = canvas.Canvas(os.path.join(outdir, f'hoja-dia-{d["day"]:02d}.pdf'), pagesize=letter)
    c.setTitle(f'Day {d["day"]} Worksheet · Inglés 12 Semanas')
    c.setAuthor('Inglés 12 Semanas')
    c.setFillColor(SAND); c.rect(0, 0, W, H, fill=1, stroke=0)
    # HEADER
    c.setFillColor(BUTTER); c.rect(0, H-118, W, 118, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont('PlayB', 24)
    c.drawString(48, H-52, f'Day {d["day"]} of 84')
    c.setFillColor(BUTTER_DEEP); c.setFont('Inter', 10.5)
    c.drawString(48, H-70, f'WEEK {d["week"]} · PHASE 1 · THE BUILDING BLOCKS  ·  DAILY WORKSHEET')
    c.setFillColor(INK); c.setFont('PlaySB', 13); c.drawRightString(W-48, H-52, 'Inglés 12 Semanas')
    c.setFillColor(BUTTER_DEEP); c.setFont('Inter', 9); c.drawRightString(W-48, H-70, '(provisional name)')
    c.setFillColor(LIME); c.rect(48, H-100, W-96, 2.4, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont('PlaySB', 15)
    c.drawString(48, H-140, 'Today:  ' + d['topic'])
    c.setFont('Inter', 9.5); c.setFillColor(GRAY)
    c.drawString(390, H-140, 'Your name:')
    field(c, 'student_name', 462, H-143, 102, tip='Type your name here')
    # 1. VOCABULARIO
    y = section(c, H-174, 1, 'Words of the day', 'Write each word 3 times — writing by hand makes it stick.')
    y -= 6
    words = d['words']
    row_h = 22
    tab_top, tab_bot = y, y - len(words)*row_h
    c.setFillColor(TEALL); c.rect(48, tab_bot, W-96, tab_top - tab_bot, fill=1, stroke=0)
    for i, (w_, ph, m) in enumerate(words):
        ry = tab_top - i*row_h - 15
        c.setFillColor(INK); c.setFont('InterB', 11.5); c.drawString(58, ry, w_)
        c.setFont('Inter', 9); c.setFillColor(GRAY)
        c.drawString(58 + pdfmetrics.stringWidth(w_, 'InterB', 11.5) + 8, ry, ph)
        c.setFillColor(INK); c.setFont('Inter', 10); c.drawString(176, ry, m)
        for seg in range(3):
            lx = 288 + seg*92
            hline(c, lx, lx+80, ry-2)
            field(c, f'w{i+1}_line{seg+1}', lx, ry-2, 80, 15, f'Write "{w_}" here')
    y = tab_bot - 12
    # 2. SONIDO
    s = d['sound']
    y = section(c, y, 2, 'Sound of the day', 'Phonetics: ' + s['ipa'] + ' — ' + s['hint'])
    c.setFillColor(TEAL); c.setFont('InterB', 12); c.drawString(58, y-10, s['ipa'])
    ipa_w = pdfmetrics.stringWidth(s['ipa'], 'InterB', 12)
    c.setFillColor(INK); c.setFont('Inter', 10); c.drawString(58 + ipa_w + 10, y-10, s['line1'])
    c.setFillColor(GRAY); c.setFont('Inter', 10); c.drawString(84, y-24, s['line2'])
    c.setFillColor(INK); c.setFont('Inter', 10)
    c.drawString(58, y-40, f'Say this phrase out loud 5 times:  "{d["phrase"]["en"]}"')
    y -= 56
    # 3. GRAMÁTICA
    g = d['grammar']
    y = section(c, y, 3, 'Grammar in 5 minutes', 'Today: ' + g['title'])
    c.setFillColor(TEALL); c.rect(48, y-42, W-96, 42, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont('InterB', 10.5)
    c.drawString(60, y-16, g['ex1'])
    c.drawString(60, y-33, g['ex2'])
    y -= 54
    c.setFillColor(TEAL); c.setFont('InterB', 11); c.drawString(58, y, g['intro'])
    c.setFillColor(INK); c.setFont('Inter', 11)
    for i, (left, right, _ans) in enumerate(g['exercises']):
        yy = y - 18 - i*19
        c.drawString(58, yy, left)
        fx = 58 + pdfmetrics.stringWidth(left, 'Inter', 11) + 4
        fw = 118
        field(c, f'ej{i+1}', fx, yy-3, fw, 15, 'Type your answer')
        c.drawString(fx + fw + 8, yy, right)
    y -= 18 + 2*19 + 14
    # 4. FRASE
    p = d['phrase']
    y = section(c, y, 4, 'Phrase of the day', 'Write it here and say it out loud 3 times.')
    c.setFillColor(GOLD); c.rect(48, y-34, 4, 34, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont('PlaySB', 14); c.drawString(64, y-15, f'"{p["en"]}"')
    c.setFillColor(GRAY); c.setFont('Inter', 10); c.drawString(64, y-29, p['es'])
    hline(c, 64, W-70, y-58)
    field(c, 'phrase_copy', 64, y-58, W-134, 16, 'Type the phrase of the day', 11)
    y -= 74
    # ===== PÁGINA 2 — PRÁCTICA: HABLAR Y ESCRIBIR =====
    c.showPage()
    c.setFillColor(SAND); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BUTTER); c.rect(0, H-92, W, 92, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont('PlayB', 20)
    c.drawString(48, H-48, f'Day {d["day"]} of 84 — Practice')
    c.setFillColor(BUTTER_DEEP); c.setFont('Inter', 10)
    c.drawString(48, H-68, 'SPEAK A LITTLE, WRITE A LITTLE — EVERY SINGLE DAY')
    c.setFillColor(INK); c.setFont('PlaySB', 12); c.drawRightString(W-48, H-48, 'Inglés 12 Semanas')
    c.setFillColor(LIME); c.rect(48, H-82, W-96, 2.4, fill=1, stroke=0)
    y = H-122
    pr = d['practice']
    # 5. SPEAK TODAY
    y = section(c, y, 5, 'Speak today', 'Say it out loud — check each one as you say it.')
    for i, task in enumerate(pr['speak']):
        yy = y - 8 - i*28
        c.acroForm.checkbox(name=f'speak{i+1}', checked=False, x=58, y=yy-3, size=13,
            buttonStyle='check', borderWidth=1.2, borderColor=TEAL, fillColor=None, textColor=TEAL,
            tooltip='Check when you said it out loud')
        c.setFillColor(INK); c.setFont('Inter', 10)
        import textwrap
        lines = textwrap.wrap(task, 82)
        c.drawString(80, yy, lines[0])
        for extra in lines[1:]:
            yy -= 13
            c.drawString(80, yy, extra)
    y = y - 8 - len(pr['speak'])*28 - 10
    # 6. WRITE TODAY
    y = section(c, y, 6, 'Write today', 'Translate and create — real writing, every day.')
    c.setFillColor(TEAL); c.setFont('InterB', 10.5); c.drawString(58, y-6, 'Translate to English:')
    yy = y - 24
    for i, tr in enumerate(pr['translate']):
        c.setFillColor(GRAY); c.setFont('Inter', 10.5); c.drawString(66, yy, tr[0])
        hline(c, 230, W-70, yy-2)
        field(c, f'tr{i+1}', 230, yy-2, W-300, 15, 'Write it in English')
        yy -= 28
    c.setFillColor(TEAL); c.setFont('InterB', 10.5); c.drawString(58, yy, 'Your turn to create:')
    c.setFillColor(INK); c.setFont('Inter', 10); c.drawString(66, yy-16, pr['write'])
    yy -= 33
    for i in range(3):
        hline(c, 66, W-70, yy-2)
        field(c, f'free{i+1}', 66, yy-2, W-136, 15, 'Write your sentences here')
        yy -= 24
    y = yy - 4
    # 7. FEEL
    y = section(c, y, 7, 'How did you feel today?', 'Mark one and celebrate your day.')
    opts = [('feel', 'great', 'Great'), ('feel', 'okay', 'Okay'), ('feel', 'hard', 'It was hard')]
    ox = 58
    for gname, val, label in opts:
        c.acroForm.radio(name=gname, value=val, selected=False, x=ox, y=y-1, size=14,
            shape='circle', borderWidth=1, borderColor=TEAL, fillColor=None, textColor=INK, tooltip=label)
        c.setFillColor(INK); c.setFont('Inter', 10.5); c.drawString(ox+20, y, label)
        ox += 118
    c.acroForm.checkbox(name='day_complete', checked=False, x=W-236, y=y-4, size=14,
        buttonStyle='check', borderWidth=1.6, borderColor=GOLD, fillColor=None, textColor=GOLD,
        tooltip=f'Check when you finish Day {d["day"]}')
    c.setFillColor(INK); c.setFont('Inter', 10.5); c.drawString(W-214, y, f'Day {d["day"]} complete')
    hline(c, 48, W-48, 46, 1, '#D9A441')
    c.setFont('Inter', 8); c.setFillColor(GRAY)
    c.drawString(48, 34, f'Inglés 12 Semanas · Day {d["day"]} Worksheet (fillable) · Design sample — name and style are provisional')
    c.save()

if __name__ == '__main__':
    data = json.load(open(os.path.join(BASE, 'content/days.json')))
    out = os.path.join(BASE, 'hojas')
    os.makedirs(out, exist_ok=True)
    for d in data['days']:
        build_day(d, out)
        print('hoja lista:', d['day'], d['topic'])
