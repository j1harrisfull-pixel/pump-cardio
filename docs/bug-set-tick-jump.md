# Bug: the screen jumps when James ticks a set (23 Nov 2026) – brief for Claude Code

Status: reproduced on live pc-v72 by Health & Fitness on Mon 23 Nov 2026. App code only. Don't change any training content.

## What James saw
During Mon 23 Nov "Upper · Density Dash" in the Home Screen app: "Any time I press the circle", the layout moves up and
his next tap lands on something else.

## Repro
Playwright **WebKit**, 390x844, touch, tabs layout (no `wo_flat`), live URL, clock Mon 23 Nov 2026 19:00, his real `wo_log`
seeded. Today → Start session. Tap each set circle (`[data-tk]`) in order with `touchscreen.tap`. Scroll only when the next circle is
off screen. Before and after each tap, record `scrollY`, the tapped circle's `getBoundingClientRect().top`, and what
`elementFromPoint` now finds under the finger.

Results (20 taps: superset A 4 rounds, superset B 3 rounds, superset C 3 rounds):

| Tap | What happened | Shift | Under the finger afterwards |
|---|---|---|---|
| first set of block B (2_0), first set of block C (4_0) | the finished block above folds to "✓ Done · … · show" | the content jumps **up 835 px** (B) and **665 px** (C) | `.rs` / `.sp` text, not the next circle |
| last set of a block (1_3) | an "Up next" label is inserted above (`renderSess`, `.upnext` before the first open block, here the warm-up at the top) | content moves **down 50 px** | the previous row's circle (0_3) |
| last move of a round while the next row is under the rest bar (1_1, 1_2) | `startRest` → `setTimeout(keepNext,80)` → `window.scrollBy` | page scrolls **up 22–130 px** about 80 ms after the tap | `.srow.on` or the rest bar itself |
| other taps | – | 0 px | the tapped circle |

So most taps are stable, but the taps that matter most (end of a round, end of a block, first set of the next block)
move the page under his thumb, and a quick second tap hits the wrong thing.

## Root causes (src/app.js)
1. **Fold on block change.** `renderSess` folds a finished block (`fold=bdn&&!UNF[...]&&!(b.k=="ex"&&LASTB==…)`). The block stays open
   only while it is `LASTB`. The first tick in the next block changes `LASTB` (tick handler, `LASTB=lb?…`) and the whole block above
   collapses to one 66 px button with nothing to make up for the lost height.
2. **"Up next" inserted above.** After `$("sess").innerHTML=h`, a new `div.upnext` is inserted before the first open block once
   `nDone>0`. If that block is above the one being worked (e.g. an untouched warm-up), everything moves down.
3. **Auto-scroll for the rest bar.** `keepNext()` scrolls the page so the next set row clears the rest bar, 80 ms after the tap.
4. Every tick re-renders the whole session (`renderSess` → `innerHTML`). iOS Safari has no `overflow-anchor` scroll anchoring,
   so any height change above the viewport shows up as a jump.

## Suggested fix
- **Anchor the tapped row on every re-render.** In the `[data-tk]`, `[data-rp]`, `.pill` and `[data-st]` handlers, read the
  tapped row's `data-row` top before `renderSess()`. After it, find the same row and `window.scrollBy(0, newTop - oldTop)`.
  Use a small `renderKeep(key)` helper. This alone fixes causes 1 and 2.
- **Fold without moving the thumb.** Either keep the finished block open until the panel is closed or reopened, or fold it
  with the anchor above, so the content above shrinks and the screen stays still.
- **"Up next":** render the label slot every time (empty, fixed height) or put it inline in the block heading, so it never adds
  height above the current block.
- **No auto-scroll from the rest timer.** Remove `keepNext`'s `scrollBy`. Reserve space instead: when `#rbar` shows, set
  `padding-bottom` on `#sess` to its height, so James can scroll the next row clear himself and nothing moves above it.
- Optional guard: ignore a tap on a different control within 300 ms of a layout change.

## Acceptance test (new suite, add to FULL and FAST)
WebKit and Chromium, 390x844, touch, tabs layout, clock Mon 23 Nov 19:00. Today → Start session. Tap all 20 circles in order
(scroll only if the next circle is off screen), and do the same on Thu 26 Nov (Step-Up Staircase):
1. After each tap, and again 600 ms later, the tapped circle's `top` changes by at most 2 px and `scrollY` does not change
   unless the test itself scrolled.
2. `elementFromPoint` at the tap point is still the tapped circle (or its row) after every tap, including the last set of a
   block and the first set of the next block.
3. Finished blocks still end up folded ("✓ Done · … · show") once the panel is reopened. The rest bar still starts after the last
   move of a round, and the next row can be scrolled clear of it (the bottom padding is there).
4. Existing suites stay green (test_v63 "label chip and name on one line" already failed before this work).
