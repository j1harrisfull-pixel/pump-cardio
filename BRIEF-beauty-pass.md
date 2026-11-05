# Brief: Beauty pass — white + orange (for Claude Code)

*Approved by James on 5 Nov 2026 after reviewing the light mocks. Read `CLAUDE.md` first (architecture, hard rules, localStorage compatibility), then this brief. Visual reference: `docs/beauty-pass-mocks/light-*.png` (HTML sources alongside). Research: `docs/beauty-pass-research.md`.*

**Goal:** Visual beauty pass only. Make the live PWA look like the approved **white + orange** light mocks — clearly better and clearly different from the current dark, dense UI. Do **not** change workouts, timers, list/clock modes, or session data.

Ship as **one release** (next version after live pc-v32), one commit, with tests green.

## Approved look (tokens)

| Token | Value |
|---|---|
| Page background | `#F5F5F7` |
| Cards | `#FFFFFF` with soft shadow **or** `#E8E8ED` hairline border |
| Text | `#111111` |
| Muted / secondary | `#6B6B70` |
| Accent (orange) | `#FF8A3D` — selected day, primary CTAs, ticks on, progress fill |
| Accent soft | `rgba(255,138,61,.14)` for labels / selected wash |
| Hairline | `#E8E8ED` |

Also:
- **More padding / breathing room** than the current dense cards.
- **Softer rounded cards** (≈16–20 px).
- **Thinner / smaller icons** (20–24 px) with **≥44 px tap targets**.
- Keep **gym-readable large type** and **big timers**. List mode + full-screen clock mode from pc-v31 stay as they are functionally.
- Week strip: light/white pills; **solid orange only for today / selected**.
- EMOM / clock: huge near-black countdown on white; orange for active minute progress / primary Pause / Start.

Match spacing and hierarchy in the mocks: one big current move, next move small; quieter secondary chrome.

## Reference mocks

In-repo (copy of the approved previews):

- `docs/beauty-pass-mocks/light-week.png` (+ `.html`) — week strip + today card
- `docs/beauty-pass-mocks/light-session.png` (+ `.html`) — Upper strength list mode
- `docs/beauty-pass-mocks/light-emom.png` (+ `.html`) — 16 kg EMOM clock mid-session

Side-by-side the live app with these PNGs on a phone-width viewport. Close is good enough; pixel-perfect is not required.

## In scope

CSS / chrome in `src/top.html` (and any style tied to it after `bash scripts/build.sh`):

- CSS variables and body / card / button / input chrome
- Week strip day pills
- Progress ring colours
- Typography hierarchy (titles, muted notes, labels)
- Icon size and tap targets
- Rest bar / guided bar chrome colours only (not behaviour)
- Contrast that still reads outdoors / under gym lights as far as a light theme allows

## Out of scope

- Session content, `SESS` / `OVR` / `PROG` / `BK` / week-4 (or any) programme data
- Timer behaviour, segment logic, beeps, wake lock, “finished while locked”
- List mode vs clock mode structure (pc-v31 stays)
- New features, photo backgrounds, dark-mode toggle (light only for now)
- Second user profiles
- Renaming localStorage keys or exercise / block ids
- Migrations unless a style-only change somehow needs one (it should not)

## Safety / compatibility

- **Never break localStorage keys or logged ticks.** Seeded logs must still load.
- **Pull `main` first.** Live is **pc-v32** (week 4 sessions) on top of **pc-v31** (list + clock modes). Both must survive untouched in behaviour and data.
- Do not edit session blocks “while you’re there”.
- Safety copy, stop-signs line, RPE / RIR wording: leave as-is.

## Process

1. `git pull` (or fetch + reset to `origin/main`) so week 4 + pc-v31 modes are present.
2. Change theme chrome in `src/top.html` (primary). Rebuild with `bash scripts/build.sh`.
3. Update Playwright expectations **only** where they assert visual chrome (colours, contrast, class names for theme). Do not weaken behaviour tests.
4. `bash scripts/test.sh` — all suites must pass.
5. `bash scripts/bump.sh NN` for the next version after whatever is live (expect **33** if live is still pc-v32; confirm `sw.js` head first).
6. One commit: `pc-vNN: beauty pass — white + orange (visual only)`.
7. Push to `main`. Confirm live: `curl -s https://j1harrisfull-pixel.github.io/pump-cardio/sw.js | head -c 22` and visual spot-check on phone.

## Success criteria

- [ ] Side-by-side with `docs/beauty-pass-mocks/light-*.png` looks close (light canvas, orange accent, airy cards).
- [ ] Week home, a strength list session, and an EMOM clock all read clearly at 390×844.
- [ ] No session / timer / storage regressions; `bash scripts/test.sh` green.
- [ ] Version bumped; Pages serving the new `pc-vNN`.

## Out of scope reminder

If tempted to “also fix” an EMOM label, a week-4 cue, or a second profile: **stop**. That is a different brief.
