#!/usr/bin/env python3
"""Draw Wednesday 25 November 2026's world news as one newspaper front page.

Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR / $OUTPUT_DIR).
Deterministic: no network, no clock, no randomness. PIL only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (24, 58, 110)
GREY = (90, 88, 80)
LIGHT = (232, 226, 210)


def font(name, size):
    paths = {
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    }
    try:
        return ImageFont.truetype(paths[name], size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.25):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def headline(draw, x, y, text, fnt, width, fill=INK, leading=1.08):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 44  # margin

    # ---- Masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((m, 18), "THE WORLD IN ONE DAY", font=font("serif_b", 52),
           fill=(247, 243, 232))
    d.text((m, 82), "WEDNESDAY  25  NOVEMBER  2026",
           font=font("sans_b", 22), fill=(214, 178, 60))
    d.text((W - m - 250, 82), "SIX STORIES  \u00b7  ONE DAY",
           font=font("sans_b", 20), fill=(214, 178, 60))
    d.rectangle([0, 118, W, 124], fill=RED)

    y = 140
    # ---- Lead story: CIA / ODNI hack ----
    d.text((m, y), "CYBERATTACK  \u00b7  WASHINGTON", font=font("sans_b", 20), fill=RED)
    y += 30
    y = headline(d, m, y, "CIA and US spy chief's office hit by hack",
                 font("serif_b", 42), W - 2 * m - 210)
    y += 6
    y = para(d, m, y,
             "An unclassified network used by the CIA and the Office of the "
             "Director of National Intelligence to analyse open-source "
             "material was breached, US officials said. No classified "
             "systems were hit, but it is the latest in a string of "
             "breaches across US federal agencies.",
             font("sans", 20), W - 2 * m - 210)
    # drawn padlock / shield emblem, right of lead text
    cx, cy = W - m - 80, 250
    d.polygon([(cx, cy - 62), (cx + 72, cy - 30), (cx + 72, cy + 28),
               (cx, cy + 66), (cx - 72, cy + 28), (cx - 72, cy - 30)],
              outline=BLUE, width=5)
    d.rectangle([cx - 26, cy - 8, cx + 26, cy + 34], fill=BLUE)
    d.arc([cx - 22, cy - 38, cx + 22, cy + 6], 180, 360, fill=BLUE, width=7)
    d.text((cx - 5, cy + 2), "!", font=font("sans_b", 26), fill=PAPER)
    d.text((cx - 52, cy + 76), "OPEN-SOURCE", font=font("sans_b", 15), fill=GREY)
    d.text((cx - 42, cy + 96), "NETWORK", font=font("sans_b", 15), fill=GREY)

    y += 14
    d.line([(m, y), (W - m, y)], fill=INK, width=3)
    y += 16

    # ---- Story 2: Riyadh tower ----
    d.text((m, y), "MIDDLE EAST  \u00b7  RIYADH", font=font("sans_b", 20), fill=RED)
    y += 30
    y = headline(d, m, y, "Houthis hit Riyadh's tallest tower again; 11 wounded",
                 font("serif_b", 32), W - 2 * m)
    y += 6
    y = para(d, m, y,
             "A Houthi drone struck the PIF Tower, home of Saudi Arabia's "
             "sovereign wealth fund, for the second time in less than a "
             "week. Saudi civil defence reported 11 people wounded and "
             "damage halfway up the landmark's facade.",
             font("sans", 19), W - 2 * m)
    y += 12
    d.line([(m, y), (W - m, y)], fill=INK, width=2)
    y += 16

    # ---- Story 3: Ukraine / Sparta II ----
    d.text((m, y), "WAR IN UKRAINE  \u00b7  GULF OF FINLAND", font=font("sans_b", 20), fill=RED)
    y += 30
    y = headline(d, m, y, "Zelenskyy confirms Ukraine struck Russian ship Sparta II",
                 font("serif_b", 32), W - 2 * m)
    y += 6
    y = para(d, m, y,
             "President Volodymyr Zelenskyy said Ukraine was behind "
             "Saturday's drone strike on the Russian cargo ship in the "
             "Gulf of Finland, calling the vessel a legitimate military "
             "target. Ally Norway urged Kyiv to exercise caution.",
             font("sans", 19), W - 2 * m)
    y += 12
    d.line([(m, y), (W - m, y)], fill=INK, width=2)
    y += 16

    # ---- Bottom row: three short stories ----
    col_w = (W - 2 * m - 2 * 24) // 3
    cols = [
        ("TECH  \u00b7  NEW YORK", "Huawei found guilty in US trial",
         "A jury convicted China's Huawei on 10 of 12 criminal counts, "
         "including stealing trade secrets, after a three-month trial."),
        ("TRADE  \u00b7  WASHINGTON", "Trump set to unveil new tariffs",
         "The Trump administration is poised to release findings of a "
         "probe into excess factory capacity in 16 trading partners."),
        ("HEALTH  \u00b7  CONGO", "WHO flees Ebola hospital amid fighting",
         "Health workers were evacuated from a hospital in Akwe, Ituri, "
         "after sheltering there for three days as fighting raged."),
    ]
    top = y
    max_y = top
    for i, (kicker, head, body) in enumerate(cols):
        x = m + i * (col_w + 24)
        d.rectangle([x, top, x + col_w, top + 6], fill=RED)
        yy = top + 16
        yy = para(d, x, yy, kicker, font("sans_b", 16), col_w, fill=RED, leading=1.2)
        yy += 4
        yy = headline(d, x, yy, head, font("serif_b", 22), col_w)
        yy += 4
        yy = para(d, x, yy, body, font("sans", 15), col_w, leading=1.25)
        max_y = max(max_y, yy)

    # ---- Footer ----
    fy = 972
    d.line([(m, fy - 14), (W - m, fy - 14)], fill=INK, width=2)
    d.text((m, fy), "Sources: Reuters  \u00b7  CNN  \u00b7  The New York Times  \u00b7  Associated Press",
           font=font("sans", 16), fill=GREY)
    d.text((W - m - 118, fy), "25 NOV 2026", font=font("sans_b", 16), fill=GREY)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.environ.get("OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
