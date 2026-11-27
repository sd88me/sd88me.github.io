# Explorations

Work in progress for review. Folders starting with `_` are not published by GitHub Pages.

- `directions/index.html`: three alternative site themes (Faceplate, Mandala, Signal) and a board of eight logo directions. Open it through a local server from the repo root (`python3 -m http.server`), then visit `/_explorations/directions/`. It expects `img/` and `logos/` next to it: copy `../logos` and `../../img` in, or view the published preview instead.
- `logos/`: every logo direction as outlined SVG (no fonts needed to display them).
- `gen_logos.py`: regenerates the logos from the typefaces. Needs `pip install fonttools uharfbuzz` and the fonts from github.com/google/fonts (Syne, Michroma, Martian Mono, Bodoni Moda, Cormorant Garamond, Major Mono Display, Big Shoulders Display, Unbounded) in `_explorations/fonts/`. All are SIL Open Font License.

## Round 2
- `round2/index.html`: organic symbols (Sand rings, Peaks, Pen, Plate, Cells) with Stamp, horizontal and Seal lockups, and three more themes: Cymatic, Nocturne, Bloom. Needs `sym/` and `img/` next to it, like round 1.
- `gen_symbols.py`: rebuilds the symbols and lockups. Needs `pip install numpy scikit-image fonttools uharfbuzz`, plus `gen_logos.py` and the fonts as above.

## Round 3
- `round3/index.html`: the two finalist symbols (Sand rings, Peaks) with a lowercase wordmark, Stamp, Seal and small sizes, plus three themes in greens, blues and oranges: Specimen, Resonance and Orbit.
- `gen_round3.py`: rebuilds the round 3 lockups (uses `gen_symbols.py`).

## Round 4
- `round4/index.html`: the logo system (Peaks at four optical sizes, SD88ME capitals in four typefaces with weight-matched marks, icons, favicons, Stamp), Specimen with a live palette switcher (Buddha-poster colours, brighter), and Orbit with a live typeface switcher.
- `gen_round4.py`: rebuilds the round 4 logo files. Line weights in the lockups are measured from each typeface's letter stems.

## Round 5
- `round5/index.html`: Specimen with a palette switcher and a graphics-panel switcher (graphite, midnight blue, warm black, paper, full colour), and Orbit in Instrument Sans with four colour schemes (Ember, Ultramarine, Dune, Graphite & lime). Uses the logo files in `../round4/sym/`: copy that folder next to it as `sym/`, plus `img/`.

## Round 6
- `round6/index.html`: Cymatic with the Peaks + SD88ME logo (Mona Sans Wide, one colour), sand that forms the Peaks mark (or four rings), sigils on cards, a drifting sigil band and an optional sigil ring, and six colour themes. The logo is inlined, so it only needs `img/` next to it.
