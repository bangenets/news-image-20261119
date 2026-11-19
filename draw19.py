#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news summary image (1024x1024 PNG).

One-day newspaper front page: masthead with the date, one lead story and
four further stories, each with a simple code-drawn flat icon, plus an
"Also today" strip. All facts verified against wire reporting of the day.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
NAVY = (16, 38, 63)
NAVY2 = (24, 54, 86)
GOLD = (245, 197, 66)
RED = (178, 34, 34)
INK = (24, 24, 24)
GREY = (96, 96, 96)
CARD = (255, 255, 255)
BORDER = (210, 205, 192)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, max_w, fill, spacing=4, max_lines=None):
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


# ---------------------------------------------------------------- icons
def icon_globe_flags(d, x, y, s):
    """Globe with three small flags (China, Russia, US) on poles."""
    cx, cy, r = x + s // 2, y + s // 2 + 8, s // 2 - 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 130, 190),
              outline=(16, 38, 63), width=3)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=(255, 255, 255), width=2)
    for yy in (-0.55, 0, 0.55):
        d.arc([cx - r, cy + int(r * yy) - int(r * 0.45), cx + r, cy + int(r * yy) + int(r * 0.45)],
              200, 340, fill=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    # three flag poles
    flags = [((214, 38, 38), None), (None, "ru"), (None, "us")]
    fx = [x + 8, x + s // 2 - 14, x + s - 46]
    for i, (col, kind) in enumerate(flags):
        px = fx[i]
        d.line([px + 12, y + 2, px + 12, y + 40], fill=(60, 60, 60), width=3)
        if kind is None:
            d.rectangle([px + 12, y + 2, px + 38, y + 20], fill=col)
            d.ellipse([px + 18, y + 7, px + 24, y + 13], fill=(245, 197, 66))
        elif kind == "ru":
            d.rectangle([px + 12, y + 2, px + 38, y + 20], fill=(255, 255, 255))
            d.rectangle([px + 12, y + 8, px + 38, y + 14], fill=(0, 57, 166))
            d.rectangle([px + 12, y + 14, px + 38, y + 20], fill=(214, 38, 38))
        else:
            d.rectangle([px + 12, y + 2, px + 38, y + 20], fill=(255, 255, 255))
            for k in range(3):
                d.rectangle([px + 12, y + 2 + k * 6, px + 38, y + 5 + k * 6], fill=(178, 34, 34))
            d.rectangle([px + 12, y + 2, px + 23, y + 11], fill=(0, 40, 104))


def icon_controller(d, x, y, s):
    """Game controller."""
    cx, cy = x + s // 2, y + s // 2
    d.rounded_rectangle([x + 18, cy - 34, x + s - 18, cy + 40], radius=22,
                        fill=(30, 30, 46), outline=(16, 38, 63), width=3)
    d.rounded_rectangle([x + 18, cy - 34, x + s - 18, cy + 40], radius=22, outline=(245, 197, 66), width=2)
    # D-pad
    d.rectangle([x + 40, cy - 16, x + 52, cy + 8], fill=(240, 240, 240))
    d.rectangle([x + 34, cy - 10, x + 58, cy + 2], fill=(240, 240, 240))
    # buttons
    for bx, by, col in ((x + s - 62, cy - 14, (214, 38, 38)), (x + s - 46, cy - 2, (58, 130, 190)),
                        (x + s - 78, cy - 2, (58, 160, 90)), (x + s - 62, cy + 10, (245, 197, 66))):
        d.ellipse([bx, by, bx + 12, by + 12], fill=col)
    # joysticks
    d.ellipse([cx - 22, cy + 10, cx - 6, cy + 26], fill=(120, 120, 120))
    d.ellipse([cx + 8, cy + 10, cx + 24, cy + 26], fill=(120, 120, 120))


def icon_gavel(d, x, y, s):
    """Judge's gavel (diagonal) over its sound block."""
    import math as _m
    cx, cy = x + s // 2, y + s // 2 - 6
    # handle: diagonal from lower-left to upper-right
    d.line([cx - 38, cy + 38, cx + 26, cy - 26], fill=(120, 72, 20), width=10)
    # head: rectangle perpendicular to the handle, centred on its top end
    hx, hy = cx + 26, cy - 26
    p = (0.7071, 0.7071)   # perpendicular to handle
    h = (0.7071, -0.7071)  # along handle
    L, Wd = 30, 12
    pts = [(hx + L * p[0] + Wd * h[0], hy + L * p[1] + Wd * h[1]),
           (hx + L * p[0] - Wd * h[0], hy + L * p[1] - Wd * h[1]),
           (hx - L * p[0] - Wd * h[0], hy - L * p[1] - Wd * h[1]),
           (hx - L * p[0] + Wd * h[0], hy - L * p[1] + Wd * h[1])]
    d.polygon(pts, fill=(90, 50, 10), outline=(245, 197, 66))
    # sound block
    d.rounded_rectangle([cx - 42, cy + 48, cx + 42, cy + 60], radius=6, fill=(120, 72, 20))


def icon_euro(d, x, y, s):
    """Gold coin with a euro sign."""
    cx, cy, r = x + s // 2, y + s // 2 - 8, s // 2 - 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 197, 66), outline=(180, 130, 20), width=4)
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], outline=(180, 130, 20), width=2)
    d.text((cx, cy), "€", font=font(FB, 64), fill=(120, 80, 10), anchor="mm")
    d.text((cx, y + s - 26), "€45 BILLION", font=font(FB, 20), fill=(60, 60, 60), anchor="ma")


def icon_vangogh(d, x, y, s):
    """Framed picture: swirling night sky in Van Gogh's manner."""
    d.rectangle([x + 12, y + 12, x + s - 12, y + s - 12], fill=(245, 197, 66))
    d.rectangle([x + 22, y + 22, x + s - 22, y + s - 22], fill=(24, 54, 120))
    cx, cy = x + s // 2, y + s // 2
    for r in (18, 34, 50):
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 60, fill=(245, 197, 66), width=5)
    for sx, sy in ((x + 40, y + 40), (x + s - 48, y + 52), (x + 52, y + s - 44)):
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 255, 200))
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 220, 100))
    d.arc([x + 30, y + s - 60, x + s - 30, y + s - 10], 180, 360, fill=(20, 90, 50), width=6)


def icon_chip(d, x, y, s):
    """Microchip with a rising chart arrow (stock debut)."""
    cx, cy = x + s // 2, y + s // 2 - 6
    for i in range(4):
        px = x + 34 + i * 26
        d.line([px, cy - 52, px, cy - 38], fill=(90, 90, 90), width=4)
        d.line([px, cy + 38, px, cy + 52], fill=(90, 90, 90), width=4)
        py = y + 34 + i * 26
        d.line([cx - 52, py, cx - 38, py], fill=(90, 90, 90), width=4)
        d.line([cx + 38, py, cx + 52, py], fill=(90, 90, 90), width=4)
    d.rectangle([cx - 38, cy - 38, cx + 38, cy + 38], fill=(16, 38, 63), outline=(245, 197, 66), width=3)
    d.rectangle([cx - 18, cy - 18, cx + 18, cy + 18], fill=(58, 130, 190))
    d.text((cx, cy), "AI", font=font(FB, 24), fill=(255, 255, 255), anchor="mm")
    pts = [(x + 22, y + s - 22), (x + 52, y + s - 44), (x + 76, y + s - 34), (x + 112, y + s - 58), (x + s - 22, y + s - 66)]
    d.line(pts, fill=(34, 160, 90), width=5)
    d.polygon([(x + s - 22, y + s - 66), (x + s - 38, y + s - 64), (x + s - 24, y + s - 50)], fill=(34, 160, 90))


def icon_bridge(d, x, y, s):
    deck_y = y + s // 2
    d.line([x + 8, deck_y, x + s // 2 - 26, deck_y], fill=(70, 70, 70), width=8)
    d.line([x + s // 2 + 26, deck_y, x + s - 8, deck_y], fill=(70, 70, 70), width=8)
    for tx in (x + 34, x + s - 52):
        d.rectangle([tx, deck_y - 52, tx + 14, deck_y], fill=(178, 34, 34))
        d.line([tx + 7, deck_y - 52, tx + 7, deck_y - 72], fill=(178, 34, 34), width=3)
    d.line([x + 41, deck_y - 66, x + s // 2 - 26, deck_y], fill=(150, 150, 150), width=2)
    d.line([x + s - 45, deck_y - 66, x + s // 2 + 26, deck_y], fill=(150, 150, 150), width=2)
    # broken middle: falling span + smoke
    d.line([x + s // 2 - 18, deck_y + 6, x + s // 2 + 4, deck_y + 30], fill=(70, 70, 70), width=6)
    for ox, oy, r in ((-14, -16, 9), (2, -26, 11), (16, -12, 8)):
        d.ellipse([x + s // 2 + ox - r, deck_y + oy - r, x + s // 2 + ox + r, deck_y + oy + r],
                  fill=(190, 190, 190))
    for wy in (deck_y + 44, deck_y + 58):
        d.arc([x + 16, wy - 8, x + s - 16, wy + 8], 0, 180, fill=(58, 130, 190), width=3)


def icon_capitol(d, x, y, s):
    cx = x + s // 2
    base_y = y + s - 26
    d.rectangle([x + 22, base_y - 12, x + s - 22, base_y], fill=(90, 90, 90))
    d.rectangle([x + 34, base_y - 46, x + s - 34, base_y - 12], fill=(120, 120, 120))
    for i in range(5):
        colx = x + 44 + i * ((s - 88) // 4)
        d.rectangle([colx, base_y - 42, colx + 8, base_y - 14], fill=(240, 240, 240))
    d.pieslice([cx - 34, base_y - 96, cx + 34, base_y - 28], 180, 360, fill=(178, 34, 34))
    d.rectangle([cx - 40, base_y - 50, cx + 40, base_y - 44], fill=(90, 90, 90))
    d.line([cx, base_y - 96, cx, base_y - 112], fill=(60, 60, 60), width=3)
    d.ellipse([cx - 4, base_y - 118, cx + 4, base_y - 110], fill=(245, 197, 66))


def icon_virus(d, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 34
    for k in range(12):
        a = math.radians(k * 30)
        x1, y1 = cx + int(r * 0.8 * math.cos(a)), cy + int(r * 0.8 * math.sin(a))
        x2, y2 = cx + int((r + 16) * math.cos(a)), cy + int((r + 16) * math.sin(a))
        d.line([x1, y1, x2, y2], fill=(178, 34, 34), width=5)
        d.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=(178, 34, 34))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 38, 38), outline=(120, 10, 10), width=3)
    for ox, oy, rr in ((-14, -10, 9), (12, 6, 11), (-2, 16, 7)):
        d.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr], fill=(245, 120, 120))


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin

    # masthead
    d.rectangle([M, M, W - M, 150], fill=NAVY)
    d.text((W // 2, 40), "THE WORLD IN ONE DAY", font=font(FB, 54),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 106), "THURSDAY, 19 NOVEMBER 2026", font=font(FB, 36),
           fill=GOLD, anchor="ma")

    # ---- lead story
    ly0, ly1 = 166, 440
    d.rectangle([M, ly0, W - M, ly1], fill=CARD, outline=BORDER, width=2)
    d.rectangle([M, ly0, M + 10, ly1], fill=RED)
    # icon panel
    d.rectangle([M + 26, ly0 + 20, M + 26 + 250, ly1 - 20], fill=(226, 238, 247))
    icon_globe_flags(d, M + 26, ly0 + 20, 250)
    tx = M + 26 + 250 + 24
    tw = W - M - tx - 20
    d.text((tx, ly0 + 22), "LEAD  •  SUMMIT  •  SHENZHEN", font=font(FB, 20), fill=RED)
    y = text_block(d, (tx, ly0 + 52),
                   "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
                   font(FB, 33), tw, INK, spacing=2, max_lines=3)
    text_block(d, (tx, y + 8),
               "The leaders of the three nuclear powers hold a first trilateral. "
               "Trump presses arms control, but no major deal is expected.",
               font(FR, 22), tw, (60, 60, 60), spacing=3, max_lines=3)

    # ---- 2x2 grid
    cards = [
        ("GAMING", "GTA VI ROLLS OUT AFTER 13-YEAR WAIT",
         "Gamers enter Vice City as GTA VI begins its global launch.",
         icon_controller, (226, 232, 247)),
        ("US POLITICS", "JEFFRIES NOMINATED FOR HOUSE SPEAKER",
         "Jeffries is set to become the first Black Speaker of the House.",
         icon_gavel, (232, 228, 244)),
        ("EUROPE", "EU PROPOSES €45BN UKRAINE LOAN",
         "Repaid from Russian reparations, the EU says.",
         icon_euro, (247, 236, 200)),
        ("TECH", "ANTHROPIC POISED FOR $1.4TN STOCK DEBUT",
         "Claude's maker is set for a debut valued above $1.4 trillion.",
         icon_chip, (226, 244, 232)),
    ]
    gx0, gy0 = M, 456
    cw, chh, gap = 476, 210, 16
    for i, (kicker, head, sub, icon, bg) in enumerate(cards):
        cx = gx0 + (i % 2) * (cw + gap)
        cy = gy0 + (i // 2) * (chh + gap)
        d.rectangle([cx, cy, cx + cw, cy + chh], fill=CARD, outline=BORDER, width=2)
        d.rectangle([cx + 12, cy + 12, cx + 12 + 150, cy + chh - 12], fill=bg)
        icon(d, cx + 12, cy + 12, 150)
        tx = cx + 12 + 150 + 16
        tw = cx + cw - tx - 14
        d.text((tx, cy + 16), kicker, font=font(FB, 18), fill=RED)
        y = text_block(d, (tx, cy + 42), head, font(FB, 25), tw, INK, spacing=2, max_lines=3)
        text_block(d, (tx, y + 6), sub, font(FR, 19), tw, (60, 60, 60), spacing=2, max_lines=2)

    # ---- also today strip
    ay0, ay1 = 908, 972
    d.rectangle([M, ay0, W - M, ay1], fill=(232, 238, 244), outline=BORDER, width=2)
    d.text((M + 18, ay0 + 10), "ALSO TODAY", font=font(FB, 20), fill=NAVY)
    text_block(d, (M + 18, ay0 + 34),
               "Cyclone Akvan bears down on India's east coast  •  "
               "Van Gogh sells for a record $190.4m after a Nazi-era row",
               font(FR, 19), W - 2 * M - 36, INK, spacing=2, max_lines=1)

    # ---- footer
    d.text((W // 2, 984), "Sources: Reuters  •  The New York Times  •  Associated Press  •  BBC  •  European Union",
           font=font(FR, 15), fill=GREY, anchor="ma")

    out = "/tmp/entry19.png"
    img.save(out, "PNG", optimize=True)
    import os
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
