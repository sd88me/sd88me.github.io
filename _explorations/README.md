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
