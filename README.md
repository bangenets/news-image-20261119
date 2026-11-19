# The World in One Day — Thursday, 19 November 2026

A one-image summary of the world's news of Thursday 19 November 2026,
built for make.fun's `news-image-20261119` competition.

## What's in the image

A newspaper-style front page, drawn entirely in code:

- **Lead — Summit:** Donald Trump, Xi Jinping and Vladimir Putin meet
  in Shenzhen for a first trilateral of the three nuclear powers.
- **Gaming:** Grand Theft Auto VI rolls out worldwide after a
  13-year wait.
- **US politics:** Democrats nominate Hakeem Jeffries for House
  Speaker — set to become the first Black Speaker.
- **Europe:** The EU proposes a €45 billion loan for Ukraine, to be
  repaid from Russian reparations.
- **Tech:** Anthropic, the maker of Claude, is poised for a stock
  debut valued above $1.4 trillion.
- **Also today:** Cyclone Akvan bears down on India's east coast; a
  Van Gogh sells for a record $190.4 million after a Nazi-era row.

Facts verified against wire reporting of the day (Reuters, The New
York Times, Associated Press, BBC, European Union).

Note: the image was drawn in the morning of 19 November 2026 (UTC),
from the day's reporting available at that time; the summit and the
day's later events were still unfolding.

## Files

- `entry.png` — the submitted image (1024×1024, drawn by `draw19.py`).
- `main.ts` — the entry program: copies `entry.png` to the output
  directory (`$MAKEFUN_OUTPUT_DIR`, or `/output`).
- `draw19.py` — the Python + Pillow script that draws the image from
  scratch (flat vector-style icons, no copyrighted photos).

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png
```
