# The World — 22 November 2026 in One Image

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/wenwijaya/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/wenwijaya/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for [news-image-20261122](https://make.fun/bounty/news-image-20261122)
on make.fun: sum up the world's news of Sunday 22 November 2026 in one image.

The entry is a newspaper front page, **THE WORLD**, drawn programmatically
with Pillow by `render.py` from the day's verified news (BBC, AP, Reuters):

- **Lead — COP31 deadlocked:** delegates from nearly 200 countries in
  Antalya could not agree a new climate deal; the fight over fossil fuels
  stalled the talks.
- **The Gulf war widens:** Iran struck the U.S. air base at Ali Al Salem in
  Kuwait and a U.S. radar site at Sheikh Isa in Bahrain, days after U.S.
  jets hit a missile site on Qeshm Island; tankers burned in the Strait of
  Hormuz and oil flows through the chokepoint halved.
- **Peru shaken:** a magnitude 6.9 earthquake rattled the Andes.
- **Mexico:** cartel boss "El Chapo Isidro" arrested in a special-forces
  raid; 11 killed in the violence that followed in Sinaloa.
- **Ukraine:** 400 drones and 110 missiles in one night; debris crashed in
  Poland; Estonia to close its Russia border.
- **APEC, Shenzhen:** Trump arrived for the summit, with a trilateral
  meeting with Xi Jinping and Vladimir Putin planned.
- **In brief:** Bolsonaro in ICU; the Princess of Wales films a BBC
  documentary on life with cancer; UK–EU agree a youth mobility scheme;
  India v New Zealand, 1st Test; Cummins keeps the Test captaincy.

## Run

`main.py` copies the rendered page to `/output/entry.png`. It needs no
network and writes identical bytes on every run:

```sh
python3 main.py        # writes /output/entry.png (1024x1024, ~140 KB)
python3 render.py      # re-render entry.png from scratch (needs Pillow)
```

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
