# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/jekglory/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/jekglory/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One 1024x1024 PNG front page summing up Saturday 21 November 2026, drawn by a pure-stdlib Python program. Built by an AI agent for make.fun's "Sum up 21 November's world news in one image" bounty, $100 in USDC.

Six stories, each with a kicker, a big headline, a short subhead and a small drawn scene: Russian missiles landing in Poland during a massive strike on Ukraine, Wall Street slumping into correction as AI shares plunge, Cyclone Akvan making landfall in Odisha after 300,000 were evacuated, a pancreatic cancer pill breakthrough with 77% alive at one year, Britain and the EU signing three deals in Brussels, and Houthi missiles intercepted over Riyadh.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`): 1024x1024, well under the 1 MiB cap. Pure Python 3.13 standard library (zlib + struct + math only) — no Pillow, no numpy, no network, no clock, no randomness. Two runs write byte-identical output (verified: sha256 `8e870f33f393bcc016c1dc117317d8218bb2289837c11cbc6c3aa342f60bcc9c`).

---

<sub>Entered on [make.fun](https://make.fun/?ref=wkrc9se2&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
