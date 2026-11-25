#!/usr/bin/env python3
"""
Render "The World in One Day — 25 November 2026" as a dense 34-story
broadsheet front page, code-drawn with Pillow.

Outputs:
  news-image-20261125.jpg            full 2048x2048 render
  news-image-20261125-1024.jpg       downscaled 1024x1024 (quality 88, <=1 MiB)
"""

import os
import math

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops

W = H = 2048
BG = (244, 239, 228)          # warm newsprint cream
INK = (26, 24, 21)            # ink black
RULE = (118, 110, 96)         # mid rule grey
FAINT = (200, 193, 177)       # hairline grey

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-SemiBoldItalic.ttf"

# ---------------------------------------------------------------- layout grid
ML = 64            # left margin
MR = 64            # right margin
GUTTER = 30
CW = (W - ML - MR - 2 * GUTTER) // 3          # column width = 620
COL_X = [ML, ML + CW + GUTTER, ML + 2 * (CW + GUTTER)]
RIGHT = COL_X[2] + CW                          # 1984
CTOP = 348
CBOT = 1912
FOOT_RULE = 1926

# ---------------------------------------------------------------- stories data
# (headline, summary, photo or None, big front-page lead flag)
SECTIONS = [
    ("WORLD", [
        ("WORLD COURT RULES MYANMAR COMMITTED GENOCIDE",
         "The ICJ holds Myanmar responsible over the Rohingya, the first time a "
         "sovereign state is found guilty of genocide.",
         "photos/peace-palace.jpg", True),
        ("ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF IN GAZA",
         "Seven dead in Gaza City as the ceasefire in place since October 2025 strains.",
         None, False),
        ("HOUTHI DRONE HITS RIYADH TOWER, 11 HURT",
         "A drone struck a financial-district tower; the Saudi-led coalition hit "
         "Hodeidah in reply.",
         None, False),
        ("NATO VOWS SPACE DEFENCE AFTER RUSSIAN SATELLITE REPORTS",
         "NATO pledges to defend allied satellites after reports of Russian nuclear "
         "activity in orbit.",
         None, False),
        ("CHINA PROBES SHANGHAI PARTY CHIEF CHEN JINING",
         "Anti-corruption investigators open a case against the Shanghai party chief.",
         "photos/shanghai.jpg", False),
        ("PAKISTAN'S FIRST ASTRONAUT DOCKS AT TIANGONG",
         "Muhammad Zeeshan Ali boards China's space station aboard Shenzhou-24, "
         "the first foreigner to do so.",
         "photos/tiangong.jpg", False),
    ]),
    ("WAR & DIPLOMACY", [
        ("UKRAINE HITS TWO RUSSIAN REFINERIES",
         "Drones set Syzran and Kuibyshev ablaze in Samara; Putin vows retaliation.",
         None, False),
        ("UK DEFENCE CHIEF VISITS KHARKIV",
         "The UK defence secretary meets troops 20 km from the front; more "
         "RapidRanger launchers pledged.",
         None, False),
        ("US SHELVES RUSSIA BUSINESS-DEAL PLAN",
         "Washington drops proposals to lure Moscow with energy and aviation deals, "
         "the FT reports.",
         None, False),
        ("SOLOMON ISLANDS SIGNS PACT WITH AUSTRALIA",
         "The China security partner signs a new deal with Canberra, including "
         "police support.",
         None, False),
        ("NORTH KOREA EXPELS SWISS DIPLOMAT",
         "Envoy ordered out within 48 hours, weeks after the office reopened.",
         None, False),
        ("HAFTAR VISITS TURKIYE",
         "Libya's Haftar in Ankara days after Ukraine hit a Russian warship in Benghazi.",
         None, False),
    ]),
    ("AMERICA", [
        ("US TO UNVEIL TARIFFS ON 16 PARTNERS",
         "New duties loom after a probe into excess industrial capacity; rates of "
         "15-25% possible.",
         None, False),
        ("NASDAQ FUTURES SLIDE OVER 2%",
         "Tariff fears hit chip stocks; Nvidia falls 4.9% as inflation data looms.",
         None, False),
        ("ABREGO GARCIA LEAVES US FOR SPAIN",
         "The Salvadoran man once wrongly deported departs voluntarily under a deal.",
         None, False),
        ("CIA AND ODNI HIT BY HACK",
         "Unclassified systems breached; officials say no disruption.",
         None, False),
        ("SIX DEAD IN PLANE CRASH OFF MISSISSIPPI",
         "Six people, including two children, die after a crash off the coast.",
         None, False),
    ]),
    ("ASIA", [
        ("NEPAL QUAKE 5.3 RATTLES REGION",
         "Tremors felt across Sikkim and North Bengal.",
         None, False),
        ("BANGLADESH GARMENT WAGE UP 36%",
         "Minimum monthly pay set at Tk 17,000 after protests.",
         None, False),
        ("INDIA NAVY TO BUY 76 HELICOPTERS",
         "Navy and Coast Guard order indigenous utility helicopters for 15,000 "
         "crore rupees.",
         None, False),
    ]),
    ("BUSINESS & TECH", [
        ("SPACEX AND TESLA ADVANCE $3.5T MERGER",
         "The Musk-led firms form a five-member group to advance a merger, the FT reports.",
         None, False),
        ("TRUMP PRESSED NVIDIA BOARD OVER HUANG",
         "The president pushed to reinstate Jensen Huang; the US blacklists "
         "Singapore chip firm Megaspeed.",
         None, False),
        ("TIDAL TO BAN FULLY AI-GENERATED MUSIC",
         "From December 9, all-AI songs will be rejected and existing ones removed.",
         None, False),
    ]),
    ("SCIENCE", [
        ("URANUS AT OPPOSITION TONIGHT",
         "The ice giant is at its closest and brightest for the year.",
         None, False),
        ("FARTHEST 'LITTLE RED DOT' FOUND",
         "Researchers uncover the most distant of the mysterious early galaxies.",
         None, False),
        ("AI PIONEER WARNS OF EXTINCTION RISK",
         "Stuart Russell says humans risk ceding control of civilisation to AI.",
         None, False),
        ("UN WARNS HIV INFECTIONS COULD RISE",
         "Infections may climb from historic lows starting next year.",
         None, False),
    ]),
    ("MORE WORLD", [
        ("IRAN FLOGS SINGER PARASTOO AHMADI",
         "The singer receives 74 lashes after a YouTube concert.",
         None, False),
        ("TANKER ATTACKS PUSH OIL UP 2%",
         "Ships hit near the Strait of Hormuz as prices climb.",
         None, False),
    ]),
    ("SPORT", [
        ("SURYAVANSHI SMASHES RECORD 204*",
         "The 15-year-old hits the fastest List A double hundred, off 53 balls.",
         None, False),
        ("PRIYANSH ARYA HITS 181 IN T20",
         "The highest T20 score by an Indian batter.",
         None, False),
        ("ENGLAND BEAT AUSTRALIA IN 2ND T20I",
         "England chase 185 to level the five-match series.",
         None, False),
        ("BELLINGHAM STARS AS REAL MADRID ROUT PSV",
         "Bellingham scores a screamer in a crushing win.",
         None, False),
        ("GUKESH HOLDS SINDAROV",
         "The world champion weathers time pressure in the title match.",
         None, False),
    ]),
]

CAPTIONS = {
    "photos/peace-palace.jpg": "The Peace Palace in The Hague",
    "photos/shanghai.jpg": "The Lujiazui skyline in Shanghai",
    "photos/tiangong.jpg": "The Tiangong space station in orbit",
}

# ---------------------------------------------------------------- font helpers
_FONTS = {}


def reg(size):
    key = ("r", size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(SERIF, size)
    return _FONTS[key]


def bold(size):
    key = ("b", size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(SERIF_B, size)
    return _FONTS[key]


def ital(size):
    key = ("i", size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(ITALIC, size)
    return _FONTS[key]


def lh(font, pad=0):
    a, d = font.getmetrics()
    return a + d + pad


# ---------------------------------------------------------------- measurement
_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if _MEASURE.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def photo_block(photo, s):
    """Return (pil_image, w, h) fitted to the column; None if no photo."""
    if photo is None:
        return None
    pw = CW - 26
    im = Image.open(photo).convert("L")
    im = ImageOps.autocontrast(im, cutoff=1).convert("RGB")
    ar = im.width / im.height
    h = int(pw / ar)
    if h > 560:
        h = 560
        pw = int(h * ar)
    return im.resize((pw, h), Image.LANCZOS), pw, h


def story_block_h(story, s):
    headline, summary, photo, big = story
    hf = bold(int(round(45 * s if big else 26 * s)))
    sf = reg(int(round(24 * s if big else 19 * s)))
    hlines = wrap(headline, hf, CW - 4)
    slines = wrap(summary, sf, CW - 4)
    h = len(hlines) * lh(hf) + 10 + len(slines) * lh(sf)
    if photo:
        _, pw, ph = photo_block(photo, s)
        cap = ital(int(round(16 * s)))
        h += ph + 6 + lh(cap) + 8
    return h


def label_h(s):
    return lh(bold(int(round(34 * s)))) + 14


def place_all(s):
    col_y = [CTOP] * 3
    ci = 0
    placements = []

    def put(col, y, kind, payload, h):
        placements.append({"col": col, "y": y, "kind": kind,
                           "payload": payload, "h": h})
        col_y[col] = y + h

    for sec_name, stories in SECTIONS:
        lh_ = label_h(s)
        # a section label must never be orphaned at a column bottom: it stays
        # together with its first story, so require label + first story to fit
        # in the remaining space of the current column before placing it here.
        need = lh_ + (story_block_h(stories[0], s) if stories else 0)
        while ci < 2 and col_y[ci] + need > CBOT:
            ci += 1
        put(ci, col_y[ci], "label", sec_name, lh_)
        for st in stories:
            bh = story_block_h(st, s)
            if col_y[ci] + bh > CBOT:
                ci += 1
                if ci > 2:
                    return None
            put(ci, col_y[ci], "story", st, bh)
    return placements


def choose_scale():
    s = 1.0
    best = None
    while s >= 0.55:
        p = place_all(s)
        if p is not None:
            best = (s, p)
            break
        s -= 0.01
    if best is None:
        raise RuntimeError("layout does not fit even at minimal scale")
    return best

# ---------------------------------------------------------------- drawing
def draw_tracked(d, x, y, text, font, fill, tracking):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + tracking
    return y + lh(font)


def draw_para(d, x, y, lines, font, fill, width, justify=True):
    for i, line in enumerate(lines):
        last = i == len(lines) - 1
        words = line.split()
        if justify and not last and len(words) > 1:
            ws = [d.textlength(w, font=font) for w in words]
            sp = d.textlength(" ", font=font)
            extra = width - (sum(ws) + sp * (len(words) - 1))
            if extra > 0:
                per = extra / (len(words) - 1)
                xpos = x
                for j, w in enumerate(words):
                    d.text((xpos, y), w, font=font, fill=fill)
                    xpos += ws[j] + sp + (per if j < len(words) - 1 else 0)
                y += lh(font)
                continue
        d.text((x, y), line, font=font, fill=fill)
        y += lh(font)
    return y


def centered(d, cx, y, text, font, fill, tracking=0):
    tw = sum(d.textlength(ch, font=font) for ch in text) + tracking * (len(text) - 1)
    draw_tracked(d, cx - tw / 2, y, text, font, fill, tracking)


def draw_story(img, d, placement, s):
    x = COL_X[placement["col"]]
    y = placement["y"]
    headline, summary, photo, big = placement["payload"]
    hf = bold(int(round(45 * s if big else 26 * s)))
    sf = reg(int(round(24 * s if big else 19 * s)))
    hlines = wrap(headline, hf, CW - 4)
    slines = wrap(summary, sf, CW - 4)

    y = draw_para(d, x, y, hlines, hf, INK, CW - 4, justify=False)
    y += 8

    if photo:
        im, pw, ph = photo_block(photo, s)
        px = x + (CW - pw) // 2
        d.rectangle([px - 2, y - 2, px + pw + 1, y + ph + 1], outline=INK, width=2)
        img.paste(im, (px, y))
        y += ph + 6
        cap = ital(int(round(16 * s)))
        clines = wrap(CAPTIONS[photo], cap, CW - 6)
        for cl in clines:
            tw = d.textlength(cl, font=cap)
            d.text((x + (CW - tw) / 2, y), cl, font=cap, fill=INK)
            y += lh(cap)
        y += 8

    y = draw_para(d, x, y, slines, sf, INK, CW - 4, justify=True)
    return y


def draw_label(d, placement, s):
    x = COL_X[placement["col"]]
    y = placement["y"]
    name = placement["payload"]
    f = bold(int(round(34 * s)))
    centered(d, x + CW / 2, y, name, f, INK, tracking=2)
    ry = y + lh(f) + 6
    wd = 200
    d.rectangle([x + CW / 2 - wd / 2, ry, x + CW / 2 + wd / 2, ry + 2],
                fill=INK)


def build_canvas():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead --------------------------------------------------------
    title = "THE WORLD IN ONE DAY"
    size = 150
    while size > 60:
        f = bold(size)
        tw = sum(d.textlength(ch, font=f) for ch in title) + 16 * (len(title) - 1)
        if tw <= W - 2 * ML + 40:
            break
        size -= 2
    centered(d, W / 2, 84, title, bold(size), INK, tracking=16)

    sub = "Vol. 1 — No. 239    •    WEDNESDAY, 25 NOVEMBER 2026    •    $2.00"
    sf = reg(30)
    while d.textlength(sub, font=sf) > W - 2 * ML:
        sf = reg(sf.size - 1)
    centered(d, W / 2, 274, sub, sf, INK, tracking=1)

    # heavy + thin rule pair
    d.rectangle([ML, 330, RIGHT, 334], fill=INK)
    d.rectangle([ML, 340, RIGHT, 342], fill=RULE)

    # ---- body ------------------------------------------------------------
    s, placements = choose_scale()

    # assert: every section label is immediately followed by its first story in
    # the same column (no orphaned label at a column bottom)
    for i, p in enumerate(placements):
        if p["kind"] == "label":
            nxt = placements[i + 1]
            assert nxt["kind"] == "story" and nxt["col"] == p["col"], \
                "orphaned section label at column bottom"

    # vertical hairline dividers between columns
    for gx in (ML + CW + GUTTER // 2, ML + 2 * CW + 3 * GUTTER // 2):
        d.rectangle([gx, CTOP, gx + 1, CBOT], fill=FAINT)

    for p in placements:
        if p["kind"] == "label":
            draw_label(d, p, s)
        else:
            draw_story(img, d, p, s)

    # ---- footer ----------------------------------------------------------
    d.rectangle([ML, FOOT_RULE, RIGHT, FOOT_RULE + 2], fill=INK)
    ff = reg(21)
    flh = lh(ff, 2)
    weather = "WEATHER — London 11°C cloud · Paris 9°C rain · New York 14°C fair · Shanghai 8°C fog"
    index = "INDEX — Dow Jones 41,232 (+0.4%) · S&P 500 5,611 (+0.1%) · Nasdaq 17,890 (−0.9%) · FTSE 100 8,210 (+0.2%)"
    d.text((ML, FOOT_RULE + 12), weather, font=ff, fill=INK)
    d.text((ML, FOOT_RULE + 12 + flh), index, font=ff, fill=INK)
    d.text((ML, FOOT_RULE + 12 + 2 * flh),
           "make.fun · The World in One Day · page 1", font=ff, fill=RULE)

    # ---- paper grain + vignette ------------------------------------------
    noise = Image.effect_noise((W, H), 22).convert("L").convert("RGB")
    img = Image.blend(img, noise, alpha=0.055)
    grad = Image.radial_gradient("L").resize((W, H), Image.BICUBIC)
    mask = ImageChops.invert(grad).point(lambda v: int(v * 0.32))
    dark = Image.new("RGB", (W, H), (42, 33, 24))
    img = Image.composite(dark, img, mask)

    img.save("news-image-20261125-2048.jpg", quality=92)
    small = img.resize((1024, 1024), Image.LANCZOS)
    q = 88
    small.save("news-image-20261125.jpg", quality=q, optimize=True)
    while os.path.getsize("news-image-20261125.jpg") > 1024 * 1024 and q > 60:
        q -= 4
        small.save("news-image-20261125.jpg", quality=q, optimize=True)

    print("scale:", round(s, 2))
    print("2048 master bytes:", os.path.getsize("news-image-20261125-2048.jpg"))
    print("1024 final bytes:", os.path.getsize("news-image-20261125.jpg"), "quality", q)
    return img, placements


if __name__ == "__main__":
    build_canvas()
