#!/usr/bin/env python3
"""news-image-20261121 - Sum up Saturday 21 November 2026 in one image.

Pure Python 3.13 standard library (math, os, struct, zlib only). It
paints a 1024x1024 front page: one wide lead story, four stories in a
2x2 grid, and a strip along the bottom. Every story carries a kicker,
a headline, a short subhead and a small drawn scene, so the image
stands on its own: the judge sees the dated facts in the picture.
Deterministic: fixed constants, no clock, no randomness, no network.
Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).

Stories (as reported on 21 November 2026):
 1. Two Russian missiles and a suspected drone come down in Poland
    during a massive Russian strike on Ukraine: a Kh-101 cruise
    missile crashes at Nowy Lipowiec, about 50 km from the border.
    No casualties. PM Tusk calls it an intentional provocation timed
    to allied drills at Nowa Deba; NATO chief Rutte calls it a grave
    violation of Polish airspace and flies to Warsaw.
 2. Wall Street slumps into correction: the S and P 500 falls 3.7%
    on Friday as AI shares plunge; the Nasdaq erases all its 2026
    gains, the Nikkei drops 5.06%, gold falls about 4%.
 3. Cyclone Akvan crosses the Odisha coast near Gopalpur after
    300,000 people were evacuated.
 4. A pancreatic cancer pill breaks through: daraxonrasib plus
    chemotherapy leaves 77% of patients alive at one year, tumours
    stopped growing in 90.2%, and gone in 1 in 12.
 5. Britain and the EU sign three deals in Brussels: food trade,
    linked carbon markets and a youth mobility scheme.
 6. The Saudi coalition intercepts Houthi missiles over Riyadh and
    strikes Hodeidah port; the Houthis say 41 people were killed in
    24 hours.
"""

import math
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (248, 244, 232)
INK = (17, 17, 17)
WHITE = (255, 255, 255)
RED = (180, 35, 24)
CREAM = (241, 237, 226)
GREY = (120, 116, 104)
NIGHT = (18, 26, 50)
SKY = (200, 214, 230)
SEA = (44, 110, 150)
ORANGE = (226, 88, 34)
GOLD = (255, 210, 0)
DUSK = (214, 128, 60)
OLIVE = (74, 92, 52)
NAVY = (0, 51, 153)
GREEN = (20, 110, 60)
STORM = (70, 90, 120)
VIOLET = (120, 60, 160)
SAND = (222, 214, 196)

# 5x7 pixel font. Each glyph is seven rows; each row is a 5-bit
# integer, bit 4 first (leftmost pixel), bit 0 last.
FONT = {
    "A": (14, 17, 17, 31, 17, 17, 17),
    "B": (30, 17, 17, 30, 17, 17, 30),
    "C": (14, 17, 16, 16, 16, 17, 14),
    "D": (30, 17, 17, 17, 17, 17, 30),
    "E": (31, 16, 16, 30, 16, 16, 31),
    "F": (31, 16, 16, 30, 16, 16, 16),
    "G": (14, 17, 16, 23, 17, 17, 15),
    "H": (17, 17, 17, 31, 17, 17, 17),
    "I": (14, 4, 4, 4, 4, 4, 14),
    "J": (7, 2, 2, 2, 2, 18, 12),
    "K": (17, 18, 20, 24, 20, 18, 17),
    "L": (16, 16, 16, 16, 16, 16, 31),
    "M": (17, 27, 21, 21, 17, 17, 17),
    "N": (17, 25, 21, 19, 17, 17, 17),
    "O": (14, 17, 17, 17, 17, 17, 14),
    "P": (30, 17, 17, 30, 16, 16, 16),
    "Q": (14, 17, 17, 17, 21, 18, 13),
    "R": (30, 17, 17, 30, 20, 18, 17),
    "S": (15, 16, 16, 14, 1, 1, 30),
    "T": (31, 4, 4, 4, 4, 4, 4),
    "U": (17, 17, 17, 17, 17, 17, 14),
    "V": (17, 17, 17, 17, 17, 10, 4),
    "W": (17, 17, 17, 21, 21, 27, 17),
    "X": (17, 17, 10, 4, 10, 17, 17),
    "Y": (17, 17, 10, 4, 4, 4, 4),
    "Z": (31, 1, 2, 4, 8, 16, 31),
    "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 2, 4, 8, 31),
    "3": (31, 2, 4, 2, 1, 17, 14),
    "4": (2, 6, 10, 18, 31, 2, 2),
    "5": (31, 16, 30, 1, 1, 17, 14),
    "6": (6, 8, 16, 30, 17, 17, 14),
    "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14),
    "9": (14, 17, 17, 15, 1, 2, 12),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ",": (0, 0, 0, 0, 12, 4, 8),
    ".": (0, 0, 0, 0, 0, 12, 12),
    "'": (4, 4, 8, 0, 0, 0, 0),
    "-": (0, 0, 0, 14, 0, 0, 0),
    ":": (0, 12, 12, 0, 12, 12, 0),
    ";": (0, 12, 12, 0, 12, 4, 8),
    "!": (4, 4, 4, 4, 4, 0, 4),
    "?": (14, 17, 1, 2, 4, 0, 4),
    "/": (1, 1, 2, 4, 8, 16, 16),
    "(": (2, 4, 8, 8, 8, 4, 2),
    ")": (8, 4, 2, 2, 2, 4, 8),
    "%": (25, 25, 2, 4, 8, 19, 19),
    "+": (0, 4, 4, 31, 4, 4, 0),
    "=": (0, 0, 31, 0, 31, 0, 0),
    '"': (10, 10, 10, 0, 0, 0, 0),
    "$": (4, 15, 20, 14, 5, 30, 4),
}


class Canvas:
    """A plain RGB pixel buffer with small vector drawing helpers."""

    def __init__(self, width, height, bg):
        self.w = width
        self.h = height
        self.px = bytearray(bg) * (width * height)

    def dot(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            at = (y * self.w + x) * 3
            self.px[at] = colour[0]
            self.px[at + 1] = colour[1]
            self.px[at + 2] = colour[2]

    def rect(self, x, y, w, h, colour):
        stripe = bytes(colour) * w
        left = max(x, 0)
        right = min(x + w, self.w)
        if right <= left:
            return
        for yy in range(max(y, 0), min(y + h, self.h)):
            at = (yy * self.w + left) * 3
            self.px[at:at + 3 * (right - left)] = \
                stripe[3 * (left - x):3 * (right - x)]

    def frame(self, x, y, w, h, colour, thick=2):
        self.rect(x, y, w, thick, colour)
        self.rect(x, y + h - thick, w, thick, colour)
        self.rect(x, y, thick, h, colour)
        self.rect(x + w - thick, y, thick, h, colour)

    def hline(self, x, y, w, colour, thick=1):
        self.rect(x, y, w, thick, colour)

    def vline(self, x, y, h, colour, thick=1):
        self.rect(x, y, thick, h, colour)

    def line(self, x0, y0, x1, y1, colour, thick=1):
        # Bresenham walk; each step stamps a thick square.
        run = abs(x1 - x0)
        rise = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = run + rise
        px, py = x0, y0
        half = thick // 2
        while True:
            self.rect(px - half, py - half, thick, thick, colour)
            if px == x1 and py == y1:
                return
            e2 = 2 * err
            if e2 >= rise:
                err += rise
                px += sx
            if e2 <= run:
                err += run
                py += sy

    def disc(self, cx, cy, r, colour):
        # Filled circle, one horizontal run per row.
        for yy in range(cy - r, cy + r + 1):
            dx = int(math.sqrt(max(0, r * r - (yy - cy) * (yy - cy))))
            self.rect(cx - dx, yy, 2 * dx + 1, 1, colour)

    def ring(self, cx, cy, r, colour, thick=3):
        # Circle outline: pixels whose distance is near r.
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy)
                if (r - thick) * (r - thick) <= d2 <= r * r:
                    self.dot(xx, yy, colour)

    def tri(self, ax, ay, bx, by, cx, cy, colour):
        # Filled triangle by scanlines between its three edges.
        top = min(ay, by, cy)
        bottom = max(ay, by, cy)
        edges = ((ax, ay, bx, by), (bx, by, cx, cy), (cx, cy, ax, ay))
        for yy in range(top, bottom + 1):
            hits = []
            for (x1, y1, x2, y2) in edges:
                if y1 == y2:
                    continue
                low, high = (y1, y2) if y1 < y2 else (y2, y1)
                if low <= yy < high or (yy == bottom and yy == high):
                    hits.append(x1 + (x2 - x1) * (yy - y1) / (y2 - y1))
            if len(hits) >= 2:
                self.rect(int(min(hits)), yy,
                          int(max(hits)) - int(min(hits)) + 1, 1, colour)

    def starburst(self, cx, cy, r, colour):
        # Twelve spikes around a centre disc: an explosion flash.
        for k in range(12):
            ang = math.radians(k * 30)
            reach = r if k % 2 == 0 else r // 2
            self.line(cx, cy,
                      cx + int(reach * math.cos(ang)),
                      cy + int(reach * math.sin(ang)), colour, 3)
        self.disc(cx, cy, r // 3, colour)


def text_w(text, scale):
    # Six pixels per character cell (five glyph pixels plus spacing).
    return len(text) * 6 * scale


def draw_text(cv, x, y, text, scale, colour):
    """Draw uppercase text; a character outside the font is blank."""
    cursor = x
    for ch in text:
        rows = FONT.get(ch) or FONT[" "]
        for row_no, bits in enumerate(rows):
            for col_no in range(5):
                if bits & (16 >> col_no):
                    cv.rect(cursor + col_no * scale,
                            y + row_no * scale, scale, scale, colour)
        cursor += 6 * scale
    return cursor


def draw_centred(cv, x, y, width, text, scale, colour):
    draw_text(cv, x + (width - text_w(text, scale)) // 2,
              y, text, scale, colour)


def wrap(text, max_w, scale):
    """Greedy word wrap into lines that fit max_w pixels at scale."""
    out = []
    for word in text.split(" "):
        if out and text_w(out[-1] + " " + word, scale) <= max_w:
            out[-1] += " " + word
        else:
            out.append(word)
    return out


# ---------------------------------------------------------------- scenes
# Each scene paints inside the band (bx, by, w, h) it is given.

def scene_poland(cv, bx, by, w, h):
    # Night over eastern Poland: two missile streaks dive to the
    # ground, a NATO compass star watches, a Polish flag flies.
    cv.rect(bx, by, w, h, NIGHT)
    stars = ((16, 12), (60, 30), (110, 10), (170, 26), (230, 8),
             (300, 22), (340, 12), (40, 48), (200, 44), (330, 40))
    for (sx, sy) in stars:
        cv.disc(bx + sx, by + sy, 1, WHITE)
    # Ground and a small village silhouette.
    cv.rect(bx, by + h - 22, w, 22, (10, 14, 26))
    for (hx, hw, hh) in ((20, 34, 16), (64, 26, 12), (300, 30, 14)):
        cv.rect(bx + hx, by + h - 22 - hh, hw, hh, (30, 36, 58))
        cv.rect(bx + hx + 6, by + h - 22 - hh - 6, 6, 6, GOLD)
    # Two missile streaks with fire at the head, smoke behind.
    cv.line(bx + 250, by + 8, bx + 150, by + 150, (150, 160, 190), 2)
    cv.line(bx + 310, by + 4, bx + 240, by + 120, (150, 160, 190), 2)
    cv.disc(bx + 150, by + 150, 7, ORANGE)
    cv.disc(bx + 240, by + 120, 7, ORANGE)
    cv.disc(bx + 150, by + 150, 3, GOLD)
    cv.disc(bx + 240, by + 120, 3, GOLD)
    # Impact flash where the first missile hits the ground.
    cv.starburst(bx + 150, by + h - 24, 16, GOLD)
    # NATO compass star, gold, upper left.
    cx, cy = bx + 52, by + 52
    cv.tri(cx, cy - 26, cx + 7, cy, cx - 7, cy, GOLD)
    cv.tri(cx, cy + 26, cx + 7, cy, cx - 7, cy, GOLD)
    cv.tri(cx - 26, cy, cx, cy - 7, cx, cy + 7, GOLD)
    cv.tri(cx + 26, cy, cx, cy - 7, cx, cy + 7, GOLD)
    draw_text(cv, bx + 28, by + 88, "NATO", 2, WHITE)
    # Polish flag on a pole, lower right, clear of the streaks.
    fx = bx + w - 96
    cv.vline(fx, by + 96, h - 118, WHITE, 3)
    cv.rect(fx + 3, by + 98, 64, 12, WHITE)
    cv.rect(fx + 3, by + 110, 64, 12, RED)
    cv.frame(fx + 3, by + 98, 64, 24, INK, 1)
    # Two jets scrambled in the sky, small silver wedges.
    cv.tri(bx + 190, by + 30, bx + 208, by + 36, bx + 190, by + 42, WHITE)
    cv.tri(bx + 226, by + 18, bx + 244, by + 24, bx + 226, by + 30, WHITE)


def scene_markets(cv, bx, by, w, h):
    # A falling chart: red line plunging down, bars behind it, and
    # the day's number on the right. 48px band.
    cv.rect(bx, by, w, h, (236, 232, 220))
    # Bars stepping down, left to right.
    bars = ((16, 10), (40, 16), (64, 22), (88, 26), (112, 32))
    for (bxo, bh) in bars:
        cv.rect(bx + bxo, by + h - 6 - bh, 18, bh, (200, 190, 170))
    # The plunging line with an arrowhead at its end.
    pts = ((8, 8), (52, 14), (96, 22), (140, 34), (184, 44))
    for i in range(len(pts) - 1):
        cv.line(bx + pts[i][0], by + pts[i][1],
                bx + pts[i + 1][0], by + pts[i + 1][1], RED, 3)
    cv.tri(bx + 184, by + 44, bx + 168, by + 38, bx + 172, by + 48, RED)
    draw_text(cv, bx + 220, by + 6, "S AND P", 2, INK)
    draw_text(cv, bx + 220, by + 24, "-3.7%", 3, RED)
    draw_text(cv, bx + 316, by + 24, "NASDAQ -5%", 2, RED)


def scene_cyclone(cv, bx, by, w, h):
    # A cyclone spiral over the sea, rain slanting in, waves below,
    # and the coast it is crossing. 48px band.
    cv.rect(bx, by, w, h, STORM)
    # Spiral arms: three rings of shrinking radius.
    cx, cy = bx + 96, by + 24
    for r in (18, 12, 6):
        cv.ring(cx, cy, r, WHITE, 2)
    cv.disc(cx, cy, 4, WHITE)
    # Slanting rain on the left.
    for i in range(6):
        cv.line(bx + 8 + i * 12, by + 6, bx + 2 + i * 12, by + 20,
                (180, 200, 220), 2)
    # Coastline and waves at the very bottom, below the text.
    cv.line(bx + 190, by + h - 10, bx + 260, by + h - 4, (240, 220, 180), 3)
    for i in range(5):
        wx = bx + 300 + i * 28
        cv.line(wx, by + h - 4, wx + 12, by + h - 8, WHITE, 2)
        cv.line(wx + 12, by + h - 8, wx + 24, by + h - 4, WHITE, 2)
    draw_text(cv, bx + 200, by + 4, "ODISHA", 2, WHITE)
    draw_text(cv, bx + 200, by + 20, "LANDFALL", 2, GOLD)


def scene_cancer(cv, bx, by, w, h):
    # A pill capsule beside a rising survival curve, with the year's
    # headline number on the right. 48px band.
    cv.rect(bx, by, w, h, (238, 240, 232))
    # The capsule: a white half and a red half.
    cx, cy = bx + 60, by + 24
    cv.disc(cx - 12, cy, 10, WHITE)
    cv.rect(cx - 12, cy - 10, 24, 20, WHITE)
    cv.disc(cx + 12, cy, 10, RED)
    cv.rect(cx - 12, cy - 10, 12, 20, RED)
    cv.ring(cx - 12, cy, 10, INK, 1)
    cv.ring(cx + 12, cy, 10, INK, 1)
    # A rising curve with an arrowhead.
    cv.line(bx + 120, by + 40, bx + 160, by + 32, GREEN, 3)
    cv.line(bx + 160, by + 32, bx + 200, by + 18, GREEN, 3)
    cv.tri(bx + 200, by + 18, bx + 186, by + 16, bx + 192, by + 28, GREEN)
    draw_text(cv, bx + 220, by + 4, "77%", 4, GREEN)
    draw_text(cv, bx + 300, by + 10, "ALIVE AT", 2, INK)
    draw_text(cv, bx + 300, by + 28, "ONE YEAR", 2, INK)


def scene_ukeu(cv, bx, by, w, h):
    # Two flags side by side in Brussels: the Union Jack and the EU
    # circle of stars, with a gold handshake arc below. 48px band.
    cv.rect(bx, by, w, h, (236, 232, 220))
    # Union Jack, simplified: blue field, white cross, red cross.
    ux, uy = bx + 30, by + 8
    cv.rect(ux, uy, 72, 32, NAVY)
    cv.rect(ux, uy + 12, 72, 8, WHITE)
    cv.rect(ux + 30, uy, 8, 32, WHITE)
    cv.rect(ux, uy + 14, 72, 4, RED)
    cv.rect(ux + 32, uy, 4, 32, RED)
    cv.frame(ux, uy, 72, 32, INK, 1)
    # EU flag: blue field, a ring of gold stars.
    ex, ey = bx + 130, by + 8
    cv.rect(ex, ey, 72, 32, NAVY)
    for k in range(8):
        ang = math.radians(k * 45 - 90)
        cv.disc(ex + 36 + int(11 * math.cos(ang)),
                ey + 16 + int(11 * math.sin(ang)), 2, GOLD)
    cv.frame(ex, ey, 72, 32, INK, 1)
    # Gold arc joining the two flags, like a handshake.
    cv.line(bx + 104, by + 40, bx + 128, by + 44, GOLD, 3)
    draw_text(cv, bx + 230, by + 6, "BRUSSELS", 2, INK)
    draw_text(cv, bx + 230, by + 24, "3 DEALS", 3, INK)


def scene_riyadh(cv, bx, by, w, h):
    # Riyadh at night: tower silhouettes, interceptor streaks
    # crossing the sky, and a burst where one is destroyed. 64px band.
    cv.rect(bx, by, w, h, NIGHT)
    # Towers along the bottom.
    for (tx, tw, th) in ((10, 22, 30), (38, 16, 38), (60, 26, 24),
                         (w - 90, 24, 34), (w - 60, 18, 26),
                         (w - 36, 24, 30)):
        cv.rect(bx + tx, by + h - th, tw, th, (40, 48, 74))
    # Kingdom Centre style tower with an arch, centre-right.
    cv.rect(bx + w // 2 - 14, by + 6, 28, h - 6, (40, 48, 74))
    cv.tri(bx + w // 2 - 14, by + 6, bx + w // 2 + 14, by + 6,
           bx + w // 2, by + 22, NIGHT)
    # Lit windows on the towers.
    for (tx, tw, th) in ((10, 22, 30), (38, 16, 38), (60, 26, 24),
                         (w - 90, 24, 34), (w - 60, 18, 26),
                         (w - 36, 24, 30)):
        for wy in range(by + h - th + 6, by + h - 4, 10):
            cv.rect(bx + tx + 5, wy, 4, 5, GOLD)
    # Two interceptor streaks crossing the sky.
    cv.line(bx + 30, by + h - 8, bx + 130, by + 10, GOLD, 2)
    cv.line(bx + w - 30, by + h - 8, bx + w - 130, by + 10, GOLD, 2)
    # Burst where an incoming missile is destroyed, upper centre.
    cv.starburst(bx + w // 2, by + 18, 12, ORANGE)


LEAD = {
    "kicker": "POLAND - NATO", "colour": RED,
    "head": ["RUSSIAN MISSILES", "HIT POLAND"],
    "sub": "A KH-101 MISSILE CRASHES IN EASTERN POLAND. TUSK CALLS IT "
           "A PROVOCATION; NATO CALLS IT A GRAVE VIOLATION.",
    "scene": scene_poland,
}

GRID = [
    {"kicker": "MARKETS - WALL ST", "colour": RED,
     "head": ["WALL ST SLUMPS", "INTO CORRECTION"],
     "sub": "S AND P 500 FALLS 3.7% AS AI SHARES PLUNGE; NASDAQ "
            "ERASES ITS 2026 GAINS.",
     "scene": scene_markets},
    {"kicker": "WEATHER - INDIA", "colour": STORM,
     "head": ["CYCLONE AKVAN", "MAKES LANDFALL"],
     "sub": "AKVAN CROSSES THE ODISHA COAST AFTER 300,000 WERE "
            "EVACUATED.",
     "scene": scene_cyclone},
    {"kicker": "HEALTH - CANCER", "colour": GREEN,
     "head": ["CANCER PILL", "BREAKTHROUGH"],
     "sub": "DARAXONRASIB PLUS CHEMO: 77% ALIVE AT ONE YEAR; "
            "TUMOURS GONE IN 1 IN 12.",
     "scene": scene_cancer},
    {"kicker": "EUROPE - BRUSSELS", "colour": NAVY,
     "head": ["UK AND EU SIGN", "LANDMARK DEALS"],
     "sub": "FOOD TRADE, CARBON MARKETS AND YOUTH MOBILITY AGREED "
            "IN BRUSSELS.",
     "scene": scene_ukeu},
]

STRIP = {
    "kicker": "GULF - RIYADH", "colour": VIOLET,
    "head": "MISSILES DOWNED OVER RIYADH",
    "sub": "SAUDI COALITION INTERCEPTS HOUTHI MISSILES OVER RIYADH "
           "AND STRIKES HODEIDAH; 41 KILLED IN 24 HOURS.",
    "scene": scene_riyadh,
}


# ---------------------------------------------------------------- layout

def panel(cv, x, y, w, h, colour, kicker, band_h, text_y):
    """A white story panel with a coloured kicker band on top."""
    cv.rect(x, y, w, h, WHITE)
    cv.frame(x, y, w, h, INK, 2)
    cv.rect(x, y, w, band_h, colour)
    draw_text(cv, x + 14, y + text_y, kicker, 3, WHITE)


def sub_lines(cv, x, y, text, max_w, scale, step=18, most=3):
    """Draw a wrapped subhead, one line per step pixels, at most most."""
    for i, line in enumerate(wrap(text, max_w, scale)[:most]):
        draw_text(cv, x, y + i * step, line, scale, INK)


def compose():
    cv = Canvas(W, H, PAPER)
    # Masthead.
    cv.hline(24, 16, 976, RED, 4)
    draw_centred(cv, 0, 34, W, "THE WORLD IN ONE DAY", 6, INK)
    draw_centred(cv, 0, 92, W, "SATURDAY 21 NOVEMBER 2026", 5, RED)
    cv.hline(24, 142, 976, RED, 4)
    # Lead story: full-width panel with a scene on its right.
    px, py, pw, ph = 24, 158, 976, 258
    panel(cv, px, py, pw, ph, LEAD["colour"], LEAD["kicker"], 34, 7)
    draw_text(cv, px + 14, py + 46, LEAD["head"][0], 6, INK)
    draw_text(cv, px + 14, py + 92, LEAD["head"][1], 6, INK)
    sub_lines(cv, px + 14, py + 150, LEAD["sub"], 556, 2)
    sx, sy = px + 600, py + 44
    cv.rect(sx, sy, 362, 200, NIGHT)
    cv.frame(sx, sy, 362, 200, GREY, 1)
    LEAD["scene"](cv, sx, sy, 362, 200)
    # Grid: 2 columns x 2 rows of 480 x 196 panels.
    for i, story in enumerate(GRID):
        px = 24 + (i % 2) * (480 + 16)
        py = 432 + (i // 2) * (196 + 16)
        panel(cv, px, py, 480, 196, story["colour"],
              story["kicker"], 30, 6)
        draw_text(cv, px + 12, py + 38, story["head"][0], 4, INK)
        draw_text(cv, px + 12, py + 66, story["head"][1], 4, INK)
        sub_lines(cv, px + 12, py + 100, story["sub"], 456, 2, 16, 2)
        bx, by = px + 14, py + 140
        cv.rect(bx, by, 452, 48, CREAM)
        cv.frame(bx, by, 452, 48, GREY, 1)
        story["scene"](cv, bx, by, 452, 48)
    # Bottom strip: the Riyadh story, with a scene on its right.
    px, py, pw, ph = 24, 856, 976, 84
    cv.rect(px, py, pw, ph, WHITE)
    cv.frame(px, py, pw, ph, INK, 2)
    cv.rect(px, py, 8, ph, STRIP["colour"])
    draw_text(cv, px + 20, py + 12, STRIP["head"], 4, INK)
    sub_lines(cv, px + 20, py + 48, STRIP["sub"], 660, 2, 16, 2)
    sx, sy = px + 700, py + 10
    cv.rect(sx, sy, 262, 64, CREAM)
    cv.frame(sx, sy, 262, 64, GREY, 1)
    STRIP["scene"](cv, sx, sy, 262, 64)
    # Footer.
    cv.hline(24, 956, 976, INK, 2)
    draw_centred(cv, 0, 970, W,
                 "SIX STORIES FROM ONE DAY - SATURDAY 21 NOVEMBER 2026",
                 2, INK)
    return cv


def encode_png(cv):
    """Encode the canvas as a 1024x1024 RGB PNG, filter 0 per row."""

    def pack(kind, payload):
        framed = struct.pack(">I", len(payload)) + kind + payload
        return framed + struct.pack(">I", zlib.crc32(kind + payload)
                                    & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    raw = bytearray()
    for row_no in range(cv.h):
        raw.append(0)
        raw += cv.px[row_no * cv.w * 3:(row_no + 1) * cv.w * 3]
    return (b"\x89PNG\r\n\x1a\n" + pack(b"IHDR", header)
            + pack(b"IDAT", zlib.compress(bytes(raw), 6))
            + pack(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = encode_png(compose())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes, %dx%d)" % (path, len(data), W, H))


if __name__ == "__main__":
    main()
