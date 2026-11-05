# Beauty pass research — Marchon-style look for Pump+Cardio
*5 Nov 2026. Research only; app not changed.*

## Marchon look (from App Store + online.marchon.co.uk marketing)

Two faces of the brand:
1. **Marketing / brand:** dark desaturated gym photography, bold white all-caps sans, high contrast, industrial grit.
2. **In-app workout UI (App Store frames):** mostly **light** — white/off-white cards on light grey, black type, soft rounded cards, mint-green completed sets, thin line icons, coach video play pills, block letters (W/A/B/C). Dark-mode-ready redesign noted in 3.0.5 notes; dark marketing bento shows black canvas + mint accents on rep numbers.

Shared traits: large bold neo-grotesque type, generous space, one accent colour, card-per-block, week strip as simple day markers, timers and logging big enough to glance.

Comparable apps: Hevy dark canvas `#0E1116` + blue `#1E6FFF` + green done; Strong utility log; Ladder/Future coach-video heavy (more than we need).

## Current Pump+Cardio (pc-v32)

Dark charcoal (`--bg #0d0f12`, `--card #171a1f`), warm orange accent `#FF8A3D`, system-ui 18px, dense cards, week day pills, full-width orange CTAs. Already gym-friendly and readable; feels utility-first rather than premium-minimal.

## Difficulty for a beauty pass (keep workouts/timers/list+clock)

**Medium.** Almost all of the win is CSS + light markup polish in `src/top.html` (palette, type scale, spacing, card chrome, thinner icons, week strip styling). No need to rewrite timers or session data. Hard only if we add photo backgrounds, light mode, Focus Mode animations, or video.

## Three look directions

### 1. Marchon Dark Mint
- Palette: `#000000` / `#141414` cards / text `#F5F5F5` / accent mint `#4ADE80` / muted `#8A8A8A`
- Fonts: Inter or SF, bold titles, tabular numbers
- Feel: week as green check circles; session cards with mint rep numbers and a huge white timer

### 2. Studio Light (true Marchon App Store workout)
- Palette: `#F2F2F2` bg / `#FFFFFF` cards / black text / mint done `#B8F0C8` / black CTA
- Fonts: heavy black sans, lots of white space
- Feel: airy week strip and logging tables; premium at home, weaker under gym glare

### 3. Ember Polish (upgrade what you have)
- Palette: keep dark `#0d0f12` / soften cards `#15181d` / keep orange `#FF8A3D` but use it sparingly / cooler muted `#9AA3AD`
- Fonts: same system-ui, bigger title hierarchy, more padding, thinner icons
- Feel: same orange DNA, less clutter, timers and day strip clearer from arm's length

## Reference images
`/workspace/health/beauty-pass-refs/`
