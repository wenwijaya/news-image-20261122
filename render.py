#!/usr/bin/env python3
"""Render the front page of 22 November 2026 as one 1024x1024 image.

Draws a newspaper front page with PIL: masthead, lead story (COP31
deadlock), Gulf war, Peru quake, cartel arrest, Ukraine barrage, APEC,
and an in-brief strip. Pure vector + text drawing; deterministic output.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (20, 20, 20)
RED = (164, 18, 18)
BLUE = (29, 78, 137)
TEAL = (15, 118, 110)
GREY = (90, 86, 76)
LIGHT = (232, 226, 208)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped paragraph; returns y after last line."""
    if leading is None:
        leading = int(fnt.size * 1.35)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def double_rule(draw, x0, y, x1):
    rule(draw, x0, y, x1, 4)
    rule(draw, x0, y + 7, x1, 1)


def kicker(draw, x, y, text, fill=RED, size=17):
    draw.text((x, y), text, font=font(SANS_B, size), fill=fill)
    return y + size + 8


def headline(draw, x, y, text, size, max_w, fill=INK, font_path=SERIF_B):
    fnt = font(font_path, size)
    leading = int(size * 1.08)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_globe(draw, cx, cy, r):
    """A globe half in smoke: blue disc, green continents, grey plumes."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 214, 235),
                 outline=INK, width=3)
    # night side shading
    draw.pieslice([cx - r, cy - r, cx + r, cy + r], 270, 90,
                  fill=(120, 170, 205))
    # continents (schematic blobs)
    draw.polygon([(cx - 78, cy - 30), (cx - 40, cy - 62), (cx - 8, cy - 48),
                  (cx - 22, cy - 6), (cx - 58, cy + 2)], fill=(74, 140, 74))
    draw.polygon([(cx + 12, cy - 58), (cx + 52, cy - 66), (cx + 78, cy - 30),
                  (cx + 58, cy - 2), (cx + 22, cy - 12)], fill=(74, 140, 74))
    draw.polygon([(cx - 30, cy + 34), (cx + 6, cy + 26), (cx + 30, cy + 52),
                  (cx - 2, cy + 72), (cx - 40, cy + 62)], fill=(94, 150, 84))
    # smoke plumes rising from the top
    for sx, sy, sr in [(cx - 55, cy - r - 12, 14), (cx - 30, cy - r - 26, 17),
                       (cx + 5, cy - r - 20, 13), (cx + 42, cy - r - 12, 15),
                       (cx + 62, cy - r - 28, 11)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 146, 136))
    # crack across the disc
    draw.line([(cx - 70, cy + 40), (cx - 30, cy + 18), (cx + 5, cy + 42),
               (cx + 45, cy + 20), (cx + 72, cy + 38)], fill=RED, width=4)


def draw_tanker(draw, x, y, w, h):
    """Tanker silhouette with flames and waves."""
    # flames
    for fx, fh in [(x + 30, 46), (x + 70, 60), (x + 115, 42), (x + 160, 55)]:
        draw.polygon([(fx - 14, y), (fx, y - fh), (fx + 14, y)],
                     fill=(232, 120, 20))
        draw.polygon([(fx - 7, y), (fx, y - fh + 18), (fx + 7, y)],
                     fill=(250, 200, 40))
    # hull
    draw.polygon([(x, y), (x + w, y), (x + w - 18, y + 26), (x + 14, y + 26)],
                 fill=(40, 40, 44))
    # deck containers
    draw.rectangle([x + 24, y - 26, x + 64, y], fill=(29, 78, 137))
    draw.rectangle([x + 70, y - 26, x + 110, y], fill=(164, 18, 18))
    draw.rectangle([x + 116, y - 26, x + 150, y], fill=(15, 118, 110))
    # bridge tower
    draw.rectangle([x + w - 52, y - 44, x + w - 22, y], fill=(70, 70, 76))
    # waves
    for i in range(5):
        wx = x + i * (w // 5)
        draw.arc([wx, y + 30, wx + 44, y + 52], 0, 180, fill=BLUE, width=3)


def draw_seismo(draw, x, y, w, h):
    """Seismograph zigzag on a strip."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    pts = []
    n = 26
    for i in range(n + 1):
        px = x + 6 + i * (w - 12) / n
        if i in (9, 10, 11, 12, 13):
            py = y + h / 2 + (h * 0.42 if i % 2 == 0 else -h * 0.42)
        elif i in (7, 8, 14, 15):
            py = y + h / 2 + (h * 0.2 if i % 2 == 0 else -h * 0.2)
        else:
            py = y + h / 2 + (3 if i % 2 == 0 else -3)
        pts.append((px, py))
    draw.line(pts, fill=RED, width=3, joint="curve")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    R = W - M  # right edge

    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # ---- top kicker bar ----
    y = 30
    d.text((M, y), "SUNDAY, 22 NOVEMBER 2026", font=font(SANS_B, 16), fill=INK)
    rt = "THE WORLD IN ONE IMAGE"
    d.text((R - d.textlength(rt, font=font(SANS_B, 16)), y), rt,
           font=font(SANS_B, 16), fill=RED)
    y = 58
    rule(d, M, y, R, 2)

    # ---- masthead ----
    mast = "THE WORLD"
    mf = font(SERIF_B, 108)
    d.text(((W - d.textlength(mast, font=mf)) / 2, 66), mast, font=mf, fill=INK)
    double_rule(d, M, 190, R)
    tag = "ONE DAY  ·  ONE PAGE  ·  EVERY STORY THAT MATTERED"
    tf = font(SANS_B, 15)
    d.text(((W - d.textlength(tag, font=tf)) / 2, 206), tag, font=tf, fill=GREY)

    # ---- lead story: COP31 ----
    y = 238
    y = kicker(d, M, y, "CLIMATE  ·  COP31, ANTALYA")
    y = headline(d, M, y, "FOSSIL FUELS SPLIT THE WORLD AS CLIMATE TALKS STALL",
                 40, 540)
    y += 6
    y = para(d, M, y,
             "Delegates from nearly 200 countries are deadlocked at the "
             "COP31 climate summit, with the fight over fossil fuels halting "
             "any new global deal. Draft text dropping a fossil-fuel "
             "phase-down drew fury from frontline states.",
             font(SANS, 18), 540)
    y += 8
    # stat strip
    d.rectangle([M, y, M + 540, y + 44], fill=INK)
    d.text((M + 14, y + 11), "200  COUNTRIES     ·     0  DEAL ON FOSSIL FUELS",
           font=font(SANS_B, 17), fill=PAPER)
    # globe illustration, right of lead
    draw_globe(d, 800, 382, 96)
    para(d, 640, 492,
         "ANTALYA — talks enter their final stretch with no deal in sight.",
         font(SANS, 13), 356, fill=GREY)
    rule(d, M, 528, R, 2)

    # ---- row 2: Gulf (left) / Peru + cartel (right) ----
    # left: Gulf war (fixed positions)
    kicker(d, M, 546, "THE GULF  ·  WAR, MONTH 9")
    headline(d, M, 574, "IRAN HITS U.S. BASES IN KUWAIT AND BAHRAIN", 27, 470)
    para(d, M, 638,
         "Tehran struck Ali Al Salem air base in Kuwait and a U.S. radar "
         "site in Bahrain, days after U.S. jets hit Qeshm Island. Tankers "
         "burned in Hormuz; oil flows halved.",
         font(SANS, 15), 470)
    draw_tanker(d, M + 8, 758, 200, 0)
    # right column, two stacked stories
    x2 = 540
    d.line([(x2 - 16, 546), (x2 - 16, 824)], fill=INK, width=1)
    kicker(d, x2, 546, "PERU  ·  MAGNITUDE 6.9")
    headline(d, x2, 574, "QUAKE SHAKES THE ANDES", 22, 440)
    para(d, x2, 606,
         "A magnitude 6.9 earthquake rattled Peru's Andes. No damage or "
         "casualties were immediately reported.",
         font(SANS, 14), 440)
    draw_seismo(d, x2, 650, 440, 34)
    rule(d, x2, 694, R, 1)
    kicker(d, x2, 704, "MEXICO  ·  SINALOA")
    headline(d, x2, 732, "CARTEL KINGPIN 'EL CHAPO ISIDRO' SEIZED", 22, 440)
    para(d, x2, 782,
         "Mexican special forces arrested the drug boss in a raid; 11 "
         "people were killed in the violence that followed.",
         font(SANS, 14), 440)
    rule(d, M, 824, R, 2)

    # ---- row 3: Ukraine / APEC (fixed positions) ----
    kicker(d, M, 840, "UKRAINE  ·  WAR")
    headline(d, M, 868, "400 DRONES, 110 MISSILES IN ONE NIGHT", 18, 470)
    para(d, M, 896,
         "Russia's largest barrage in weeks; debris crashed in Poland. "
         "Estonia says it will close its border with Russia.",
         font(SANS, 14), 470)
    kicker(d, x2, 840, "ASIA  ·  APEC, SHENZHEN")
    headline(d, x2, 868, "TRUMP MEETS XI — AND PUTIN", 20, 440)
    para(d, x2, 896,
         "Trump arrived in Shenzhen for the APEC summit, with a trilateral "
         "meeting with Xi Jinping and Vladimir Putin planned.",
         font(SANS, 14), 440)
    rule(d, M, 940, R, 2)

    # ---- in brief strip ----
    y = 952
    d.text((M, y), "IN BRIEF —", font=font(SANS_B, 14), fill=RED)
    para(d, M + 96, y,
         "Bolsonaro in ICU  ·  Princess of Wales films BBC documentary on "
         "life with cancer  ·  UK–EU agree youth mobility scheme  ·  "
         "India v New Zealand, 1st Test  ·  Cummins keeps Test captaincy",
         font(SANS, 14), R - M - 96)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
