# sd88me.github.io

The sd88me website, served by GitHub Pages at https://sd88me.github.io/.

| Path | What it is |
|---|---|
| `index.html` | The site (Cymatic design): home, `#reverbicon-224` plugin datasheet, `#brand` brand book. Static, no build step. |
| `img/` | Plugin panel screenshots (WebP, 960 px wide), taken from each plugin repo's docs. |
| `brand/` | SD88ME logo (sand-ring 88), the mark at four sizes, favicon, app icon, Stamp, Seal, social share image. |
| `BRAND.md` | Brand notes: logo, mark, colour, type, motifs, voice, name. |
| `_explorations/` | Design rounds 1–7 and the scripts that generate the logo files. Not published. |
| `mpc-vst-plugins/` | Mirror of the Open MPC catalog. Linked from plugin READMEs; leave its path unchanged. |

## Preview locally
```
python3 -m http.server 8000
```
Then open http://localhost:8000/.

## Before going live
- Check the method label (Circuit / Firmware / Port / Original) and platform on each plugin in the `featured` and `index` arrays in `index.html`.
- Wire the Editions sign-up form to a mailing service (Buttondown, Mailchimp or Ko-fi).
- Optional custom domain `sd88.me`: add a `CNAME` file and point DNS at GitHub Pages. GitHub redirects the old `sd88me.github.io/...` links, including `mpc-vst-plugins/`, to the new domain.
- Once there are several datasheets, give each plugin its own page (`/plugins/acid-303/`) so search engines can index them.
