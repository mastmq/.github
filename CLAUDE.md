# .github

The `mastmq` organization profile and the brand assets. This repo is the source of truth for both.

## Two jobs

`profile/README.md` renders on <https://github.com/mastmq> as the organization's front page. It leads with the banner in a `<picture>`, links the website, and lists **all** repos. It has gone stale once already by listing three of five.

`assets/` is where the brand lives. Every other repo — the broker README, the docs README, the charts README, the bench README, the website — links to `raw.githubusercontent.com/mastmq/.github/main/assets/...` or copies from it. **A change here propagates to six places.**

## banner.py is the source; the PNGs are output

`assets/banner.py` draws the layout as SVG, rasterises it with `rsvg-convert`, then composites `mascot.png` on top with Pillow. It emits all four files in one run:

```console
$ cd assets && python3 banner.py
```

Edit the script, never the PNGs. There is deliberately no `banner.svg` any more — the old one described only the background and was misleading as a "source".

| Output | Use |
| --- | --- |
| `banner.png` / `banner@2x.png` | dark, 1280×400 and 2560×800 |
| `banner-light.png` / `banner-light@2x.png` | light, paired in a `<picture>` so each GitHub theme gets its own |

After regenerating, copy them into `mastmq.github.io`'s `public/assets/` and rebuild that site, or the website keeps serving the old art.

## The mascot cannot be cut out — do not try again

Its backdrop measures `(251, 251, 251)`; its white t-shirt measures `(245, 243, 248)`. Six levels apart, with no edge between them. Every threshold tight enough to keep the shirt leaves a halo; every threshold loose enough to remove the backdrop eats holes in the shirt and the white fur. A flood fill from the frame edges fails for a second reason: the mascot's own dark body touches the bottom edge, so some seed points land *inside* the subject.

So it is not cut out. **Both** banners draw a rounded panel in exactly the backdrop's own colour, `(251, 251, 251)`, and place the mascot inside it. What would have been a seam becomes a deliberate card, and a soft shadow under the panel does the work the cutout was supposed to do. The light ground is `#EAEAEC → #F1F1F3` so the panel reads as intentional rather than as a mismatch.

This is why the light and dark variants share a panel colour even though nothing else about them matches.

## Decisions made by looking, not by reasoning

The beacon extends its own bar upward so it sits *on* the mast rather than floating above it.

The mascot bleeds off the bottom edge. A figure with air underneath reads as pasted in.

`mascot.margin-bottom: -7%`. Cropping more cuts through the "mast" wordmark on the shirt.

The mark is left of the text, not above it. Stacked, the banner needed more height than 400px, and GitHub renders a taller banner smaller for the trouble.

## There is deliberately no favicon

The lockup was rendered at the sizes it will actually be seen at before being adopted. It survives 40px, which is what GitHub shows in a list. It does not survive 16px: nine bars with two-pixel gaps become an orange-grey blur and the wordmark becomes a smear.

A favicon needs its own drawing — three or five bars rather than nine, wider gaps, no wordmark, probably no diagonal split, since at 16px the split adds noise rather than meaning. Shipping a downscaled lockup would just be shipping a blur. If you add one, draw it; do not resize.

## Colours

Sampled from the artwork rather than specified in advance. Source of truth for anything new, including the website's `:root`.

| | |
| --- | --- |
| Orange | `#F2711C` |
| Charcoal | `#4A4A4A` |
| Ground | `#F3F3F3` — off-white, not pure white |

The ground is sampled, not chosen. Compositing onto `#F4F4F4` instead left the lockup sitting in a faintly visible box one shade off its surroundings, which is the kind of thing nobody sees until they do.

## Org-wide community health files

Files placed at this repo's **root** (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.github/ISSUE_TEMPLATE/`, `PULL_REQUEST_TEMPLATE.md`) become defaults for every `mastmq` repo that lacks its own. That is the cheapest way to lift the community-health score across the org in one commit.

None exist yet. A code of conduct needs an enforcement contact, which is a decision for the owner rather than something to invent.

## Conventions

Conventional commits. The website's `Mark.astro` re-draws the logo as inline SVG with geometry matching `banner.py` (`N=9, UNIT=13, GAP=10, PEAK=112, CX=98.5, CY=88`, viewBox `0 0 197 162`, beacon `r=14.5`) — if the mark's geometry changes here, it changes there too.
