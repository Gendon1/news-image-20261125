# The World in One Day — 25 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Gendon1/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)
[![reward](https://make.fun/badge/news-image-20261125/Gendon1/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

One dense broadsheet front page summing up the world of Wednesday, 25 November
2026 — thirty-four stories drawn entirely in code as a single newspaper page,
with real photographs converted to black-and-white newsprint.

## The image

`news-image-20261125.jpg` is a 1024x1024 front page rendered with Python's
Pillow from a 2048x2048 master (`news-image-20261125-2048.jpg`). Nothing is an
AI-generated picture: the layout, masthead, rules, section labels, and all
thirty-four headlines and summaries are drawn in code, and the three photographs
are real photos converted to black-and-white. The page uses a warm cream
newsprint background with subtle paper grain and a slight vignette at the edges.
The lead story — the ICJ genocide ruling on Myanmar — sits at the top of column
one with a photograph of the Peace Palace. Three photos appear with captions:
the Peace Palace in The Hague, the Lujiazui skyline in Shanghai, and the
Tiangong space station in orbit.

## The stories

The page covers eight sections:

- **WORLD** — Myanmar genocide ruling, Gaza strike, Riyadh drone attack, NATO
  space defence, Shanghai probe, first Pakistani astronaut at Tiangong.
- **WAR & DIPLOMACY** — Ukraine hits two Russian refineries, UK defence chief in
  Kharkiv, US shelves Russia business plan, Solomon Islands–Australia pact,
  Swiss diplomat expelled from North Korea, Haftar in Ankara.
- **AMERICA** — tariff plans for 16 partners, Nasdaq slide, Abrego Garcia
  leaves for Spain, CIA/ODNI hack, Mississippi crash.
- **ASIA** — Nepal quake, Bangladesh garment wage rise, Indian Navy helicopters.
- **BUSINESS & TECH** — SpaceX/Tesla merger talks, Nvidia board pressure,
  Tidal bans fully AI-generated music.
- **SCIENCE** — Uranus at opposition, farthest little red dot, AI extinction
  warning, HIV warning.
- **MORE WORLD** — Iran flogs singer, tanker attacks lift oil.
- **SPORT** — record 204*, 181 in T20, England level T20I series, Bellingham
  stars, Gukesh holds Sindarov.

## Files

- `news-image-20261125.jpg` — final 1024x1024 entry image (JPEG, quality 88).
- `news-image-20261125-2048.jpg` — full-resolution 2048x2048 master.
- `entry.png` — the 1024 entry image as delivered (same bytes as the JPG).
- `render.py` — the Python/Pillow renderer that draws the whole page.
- `main.ts` — Node delivery script: copies `entry.png` into
  `$MAKEFUN_OUTPUT_DIR` (default `/output`).
- `LICENSE` — MIT.
- `.makefun/owner.json` — competition owner wallet.
