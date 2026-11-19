#!/usr/bin/env python3
"""news-image-20261119 - make.fun entry.

Draws a 1024x768 newspaper-style front page PNG summarising world news
for Thursday 19 November 2026. Pure Python 3 standard library (zlib,
struct). Deterministic bytes: no randomness, no network, no time.
"""
import os
import struct
import zlib

# ---------------------------------------------------------------- constants
W, H = 1024, 768
PAPER = (244, 240, 229)
INK = (26, 26, 31)
RED = (156, 32, 32)
BLUE = (28, 50, 104)
GREY = (108, 106, 100)
LGREY = (170, 167, 158)
WHITE = (250, 248, 242)
GOLD = (154, 120, 48)

def _outdir():
    d = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
    os.makedirs(d, exist_ok=True)
    return d

# ------------------------------------------------------------------ font 5x7
# Each glyph: list of 7 rows, 5 biper row, MSB left.
FONT = {
    'A': [0x0E,0x11,0x11,0x1F,0x11,0x11,0x11],
    'B': [0x1E,0x11,0x11,0x1E,0x11,0x11,0x1E],
    'C': [0x0E,0x11,0x10,0x10,0x10,0x11,0x0E],
    'D': [0x1E,0x11,0x11,0x11,0x11,0x11,0x1E],
    'E': [0x1F,0x10,0x10,0x1E,0x10,0x10,0x1F],
    'F': [0x1F,0x10,0x10,0x1E,0x10,0x10,0x10],
    'G': [0x0E,0x11,0x10,0x17,0x11,0x11,0x0F],
    'H': [0x11,0x11,0x11,0x1F,0x11,0x11,0x11],
    'I': [0x0E,0x04,0x04,0x04,0x04,0x04,0x0E],
    'J': [0x07,0x02,0x02,0x02,0x02,0x12,0x0C],
    'K': [0x11,0x12,0x14,0x18,0x14,0x12,0x11],
    'L': [0x10,0x10,0x10,0x10,0x10,0x10,0x1F],
    'M': [0x11,0x1B,0x15,0x15,0x11,0x11,0x11],
    'N': [0x11,0x19,0x15,0x13,0x11,0x11,0x11],
    'O': [0x0E,0x11,0x11,0x11,0x11,0x11,0x0E],
    'P': [0x1E,0x11,0x11,0x1E,0x10,0x10,0x10],
    'Q': [0x0E,0x11,0x11,0x11,0x15,0x12,0x0D],
    'R': [0x1E,0x11,0x11,0x1E,0x14,0x12,0x11],
    'S': [0x0F,0x10,0x10,0x0E,0x01,0x01,0x1E],
    'T': [0x1F,0x04,0x04,0x04,0x04,0x04,0x04],
    'U': [0x11,0x11,0x11,0x11,0x11,0x11,0x0E],
    'V': [0x11,0x11,0x11,0x11,0x11,0x0A,0x04],
    'W': [0x11,0x11,0x11,0x15,0x15,0x1B,0x11],
    'X': [0x11,0x11,0x0A,0x04,0x0A,0x11,0x11],
    'Y': [0x11,0x11,0x0A,0x04,0x04,0x04,0x04],
    'Z': [0x1F,0x01,0x02,0x04,0x08,0x10,0x1F],
    '0': [0x0E,0x11,0x13,0x15,0x19,0x11,0x0E],
    '1': [0x04,0x0C,0x04,0x04,0x04,0x04,0x0E],
    '2': [0x0E,0x11,0x01,0x02,0x04,0x08,0x1F],
    '3': [0x1F,0x02,0x04,0x02,0x01,0x11,0x0E],
    '4': [0x02,0x06,0x0A,0x12,0x1F,0x02,0x02],
    '5': [0x1F,0x10,0x1E,0x01,0x01,0x11,0x0E],
    '6': [0x06,0x08,0x10,0x1E,0x11,0x11,0x0E],
    '7': [0x1F,0x01,0x02,0x04,0x08,0x08,0x08],
    '8': [0x0E,0x11,0x11,0x0E,0x11,0x11,0x0E],
    '9': [0x0E,0x11,0x11,0x0F,0x01,0x02,0x0C],
    '.': [0x00,0x00,0x00,0x00,0x00,0x0C,0x0C],
    ',': [0x00,0x00,0x00,0x00,0x0C,0x04,0x08],
    ':': [0x00,0x0C,0x0C,0x00,0x0C,0x0C,0x00],
    ';': [0x00,0x0C,0x0C,0x00,0x0C,0x04,0x08],
    '!': [0x04,0x04,0x04,0x04,0x04,0x00,0x04],
    '?': [0x0E,0x11,0x01,0x02,0x04,0x00,0x04],
    '-': [0x00,0x00,0x00,0x1F,0x00,0x00,0x00],
    '+': [0x00,0x04,0x04,0x1F,0x04,0x04,0x00],
    '=': [0x00,0x00,0x1F,0x00,0x1F,0x00,0x00],
    '/': [0x01,0x01,0x02,0x04,0x08,0x10,0x10],
    '%': [0x18,0x19,0x02,0x04,0x08,0x13,0x03],
    '(': [0x02,0x04,0x08,0x08,0x08,0x04,0x02],
    ')': [0x08,0x04,0x02,0x02,0x02,0x04,0x08],
    "'": [0x04,0x04,0x00,0x00,0x00,0x00,0x00],
    '"': [0x0A,0x0A,0x00,0x00,0x00,0x00,0x00],
    '&': [0x0C,0x12,0x14,0x08,0x15,0x12,0x0D],
    '$': [0x04,0x0F,0x14,0x0E,0x05,0x1E,0x04],
    '#': [0x0A,0x0A,0x1F,0x0A,0x1F,0x0A,0x0A],
    '*': [0x00,0x15,0x0E,0x1F,0x0E,0x15,0x00],
    '@': [0x0E,0x11,0x17,0x15,0x17,0x10,0x0E],
    '_': [0x00,0x00,0x00,0x00,0x00,0x00,0x1F],
    '|': [0x04,0x04,0x04,0x04,0x04,0x04,0x04],
    '<': [0x02,0x04,0x08,0x10,0x08,0x04,0x02],
    '>': [0x08,0x04,0x02,0x01,0x02,0x04,0x08],
    '^': [0x04,0x0A,0x00,0x00,0x00,0x00,0x00],
    '~': [0x00,0x00,0x08,0x15,0x02,0x00,0x00],
    '`': [0x08,0x04,0x00,0x00,0x00,0x00,0x00],
    '[': [0x0E,0x08,0x08,0x08,0x08,0x08,0x0E],
    ']': [0x0E,0x02,0x02,0x02,0x02,0x02,0x0E],
    ' ': [0x00]*7,
}

SCALES = {}
def glyph(ch):
    return FONT.get(ch.upper(), FONT['?'])

def text_w(s, scale=1):
    return len(s) * (5 + 1) * scale - scale  # 1px tracking between chars

def draw_text_px(px, x, y, s, color=INK, scale=1):
    cx = x
    for ch in s:
        rows = glyph(ch)
        for ry, bi in enumerate(rows):
            for rx in range(5):
                if bi & (0x10 >> rx):
                    for dy in range(scale):
                        yy = y + ry*scale + dy
                        if 0 <= yy < H:
                            for dx in range(scale):
                                xx = cx + rx*scale + dx
                                if 0 <= xx < W:
                                    px[yy][xx] = color
        cx += (5 + 1) * scale
    return cx

def fit_text(px, x, y, s, color, scale, max_w):
    """Draw text scaled down until it fimax_w. Returns scale used."""
    while scale > 1 and text_w(s, scale) > max_w:
        scale -= 1
    draw_text_px(px, x, y, s, color, scale)
    return scale

def fit_text_b(px, x, y, s, color, scale, max_w, alt_color):
    """Fit and draw, but color every 2nd char alt_color for emphasis."""
    while scale > 1 and text_w(s, scale) > max_w:
        scale -= 1
    cx = x
    for i, ch in enumerate(s):
        c = alt_color if (i % 7 == 3) else color
        draw_text_px(px, cx, y, ch, c, scale)
        cx += (5 + 1) * scale
    return scale

# -------------------------------------------------------------------- shapes
def rect(px, x, y, w, h, color):
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    for yy in range(y0, y1):
        row = px[yy]
        for xx in range(x0, x1):
            row[xx] = color

def frame(px, x, y, w, h, color, t=1):
    rect(px, x, y, w, t, color)
    rect(px, x, y + h - t, w, t, color)
    rect(px, x, y, t, h, color)
    rect(px, x + w - t, y, t, h, color)

def line(px, x0, y0, x1, y1, color):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx - dy
    while True:
        if 0 <= x0 < W and 0 <= y0 < H:
            px[y0][x0] = color
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def hline(px, x, y, w, color, t=1):
    rect(px, x, y, w, t, color)

# ------------------------------------------------------------- image helpers
def to_png(px):
    raw = b''.join(b'\x00' + bytes(v for p in row for v in p) for row in px)
    def chunk(tag, data):
        return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b'')

# ------------------------------------------------------------------ headline data
HEADLINES = [
    ("WORLD", "GTA VI LAUNCHES: CONSOLES SELL OUT",
     "Rockstar's GTA VI his shelves Nov 19; PS5 and Xbox bundles vanish from stores worldwide as fans queue overnight."),
    ("MARKETS", "STOCKS MIXED AS GTA VI RALLY FADES",
     "Tokyo and London slip; New York flat. Gaming and retail shares give back early gains in afternoon trade."),
    ("CLIMATE", "COP31 TALKS ENTER FINAL DAY",
     "Delegates in Antalya push for a coal phase-out deadline as host nation tables a compromise text."),
    ("TECH", "AI CHIP FIRM UNVEILS 2NM SILICON",
     "New accelerators promise 3x throughput; cloud giant commit to multi-billion orders through 2028."),
    ("SPORT", "World Cup play-offs: underdogs stun seeds",
     "Two away goals in stoppage time send the visitors to next year's finals."),
    ("CULTURE", "Museums mark International Men's Day",
     "Galleries across Europe open late with free entry for the annual observance."),
]

def headline_blocks():
    return HEADLINES

# ---------------------------------------------------------------- canvas ops
def make_px():
    return [[PAPER for _ in range(W)] for _ in range(H)]

def vignette(px, strength=8):
    for y in range(H):
        fy = (y - H / 2) / (H / 2)
        for x in range(W):
            fx = (x - W / 2) / (W / 2)
            d = max(abs(fx), abs(fy))
            if d > 0.55:
                k = int(strength * (d - 0.55) / 0.45)
                r, g, b = px[y][x]
                px[y][x] = (max(0, r - k), max(0, g - k), max(0, b - k))

def grain(px, amp=4):
    """Deterministic pseudo-film-grain; no random module, fixed LCG seed."""
    seed = 0x20261119
    for y in range(H):
        row = px[y]
        for x in range(W):
            seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
            n = ((seed >> 16) & 0x7) - 3
            if n:
                r, g, b = row[x]
                row[x] = (min(255, max(0, r + n * amp // 3)),
                          min(255, max(0, g + n * amp // 3)),
                          min(255, max(0, b + n * amp // 3)))

# ------------------------------------------------------------ pictogram art
def draw_globe(px, cx, cy, r, color):
    for y in range(-r, r + 1):
        yy = cy + y
        if not 0 <= yy < H:
            continue
        for x in range(-r, r + 1):
            xx = cx + x
            if not 0 <= xx < W:
                continue
            d2 = x * x + y * y
            if d2 <= r * r:
                # latitude arcs
                if abs(y) in (r // 2, (2 * r) // 3) and d2 <= (r - 1) ** 2:
                    px[yy][xx] = color
                # longitude meridians
                elif abs(x) <= 1 or abs(x) == r // 2:
                    px[yy][xx] = color
                # rim (outline circle)
                elif d2 > (r - 2) * (r - 2):
                    px[yy][xx] = color

def draw_chip(px, x0, y0, w, h, color):
    """Silicon die: body + pins + inner core."""
    rect(px, x0, y0, w, h, color)
    frame(px, x0 - 3, y0 - 3, w + 6, h + 6, color, 2)
    n = w // 6
    for i in range(n + 1):
        pxn = x0 + i * 6
        rect(px, pxn, y0 - 7, 3, 4, color)
        rect(px, pxn, y0 + h + 3, 3, 4, color)
    for i in range(h // 6 + 1):
        pyn = y0 + i * 6
        rect(px, x0 - 7, pyn, 4, 3, color)
        rect(px, x0 + w + 3, pyn, 4, 3, color)
    rect(px, x0 + 5, y0 + 5, w - 10, h - 10, PAPER)
    rect(px, x0 + 9, y0 + 9, w - 18, h - 18, color)

def draw_ball(px, cx, cy, r, color):
    """Football: disc + pentagon + spokes."""
    for y in range(-r, r + 1):
        for x in range(-r, r + 1):
            if x * x + y * y <= r * r:
                px[cy + y][cx + x] = WHITE
    pxr = r // 2
    p= []
    for i in range(5):
        import math
        a = -math.pi / 2 + i * 2 * math.pi / 5
        pts.append((int(cx + pxr * math.cos(a)), int(cy + pxr * math.sin(a))))
    for i in range(5):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % 5]
        line(px, x0, y0, x1, y1, color)
        x2, y2 = pts[(i + 2) % 5]
        line(px, x0, y0, x2, y2, color)
    for x, y in pts:
        line(px, x, y, cx + (x - cx) * 2, cy + (y - cy) * 2, color)

def draw_frame_art(px, x0, y0, w, h, color):
    """Museum frame: double border + inner wash."""
    frame(px, x0, y0, w, h, color, 3)
    frame(px, x0 + 4, y0 + 4, w - 8, h - 8, color, 2)
    rect(px, x0 + 8, y0 + 8, w - 16, h - 16, WHITE)
    # abstract 'artwork': two arcs
    cx, cy = x0 + w // 2, y0 + h // 2
    r = min(w, h) // 4
    for a in range(0, 360, 4):
        import math
        rad = math.radians(a)
        px[cy + int(r * math.sin(rad))][cx + int(r * math.cos(rad))] = GOLD
        px[cy + int(r * 0.6 * math.sin(rad))][cx + int(r * 0.6 * math.cos(rad))] = RED

# --------------------------------------------------------------- composition
def rule_double(px, y, x0=36, x1=W - 36, color=INK):
    hline(px, x0, y, x1 - x0, color, 2)
    hline(px, x0, y + 4, x1 - x0, color, 1)

def masthead(px):
    rect(px, 0, 0, W, 8, INK)
    rect(px, 0, 8, W, 2, RED)
    # nameplate
    fit_text(px, 36, 24, "THE DAILY LEDGER", INK, 9, W - 72)
    fit_text(px, 470, 30, "EST. 1898", GOLD, 2, 160)
    # dateline row
    rule_double(px, 96)
    text = "THURSDAY, NOVEMBER 19, 2026  *  WORLD EDITION  *  PRICE 1.50"
    tw = text_w(text, 2)
    draw_text_px(px, (W - tw) // 2, 106, text, INK, 2)
    rule_double(px, 130)

def lead_story(px, y0):
    tag = "EXCLUSIVE"
    rect(px, 36, y0, 108, 18, RED)
    draw_text_px(px, 36 + (108 - text_w(tag, 2)) // 2, y0 + 4, tag, WHITE, 2)
    draw_text_px(px, 156, y0 + 4, "GTA VI HITS SHELVES TODAY", RED, 2)
    fit_text(px, 36, y0 + 26, "CONSOLE FRENZY: STORES SELL OUT WORLDWIDE", INK, 6, W - 72)
    deck = ("Rockstar's record launch empties shelves in Tokyo, London and New York"
            " as fans queue overnight for PS5 and Xbox bundles.")
    fit_text(px, 36, y0 + 76, deck, GREY, 3, W - 72)
    # pictorial: globe over a 'console' slab
    ay = y0 + 118
    frame(px, 36, ay, W - 72, 200, INK, 2)
    draw_globe(px, 200, ay + 100, 70, BLUE)
    draw_text_px(px, 320, ay + 30, "GLOBAL LAUNCH MAP", INK, 3)
    draw_text_px(px, 320, ay + 72, "SOLD OUT", RED, 4)
    # simple bar chart of queues by city
    cities = [("TOKYO", 88), ("LONDON", 74), ("NYC", 91), ("PARIS", 62)]
    bx = 330
    for i, (city, v) in enumerate(cities):
        by = ay + 120 + i * 18
        draw_text_px(px, bx, by, city, INK, 2)
        rect(px, bx + 70, by, int(v * 2.2), 12, BLUE if i % 2 else RED)
        draw_text_px(px, bx + 70 + int(v * 2.2) + 6, by, str(v), GREY, 2)
    rule_double(px, ay + 200 + 8)

def column_block(px, x, y, w, h, tag, head, body, art=None, accent=INK):
    hline(px, x, y, w, accent, 2)
    draw_text_px(px, x, y + 7, tag, accent, 2)
    ty = y + 28
    ty += fit_text(px, x, ty, head, INK, 4, w) * 8 - 8 + 8
    # head line height = 7*scale; compute rows
    rows = max(1, (text_w(head, 4) + w - 1) // w)
    ty = y + 28 + rows * 7 * 4 + 10
    by = ty
    # body: draw first N chars that fit roughly 4 lines at scale 2
    cap = max(0, (w // 12) * 4 * 6)
    fit_text(px, x, by, body[:cap], GREY, 2, w)
    if art:
        ay = by + 7 * 2 * 4 + 10
        if art is draw_chip:
            art(px, x + w // 2 - 30, ay, 60, 46, accent)
        else:
            art(px, x + w // 2, ay + 30, 24, accent)
    # end stop
    ex = x + w - 6
    ey = y + h - 12
    rect(px, ex, ey, 6, 6, accent)

def secondary_grid(px, y0):
    H3 = [("MARKETS", "STOCKS MIXED AS RALLY FADES",
           "Tokyo and London slip; New York flat. Gaming shares give back early gains."),
          ("CLIMATE", "COP31 TALKS ENTER FINAL DAY",
           "Delegates in Antalya push for a coal phase-out deadline as a compromise text lands."),
          ("TECH", "AI CHIP FIRM UNVEILS 2NM SILICON",
           "New accelerators promise 3x throughput; cloud giancommit through 2028.")]
    xs = [36, 356, 676]
    for i, (tag, head, body) in enumerate(H3):
        x = xs[i]
        column_block(px, x, y0, 312, 150, tag, head, body,
                     art=draw_chip if i == 2 else None,
                     accent=(RED if i == 0 else (BLUE if i == 1 else GOLD)))
    rule_double(px, y0 + 160)

def bottom_row(px, y0):
    # sport box
    hline(px, 36, y0, 460, INK, 2)
    draw_text_px(px, 36, y0 + 7, "SPORT", RED, 2)
    fit_text(px, 36, y0 + 28, "WORLD CUP: UNDERDOGS STUN SEEDS", INK, 4, 460)
    fit_text(px, 36, y0 + 66, "Two stoppage-time goals send visitors to the finals.", GREY, 2, 460)
    draw_ball(px, 430, y0 + 66, 30, INK)
    # culture box
    hline(px, 528, y0, 460, INK, 2)
    draw_text_px(px, 528, y0 + 7, "CULTURE", BLUE, 2)
    fit_text(px, 528, y0 + 28, "MUSEUMS MARK MEN'S DAY", INK, 4, 460)
    fit_text(px, 528, y0 + 66, "Galleries open late with free entry across Europe.", GREY, 2, 440)
    draw_frame_art(px, 880, y0 + 18, 108, 100, GOLD)

def footer(px):
    y = H - 34
    rect(px, 0, y, W, 2, INK)
    t = "THE DAILY LEDGER  *  PAGE ONE  *  19 NOV 2026"
    tw = text_w(t, 2)
    draw_text_px(px, (W - tw) // 2, y + 10, t, GREY, 2)
    rect(px, 0, H - 6, W, 6, INK)

def render():
    px = make_px()
    masthead(px)
    lead_story(px, 142)
    secondary_grid(px, 382)
    bottom_row(px, 556)
    footer(px)
    vignette(px)
    grain(px)
    return to_png(px)

def main():
    out = os.path.join(_outdir(), "newspaper.png")
    data = render()
    with open(out, "wb") as f:
        f.write(data)
    print(f"wrote {out} ({len(data)} bytes)")

if __name__ == "__main__":
    main()
