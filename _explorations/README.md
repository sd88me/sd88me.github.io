# Explorations

Work in progress for review. Folders starting with `_` are not published by GitHub Pages.

- `directions/index.html`: three alternative site themes (Faceplate, Mandala, Signal) and a board of eight logo directions. Open it through a local server from the repo root (`python3 -m http.server`), then visit `/_explorations/directions/`. It expects `img/` and `logos/` next to it: copy `../logos` and `../../img` in, or view the published preview instead.
- `logos/`: every logo direction as outlined SVG (no fonts needed to display them).
- `gen_logos.py`: regenerates the logos from the typefaces. Needs `pip install fonttools uharfbuzz` and the fonts from github.com/google/fonts (Syne, Michroma, Martian Mono, Bodoni Moda, Cormorant Garamond, Major Mono Display, Big Shoulders Display, Unbounded) in `_explorations/fonts/`. All are SIL Open Font License.
