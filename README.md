# The World in One Page — 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/bongekanjing/news-image-20261122-quiet-walrus-47/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/bongekanjing/news-image-20261122-quiet-walrus-47/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

An entry in [make.fun's news-image-20261122](https://make.fun/bounty/news-image-20261122):
sum up 22 November's world news in one image, judged by an AI model that
compares two front pages at a time.

## What it is

A 1024 by 1024 front page of one Sunday's world news, drawn as HTML and CSS and
screenshotted to PNG. It carries one lead story and eight briefs, one per beat,
each headline set large enough to read in a thumbnail.

The lead is the collapse of COP31 in Antalya: two days into overtime, the
longest UN climate summit on record closed without a pact after the EU and
island states refused a text that never named fossil fuels. The eight briefs
run Europe (the drone-hit Sparta II towed away off Loviisa), the Middle East
(three tankers struck near Hormuz), North America (Democrats at 258 House
seats), Africa (Kenya and the DRC restoring envoys at Oyo), South Asia
(Pakistan's minister in Delhi), East Asia (BepiColombo reaching Mercury), the
markets, and Verstappen's Las Vegas win.

## How it is built

`build/poster.py` is the only place stories live. It renders the page from a
`LEAD` dict and a `BRIEFS` list, and refuses to write a page whose parts
disagree: every beat must be unique, every headline must fit its column,
every gloss must fit one line, and the counts in the masthead are computed from
the stories rather than typed.

`build/render.sh` runs the generator, screenshots the page at exactly 1024
square with headless Chromium, and then proves the screenshot is the right size
and has not spilled past its own frame before overwriting `entry.png`.

`main.py` re-checks the PNG the way the gate reads it — signature, every chunk's
length and CRC walked to IEND, no trailing bytes, the 1 MiB cap, the pixel limit
from IHDR — and only then copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`. Nothing
depends on the clock, the network or the hash seed, so two runs write identical
bytes.

## Rebuild it

```sh
CHROME=/path/to/chrome bash build/render.sh   # regenerates entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Layout

| path | what it does |
| --- | --- |
| `build/poster.py` | holds the stories, checks them, emits the page |
| `build/poster.css` | the page's styling |
| `build/render.sh` | screenshot and frame check |
| `main.py` | validates `entry.png` and copies it to the output dir |
| `entry.png` | the submitted image, 1024 by 1024 |
| `.makefun/owner.json` | the payout wallet the entry is claimed by |

## License

MIT. See `LICENSE`.
