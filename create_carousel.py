# -*- coding: utf-8 -*-
"""
Hanna Brand – Instagram Carousel Generator
10 Slides: "Warum dein Business nicht skaliert"
"""

from PIL import Image, ImageDraw, ImageFont
import os, textwrap

# ── Output ──────────────────────────────────────────────────────────────────
OUT = "G:/Meine Ablage/Claudes Playground/Hanna Brand/Instagram Carousel"
os.makedirs(OUT, exist_ok=True)

# ── Brand Colors ─────────────────────────────────────────────────────────────
BLACK      = (13,  11,  10)
CHARCOAL   = (30,  26,  23)
WARM_DARK  = (44,  36,  32)
GOLD       = (192, 155,  94)
GOLD_LIGHT = (217, 188, 139)
GOLD_PALE  = (239, 224, 196)
BLUSH      = (205, 180, 172)
CREAM      = (247, 243, 238)
WHITE      = (253, 252, 250)
MIST       = (234, 229, 223)
MID_GRAY   = (138, 127, 120)
CHAR_MED   = (70,  60,  55)

# ── Fonts ─────────────────────────────────────────────────────────────────────
F = "C:/Windows/Fonts/"

def font(name, size):
    return ImageFont.truetype(F + name, size)

# Font shortcuts
def load_fonts():
    return {
        "display_huge":   font("CormorantInfant-Bold.ttf",       96),
        "display_xl":     font("CormorantInfant-Bold.ttf",       80),
        "display_lg":     font("CormorantInfant-SemiBold.ttf",   64),
        "display_md":     font("CormorantInfant-Medium.ttf",     52),
        "display_italic": font("CormorantInfant-BoldItalic.ttf", 72),
        "display_it_sm":  font("CormorantInfant-Italic.ttf",     44),
        "body_light":     font("Montserrat-Light.ttf",           28),
        "body_reg":       font("Montserrat-Regular.ttf",         26),
        "body_sm":        font("Montserrat-Light.ttf",           24),
        "label":          font("Montserrat-SemiBold.ttf",        13),
        "handle":         font("Montserrat-SemiBold.ttf",        19),
        "slide_num":      font("Montserrat-Light.ttf",           15),
        "cta_btn":        font("Montserrat-SemiBold.ttf",        22),
        "quote":          font("CormorantInfant-LightItalic.ttf",48),
    }

# ── Canvas ────────────────────────────────────────────────────────────────────
SIZE = 1080
PAD  = 80
W = SIZE

def new_canvas(bg):
    img = Image.new("RGB", (SIZE, SIZE), bg)
    d   = ImageDraw.Draw(img)
    return img, d

# ── Helper: Draw text with optional max-width wrap ────────────────────────────
def draw_text(d, text, x, y, fnt, color, anchor="la", max_w=None, line_height=None):
    """Draw text, optionally wrapping to max_w pixels."""
    if max_w is None:
        d.text((x, y), text, font=fnt, fill=color, anchor=anchor)
        return y + fnt.size + 8
    # word-wrap
    words = text.split()
    lines, line = [], []
    for w in words:
        test = " ".join(line + [w])
        if d.textlength(test, font=fnt) <= max_w:
            line.append(w)
        else:
            if line:
                lines.append(" ".join(line))
            line = [w]
    if line:
        lines.append(" ".join(line))
    lh = line_height or int(fnt.size * 1.4)
    cy = y
    for ln in lines:
        d.text((x, cy), ln, font=fnt, fill=color, anchor=anchor)
        cy += lh
    return cy

def text_height(d, text, fnt, max_w, line_height=None):
    """Estimate pixel height of wrapped text block."""
    words = text.split()
    lines, line = [], []
    for w in words:
        test = " ".join(line + [w])
        if d.textlength(test, font=fnt) <= max_w:
            line.append(w)
        else:
            if line:
                lines.append(" ".join(line))
            line = [w]
    if line:
        lines.append(" ".join(line))
    lh = line_height or int(fnt.size * 1.4)
    return len(lines) * lh

# ── Decoration helpers ────────────────────────────────────────────────────────
def gold_line(d, x1, y, x2, width=1, color=GOLD):
    d.line([(x1, y), (x2, y)], fill=color, width=width)

def label_tag(d, text, x, y, fnt, color=GOLD):
    d.text((x, y), text, font=fnt, fill=color, anchor="la")
    lw = d.textlength(text, font=fnt)
    return y + fnt.size + 4

def dot_bullet(d, x, y, color=GOLD, r=4):
    d.ellipse([(x-r, y-r), (x+r, y+r)], fill=color)

def corner_handle(d, f, dark=True):
    color = GOLD_PALE if dark else MID_GRAY
    # left bottom: slide handle
    d.text((PAD, SIZE - PAD), "@hanna.gpt", font=f["handle"], fill=color, anchor="lb")

def slide_number(d, f, n, total=10, dark=True):
    color = MID_GRAY if dark else BLUSH
    d.text((SIZE - PAD, SIZE - PAD), f"{n:02d} / {total}", font=f["slide_num"],
           fill=color, anchor="rb")

def top_accent_line(d, color=GOLD):
    gold_line(d, PAD, 52, SIZE - PAD, width=1, color=color)

def swipe_hint(d, f, dark=True):
    color = MID_GRAY if dark else BLUSH
    d.text((SIZE - PAD, SIZE - PAD - 28), "Swipe →", font=f["slide_num"],
           fill=color, anchor="rb")

# ── SLIDE FACTORIES ───────────────────────────────────────────────────────────

def slide_01(f):
    """Cover – Dark"""
    img, d = new_canvas(CHARCOAL)
    top_accent_line(d, GOLD)

    # Label
    y = 140
    d.text((PAD, y), "HANNA.GPT  ·  SYSTEME STATT PROMPTS", font=f["label"],
           fill=MID_GRAY, anchor="la")
    y += 40
    gold_line(d, PAD, y, PAD + 180, color=GOLD)

    # Main heading
    y += 40
    y = draw_text(d, "Warum dein Business", PAD, y, f["display_xl"], WHITE, max_w=SIZE-2*PAD)
    y = draw_text(d, "nicht skaliert –", PAD, y, f["display_xl"], WHITE, max_w=SIZE-2*PAD)
    y += 10
    y = draw_text(d, "obwohl du alles gibst.", PAD, y, f["display_italic"], GOLD_LIGHT,
                  max_w=SIZE-2*PAD)

    # Gold separator
    y += 48
    gold_line(d, PAD, y, PAD + 120, width=1, color=GOLD)

    # Sub-copy
    y += 32
    y = draw_text(d, "3 Gründe, die die meisten nie benennen.",
                  PAD, y, f["body_light"], GOLD_PALE, max_w=SIZE-2*PAD)

    corner_handle(d, f, dark=True)
    swipe_hint(d, f, dark=True)
    slide_number(d, f, 1, dark=True)
    img.save(f"{OUT}/01_Cover.png")
    print("OK Slide 01")


def slide_02(f):
    """Pain – Dark"""
    img, d = new_canvas(CHARCOAL)
    top_accent_line(d, GOLD)

    y = 140
    d.text((PAD, y), "DIE REALITÄT", font=f["label"], fill=GOLD, anchor="la")

    y += 48
    y = draw_text(d, "Du gibst alles.", PAD, y, f["display_lg"], WHITE, max_w=SIZE-2*PAD)
    y += 16

    sub = "Und trotzdem fühlt es sich an, als würde nichts wirklich laufen."
    y = draw_text(d, sub, PAD, y, f["body_light"], GOLD_PALE, max_w=SIZE-2*PAD, line_height=40)

    # Bullet points
    y += 56
    bullets = [
        "50+ Stunden pro Woche – und du kommst trotzdem nicht nach",
        "Keine Kapazität für neue Kunden, aber du willst mehr Umsatz",
        "Wochenenden? Existieren nur noch auf dem Papier",
        "KI hast du probiert – aber wirklich Zeit gespart? Nein.",
    ]
    for b in bullets:
        dot_bullet(d, PAD + 8, y + 10, color=GOLD)
        draw_text(d, b, PAD + 28, y, f["body_sm"], MIST, max_w=SIZE-2*PAD-28,
                  line_height=36)
        th = text_height(d, b, f["body_sm"], SIZE-2*PAD-28, 36)
        y += th + 20

    corner_handle(d, f, dark=True)
    slide_number(d, f, 2, dark=True)
    img.save(f"{OUT}/02_Realitaet.png")
    print("OK Slide 02")


def slide_03(f):
    """Problem Statement – Cream"""
    img, d = new_canvas(CREAM)
    top_accent_line(d, GOLD)

    y = 140
    d.text((PAD, y), "DAS PROBLEM", font=f["label"], fill=GOLD, anchor="la")

    y += 56
    y = draw_text(d, "Du bist", PAD, y, f["display_xl"], CHARCOAL, max_w=SIZE-2*PAD)
    y = draw_text(d, "der Engpass.", PAD, y, f["display_xl"], CHARCOAL, max_w=SIZE-2*PAD)

    y += 12
    gold_line(d, PAD, y, PAD + 140, width=1, color=GOLD)

    y += 40
    sub = "Nicht weil du zu wenig kannst. Sondern weil alles durch dich läuft."
    y = draw_text(d, sub, PAD, y, f["body_light"], CHAR_MED, max_w=SIZE-2*PAD, line_height=42)

    # Italic clarification
    y += 36
    y = draw_text(d, "Jede E-Mail. Jeder Post. Jede Kundenanfrage.",
                  PAD, y, f["display_it_sm"], GOLD, max_w=SIZE-2*PAD)

    y += 32
    d.text((PAD, y), "Das ist kein Fleiß-Problem.", font=f["body_light"], fill=CHAR_MED)
    y += 44
    d.text((PAD, y), "Das ist ein Struktur-Problem.", font=f["body_reg"], fill=CHARCOAL)

    corner_handle(d, f, dark=False)
    slide_number(d, f, 3, dark=False)
    img.save(f"{OUT}/03_Problem.png")
    print("OK Slide 03")


def slide_04(f):
    """Grund 1 – Dark"""
    img, d = new_canvas(WARM_DARK)
    top_accent_line(d, GOLD)

    y = 140
    d.text((PAD, y), "GRUND  #01", font=f["label"], fill=GOLD, anchor="la")

    y += 56
    y = draw_text(d, "Jede Aufgabe", PAD, y, f["display_lg"], WHITE, max_w=SIZE-2*PAD)
    y = draw_text(d, "läuft durch dich.", PAD, y, f["display_lg"], WHITE, max_w=SIZE-2*PAD)

    y += 24
    gold_line(d, PAD, y, SIZE - PAD, width=1, color=(60, 50, 44))
    y += 32

    body = "Du bist gleichzeitig CEO, Kundenservice, Content-Autorin und VA. " \
           "Kein System entscheidet ohne dich. Kein Prozess läuft ohne dich. " \
           "Du bist der Bottleneck – in deinem eigenen Unternehmen."
    y = draw_text(d, body, PAD, y, f["body_sm"], MIST, max_w=SIZE-2*PAD, line_height=40)

    # Callout box
    y += 52
    box_h = 88
    d.rounded_rectangle([(PAD, y), (SIZE-PAD, y+box_h)], radius=6,
                         fill=(50, 42, 38), outline=GOLD, width=1)
    d.text((SIZE//2, y + box_h//2), "Skalierung ohne Systemwechsel ist Erschöpfung.",
           font=f["body_sm"], fill=GOLD_LIGHT, anchor="mm")

    corner_handle(d, f, dark=True)
    slide_number(d, f, 4, dark=True)
    img.save(f"{OUT}/04_Grund1.png")
    print("OK Slide 04")


def slide_05(f):
    """Grund 2 – Cream"""
    img, d = new_canvas(CREAM)
    top_accent_line(d, GOLD)

    y = 140
    d.text((PAD, y), "GRUND  #02", font=f["label"], fill=GOLD, anchor="la")

    y += 56
    y = draw_text(d, "Du denkst in Tools.", PAD, y, f["display_lg"], CHARCOAL, max_w=SIZE-2*PAD)
    y += 8
    y = draw_text(d, "Nicht in Systemen.", PAD, y, f["display_it_sm"], GOLD, max_w=SIZE-2*PAD)

    y += 36
    gold_line(d, PAD, y, PAD + 100, width=1, color=GOLD)
    y += 36

    body = "ChatGPT, Zapier, Notion, Make – du sammelst Werkzeuge. " \
           "Aber ohne Prozesslogik dahinter bleibt jedes Tool ein Pflaster, " \
           "kein Heilmittel."
    y = draw_text(d, body, PAD, y, f["body_light"], CHAR_MED, max_w=SIZE-2*PAD, line_height=42)

    y += 52
    # Side comparison
    col_w = (SIZE - 2*PAD - 32) // 2
    # LEFT col
    d.rounded_rectangle([(PAD, y), (PAD+col_w, y+160)], radius=4,
                         fill=MIST, outline=BLUSH, width=1)
    d.text((PAD + 20, y + 24), "TOOL", font=f["label"], fill=MID_GRAY)
    tw = "Einmalige Aktion. Du machst es. Du wiederholst es."
    draw_text(d, tw, PAD+20, y+50, f["body_sm"], CHAR_MED, max_w=col_w-40, line_height=34)

    # RIGHT col
    rx = PAD + col_w + 32
    d.rounded_rectangle([(rx, y), (rx+col_w, y+160)], radius=4,
                         fill=(230, 220, 205), outline=GOLD, width=1)
    d.text((rx + 20, y + 24), "SYSTEM", font=f["label"], fill=GOLD)
    sw = "Automatischer Prozess. Läuft. Ohne dich."
    draw_text(d, sw, rx+20, y+50, f["body_sm"], CHARCOAL, max_w=col_w-40, line_height=34)

    corner_handle(d, f, dark=False)
    slide_number(d, f, 5, dark=False)
    img.save(f"{OUT}/05_Grund2.png")
    print("OK Slide 05")


def slide_06(f):
    """Grund 3 – Dark"""
    img, d = new_canvas(CHARCOAL)
    top_accent_line(d, GOLD)

    y = 140
    d.text((PAD, y), "GRUND  #03", font=f["label"], fill=GOLD, anchor="la")

    y += 56
    y = draw_text(d, "Du nutzt KI wie einen", PAD, y, f["display_md"], WHITE, max_w=SIZE-2*PAD)
    y = draw_text(d, "Assistenten.", PAD, y, f["display_lg"], GOLD_LIGHT, max_w=SIZE-2*PAD)

    y += 24
    gold_line(d, PAD, y, PAD + 90, width=1, color=GOLD)
    y += 36

    body = "Einmal fragen. Einmal antworten. Fertig. " \
           "Das ist kein Betriebssystem – das ist Beschäftigung."
    y = draw_text(d, body, PAD, y, f["body_light"], MIST, max_w=SIZE-2*PAD, line_height=42)

    y += 44
    d.text((PAD, y), "Was du stattdessen brauchst:", font=f["label"], fill=GOLD)
    y += 36

    items = [
        "Autonome Agenten die Aufgaben übernehmen",
        "Prozesse die dich als Engpass entfernen",
        "Ein KI-Betriebssystem – nicht ein Chat-Fenster",
    ]
    for item in items:
        dot_bullet(d, PAD + 8, y + 10, color=GOLD)
        th = text_height(d, item, f["body_sm"], SIZE-2*PAD-28, 36)
        draw_text(d, item, PAD + 28, y, f["body_sm"], GOLD_PALE, max_w=SIZE-2*PAD-28,
                  line_height=36)
        y += th + 18

    corner_handle(d, f, dark=True)
    slide_number(d, f, 6, dark=True)
    img.save(f"{OUT}/06_Grund3.png")
    print("OK Slide 06")


def slide_07(f):
    """Der Unterschied – Cream"""
    img, d = new_canvas(CREAM)
    top_accent_line(d, GOLD)

    y = 140
    d.text((PAD, y), "DER UNTERSCHIED", font=f["label"], fill=GOLD, anchor="la")

    y += 52
    y = draw_text(d, "Prompt vs. System.", PAD, y, f["display_lg"], CHARCOAL, max_w=SIZE-2*PAD)

    y += 16
    gold_line(d, PAD, y, SIZE-PAD, width=1, color=BLUSH)
    y += 36

    # Two big blocks
    bh = 260
    bw = (SIZE - 2*PAD - 28) // 2

    # LEFT – Prompt (grey/muted)
    d.rounded_rectangle([(PAD, y), (PAD+bw, y+bh)], radius=6,
                         fill=MIST, outline=BLUSH, width=1)
    d.text((PAD+bw//2, y+28), "PROMPT", font=f["label"], fill=MID_GRAY, anchor="mt")
    # Draw X shape manually
    cx, cy2 = PAD+bw//2, y+82
    r = 18
    d.line([(cx-r, cy2-r), (cx+r, cy2+r)], fill=BLUSH, width=4)
    d.line([(cx+r, cy2-r), (cx-r, cy2+r)], fill=BLUSH, width=4)
    ptext = "Einmalige Anweisung. Einmaliges Ergebnis. Du bist immer noch dabei."
    draw_text(d, ptext, PAD+24, y+130, f["body_sm"], CHAR_MED, max_w=bw-48, line_height=36)

    # RIGHT – System (gold/dark)
    rx = PAD + bw + 28
    d.rounded_rectangle([(rx, y), (rx+bw, y+bh)], radius=6,
                         fill=(235, 222, 200), outline=GOLD, width=2)
    d.text((rx+bw//2, y+28), "SYSTEM", font=f["label"], fill=GOLD, anchor="mt")
    # Draw checkmark manually
    cx2 = rx + bw//2
    d.line([(cx2-20, cy2+2), (cx2-6, cy2+18), (cx2+20, cy2-16)], fill=GOLD, width=4)
    stext = "Autonomer Prozess. Läuft im Hintergrund. Ohne dich."
    draw_text(d, stext, rx+24, y+130, f["body_sm"], CHARCOAL, max_w=bw-48, line_height=36)

    y += bh + 36
    center_txt = "Das ist Hannas Anti-Prompting-Ansatz."
    d.text((SIZE//2, y), center_txt, font=f["body_light"], fill=CHAR_MED, anchor="mt")

    corner_handle(d, f, dark=False)
    slide_number(d, f, 7, dark=False)
    img.save(f"{OUT}/07_Unterschied.png")
    print("OK Slide 07")


def slide_08(f):
    """Vision – Dark"""
    img, d = new_canvas(WARM_DARK)
    top_accent_line(d, GOLD)

    y = 140
    d.text((PAD, y), "DIE VISION", font=f["label"], fill=GOLD, anchor="la")

    y += 56
    y = draw_text(d, "Stell dir vor...", PAD, y, f["display_xl"], WHITE, max_w=SIZE-2*PAD)

    y += 12
    gold_line(d, PAD, y, PAD + 160, width=1, color=GOLD)
    y += 40

    visions = [
        "Kundenanfragen werden automatisch qualifiziert und sortiert.",
        "Content entsteht im Hintergrund – während du schläfst.",
        "Dein Onboarding läuft komplett ohne deine Beteiligung.",
        "Du bist Architektin – nicht Ausführende.",
    ]
    for v in visions:
        dot_bullet(d, PAD + 8, y + 14, color=GOLD, r=5)
        th = text_height(d, v, f["body_sm"], SIZE-2*PAD-36, 38)
        draw_text(d, v, PAD + 32, y, f["body_sm"], MIST, max_w=SIZE-2*PAD-36, line_height=38)
        y += max(th, 48) + 16

    y += 16
    y = draw_text(d, "Das ist kein Traum. Das ist Infrastruktur.",
                  PAD, y, f["display_it_sm"], GOLD_LIGHT, max_w=SIZE-2*PAD)

    corner_handle(d, f, dark=True)
    slide_number(d, f, 8, dark=True)
    img.save(f"{OUT}/08_Vision.png")
    print("OK Slide 08")


def slide_09(f):
    """Die Methode – Cream"""
    img, d = new_canvas(CREAM)
    top_accent_line(d, GOLD)

    y = 140
    d.text((PAD, y), "DIE METHODE", font=f["label"], fill=GOLD, anchor="la")

    y += 56
    y = draw_text(d, "Das ist kein Kurs.", PAD, y, f["display_lg"], CHARCOAL, max_w=SIZE-2*PAD)

    y += 8
    gold_line(d, PAD, y, PAD + 130, width=1, color=GOLD)
    y += 36

    body = "Es ist ein Umbau. Vom Hamsterrad zur Architektur. " \
           "Von Hustle-Energie zu einem Business das läuft – auch wenn du es nicht tust."
    y = draw_text(d, body, PAD, y, f["body_light"], CHAR_MED, max_w=SIZE-2*PAD, line_height=42)

    y += 48
    # Quote block
    qbox_h = 160
    d.rounded_rectangle([(PAD, y), (SIZE-PAD, y+qbox_h)], radius=6,
                         fill=(240, 234, 224), outline=GOLD, width=1)
    d.text((PAD+28, y+24), "»", font=f["display_md"], fill=GOLD)
    qt = "KI muss nicht techy sein. Es trägt dich."
    draw_text(d, qt, PAD+60, y+38, f["quote"], CHARCOAL, max_w=SIZE-2*PAD-88, line_height=52)

    y += qbox_h + 40
    d.text((PAD, y), "Das ist Hannas Kernbotschaft.", font=f["body_light"], fill=CHAR_MED)

    corner_handle(d, f, dark=False)
    slide_number(d, f, 9, dark=False)
    img.save(f"{OUT}/09_Methode.png")
    print("OK Slide 09")


def slide_10(f):
    """CTA – Dark"""
    img, d = new_canvas(CHARCOAL)
    top_accent_line(d, GOLD)

    y = 140
    d.text((PAD, y), "BEREIT?", font=f["label"], fill=GOLD, anchor="la")

    y += 56
    y = draw_text(d, "Dein Business soll", PAD, y, f["display_lg"], WHITE, max_w=SIZE-2*PAD)
    y = draw_text(d, "für dich arbeiten.",  PAD, y, f["display_lg"], WHITE, max_w=SIZE-2*PAD)

    y += 16
    gold_line(d, PAD, y, SIZE-PAD, width=1, color=(55, 46, 40))
    y += 40

    body = "Schreib mir SYSTEM in die DMs und ich zeige dir, " \
           "wie wir deinen ersten autonomen KI-Prozess aufbauen."
    y = draw_text(d, body, PAD, y, f["body_light"], MIST, max_w=SIZE-2*PAD, line_height=42)

    # CTA Button
    y += 64
    btn_h = 72
    btn_w = SIZE - 2*PAD
    d.rounded_rectangle([(PAD, y), (PAD+btn_w, y+btn_h)], radius=6,
                         fill=GOLD, outline=GOLD, width=0)
    d.text((PAD + btn_w//2, y + btn_h//2), "→  DM: SYSTEM",
           font=f["cta_btn"], fill=BLACK, anchor="mm")

    y += btn_h + 36

    # Sub CTA
    d.text((SIZE//2, y), "Oder Link in Bio für alle Details.",
           font=f["body_sm"], fill=MID_GRAY, anchor="mt")

    # Handle big + centered
    y += 48
    d.text((SIZE//2, y), "@hanna.gpt", font=f["display_it_sm"], fill=GOLD_LIGHT, anchor="mt")

    slide_number(d, f, 10, dark=True)
    img.save(f"{OUT}/10_CTA.png")
    print("OK Slide 10")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Loading fonts...")
    f = load_fonts()
    print("Generating slides...\n")
    slide_01(f)
    slide_02(f)
    slide_03(f)
    slide_04(f)
    slide_05(f)
    slide_06(f)
    slide_07(f)
    slide_08(f)
    slide_09(f)
    slide_10(f)
    print(f"\nDone! Slides saved to:\n{OUT}")
