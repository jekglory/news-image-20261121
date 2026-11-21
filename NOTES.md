# news-image-20261121 — notes

This entry is a pure-stdlib Python program (`main.py`) that draws a
1024x1024 front-page image summing up Saturday 21 November 2026.
The page follows the previous days' shape: one wide lead story on
top, four stories in a 2x2 grid, and a single strip along the bottom.

## The six stories (researched 2026-11-21 ~10:00 WIB, from that day's reporting)

1. POLAND - NATO (lead): Two Russian missiles and a suspected drone
   come down in Poland during a massive Russian strike on Ukraine
   (400+ drones, 110+ missiles). A Kh-101 cruise missile crashes at
   Nowy Lipowiec, about 50 km from the border, at about 06:30. No
   casualties, no destruction. PM Tusk calls it an intentional
   provocation timed to allied drills at Nowa Deba; NATO chief Rutte
   calls it a grave violation of Polish airspace and flies to Warsaw.
2. MARKETS - WALL ST: The S and P 500 falls 3.7% on Friday as AI
   shares plunge; the Nasdaq erases all its 2026 gains, the Nikkei
   drops 5.06%, gold falls about 4%.
3. WEATHER - INDIA: Cyclone Akvan crosses the Odisha coast near
   Gopalpur after 300,000 people were evacuated.
4. HEALTH - CANCER: Daraxonrasib plus chemotherapy leaves 77% of
   patients alive at one year; tumours stopped growing in 90.2%,
   and gone in 1 in 12.
5. EUROPE - BRUSSELS: Britain and the EU sign three deals in
   Brussels: food trade, linked carbon markets and a youth mobility
   scheme.
6. GULF - RIYADH (strip): The Saudi coalition intercepts Houthi
   missiles over Riyadh and strikes Hodeidah port; the Houthis say
   41 people were killed in 24 hours.

## Local verification (2026-11-21 ~10:10 WIB)

- `python3 -m py_compile main.py`: OK.
- Two runs into different output dirs: byte-identical entry.png,
  sha256 8e870f33f393bcc016c1dc117317d8218bb2289837c11cbc6c3aa342f60bcc9c.
- PNG valid (signature + IHDR 1024x1024), 41,611 bytes (cap 1,048,576).
- Rendered image inspected visually: masthead date legible, all six
  headlines + subheads legible, scenes read (NATO star + missile
  streaks + Polish flag over the night ground, falling chart with
  -3.7% and NASDAQ -5%, cyclone spiral + ODISHA LANDFALL + waves,
  pill capsule + rising curve + 77%, Union Jack + EU stars +
  BRUSSELS 3 DEALS, Riyadh towers + interceptor streaks + burst).
- Fixes during the build: cyclone coastline and ODISHA/LANDFALL
  text moved apart so the line no longer crosses the gold text
  (verified with a 3x zoom crop of the band); NASDAQ -5% moved left
  so its final % is not clipped by the scene frame.

## Repo

- jekglory/news-image-20261121, PUBLIC, MIT (SPDX line), created
  after the 2026-11-21T00:00:00Z opening.
- Files: main.py, LICENSE, README.md, NOTES.md, .makefun/owner.json.
