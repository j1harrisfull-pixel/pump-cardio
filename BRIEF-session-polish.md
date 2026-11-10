# BRIEF: session screen polish (pc-v61 to pc-v63)

Status: draft written 10 Nov 2026 for James to approve. Implement only after he says go.
Read `CLAUDE.md` first (hard rules, build, test, deploy). This brief only covers the tabs layout (pc-v58 onwards).

## Why
James, on his phone, 10 Nov 2026:
1. "When you're on this week, if you click through on Wednesday, then it should just be the workout. It shouldn't be the week in that deeper screen."
2. "Today's workout screen, it all looks a bit clunky. What can we do to make it all look a bit nicer?"

The session screen works. The problem is how it looks and how much sits above the work. Measured on a 390 × 844 screen on a strength day (Thu 12 Nov 2026, "Lower · Carry Medley"):
- Block 1 starts about 500 px down. Above it sit a floating Back pill, the title, the date, the ring, "Today · ≈ 43 min", "Change session", the "What did you do?" card, the safety note and the stop signs line.
- A strength card has uneven move headers (the A1 label sits above its name, the A2 label sits beside its name, "More" floats at different heights), then a wall of identical rows "1 · A1, 1 · A2, 2 · A1 …" with nothing showing which set is next.
- kg boxes are pale grey on white with almost no edge.
- The bottom repeats the top question as five more chips, then Notes, Finish and Reset as loose pieces.
- Opened from Week, the week arrows, Edit plan and the seven day strip sit above the session.

## Goal
One calm screen per session: a slim bar at the top, the work straight under it, the next set obvious, one tidy finish area. No change to what is saved.

## Rules for this job
- **Tabs layout only.** Scope every style under `body.tabs` (usually `body.tabs.open`). The flat layout (`wo_flat=1`) must look and behave exactly as now, because 33 older suites and the audit run on it.
- **Do not change the text of any `h2` block header**, any id, any `data-` attribute or any localStorage key. The audit reads the headers. Add new elements beside existing ones instead.
- **No change to logs or saved state.** No new required fields. This is layout, style and a little rendering.
- **Safety text:** the stop signs line stays visible on every session, in full, never clamped, never behind a tap. The session safety note (`#safe1`) also stays in full. You may restyle and move them (see Part B), not shorten or hide them.
- No new dependencies, fonts, images from the network or external scripts. Inline SVG only.
- Colours: keep the tokens in `src/top.html`. Text on orange is `#111`. Small orange text uses `--accent-ink`. Every new text and control must reach 4.5:1 in light and in dark, and every tap target must be at least 44 × 44 px.
- One commit per part, `pc-v61`, `pc-v62`, `pc-v63`, each with bump, build, full `bash scripts/test.sh` green, push to `main`, and the Pages deploy confirmed (see CLAUDE.md; `github.io` is not reachable from the cloud session, so confirm through the GitHub Actions run list).
- Tests: write new suites with `tabs_app()` from `tests/lib.py`. Update `tests/test_v58.py`, `test_v59.py` and `test_v60.py` only where this brief changes the behaviour they check.
- After each part, take screenshots at 390 × 844 and 375 × 667, light and dark, of: session top, a strength card mid way with some sets ticked and the rest bar running, a guided timer card, the bottom of the session, a run day, a day opened from Week, the "something else" form. Look at them before committing. Nothing may overlap, clip or sit under the Back button, the dock or the tab bar.

## Part A (pc-v61): a day opened from Week is just the workout
- When a day is open, hide the week row (`.wk`: arrows, label, Edit plan), the strip (`#week`), `#swr` and `#hint` on every tab. Today the rule `body.tabs.open:not(.t-week)` hides them only outside Week; make it apply on Week too.
- Back returns to the Week list at the scroll position it had.
- The Week tab stays highlighted while that day is open, so the user knows where Back leads.
- Swap days is unaffected: Edit plan is on the Week list, and it already shows the strip while editing.
- Update the checks in `test_v58.py` ("tapping a day opens it under the strip…", "another day in one tap") and `test_v60.py` ("an open day has the strip for hopping…") to the new behaviour. Hopping between days is now Back, then tap another row.

## Part B (pc-v62): top of the session
Target: on a strength day at 390 × 844 the first block header is at or above y = 330 (now about 500). At 375 × 667 the first card is at least partly visible without scrolling.

1. **One slim top bar**, fixed, about 52 px plus the safe area, solid background with a hairline under it:
   - left: `‹ Back` (the existing `#close`, keep the id);
   - middle: the session title on one line, 17 px bold, ellipsis if long;
   - right: progress as text, "3 of 19", from `score(sel)`; "✓" once logged.
   The big header (title, date, ring) is hidden while a session is open. The page content starts below the bar; nothing scrolls under the Back button unreadably.
2. **One meta line** under the bar, 14 px muted: "Thu 12 Nov · ≈ 43 min" plus, at the right end, the existing `Change session` button as a small text link. This replaces the separate `#dnote` row and `Change session` row visually. Keep both elements and their ids; lay them out on one row.
3. **The top question gets small.** For today's session, on plan and not logged, render `#topq` as one quiet text row: "Doing something else or skipping?" Tapping it expands the existing three chips in place. In every other case (past day, off plan, skipped, logged) show the chips as now. The chips, their `data-toc` values and their handlers do not change.
4. **Safety block as one quiet card**: a soft tinted card (`--soft` background, 12 px radius, 12 px padding) holding the session note in 14 px muted text and, under it, the stop signs line in `--stop` at 14 px, both in full. It sits directly above block 1. In off plan mode keep the pc-v59 behaviour (the card goes under the form).

## Part C (pc-v63): strength cards, inputs and the finish area
1. **Move headers, one pattern for every move:** label chip (A1) and name on the same line, name wraps if long; "More" becomes a 44 × 44 px icon button (three dots, inline SVG, `aria-label="More"`) pinned top right of that move. The prescription line ("3 × 7 each side" + tempo chip) and the tempo words stay under it, 14 px.
2. **Rows grouped by round.** Instead of "1 · A1, 1 · A2, 2 · A1 …" as equal rows, show each round as a group: a small round number on the left spanning its rows, the move label (A1, A2) on each row, a slightly stronger divider between rounds than inside them. Keep every existing class, `data-` attribute and tick index; this is markup around the rows plus CSS. The audit and `lib.tick()` must still find `.srow[data-x] [data-tk]` in the same order.
3. **The next set is obvious.** The first unticked row of the block you are in gets an orange left edge and full strength text. Ticked rows drop to 55% opacity with the tick filled. When the rest bar runs, its "Next: …" label already names the same set.
4. **Inputs you can see:** kg and reps boxes get a 1.5 px border (`#C7C7CC` light, `#4A4F58` dark), white or card background, 44 px high, 17 px numbers. The kg placeholder shows the last logged weight for that exercise when there is one ("20"), else "kg". Placeholder only: nothing is prefilled or saved.
5. **"+ round" and "− round"** become 44 px high text buttons, left aligned under the rows.
6. **Guided timer cards:** the Start button gets 16 px of space above it; the "Show N moves" link and the small print share one 14 px style. No behaviour change.
7. **One finish area** at the bottom, as a single card titled "Finish":
   - the outcome chips in one wrapping row (unchanged values and handlers);
   - the Notes box;
   - the `Finish workout` button full width (`#fin`, unchanged id);
   - under the card, one muted line with `+ Add an activity` and `Reset this day…` as two text links.
   The separate "Extra" and "How did it go?" `h2` elements stay in the DOM with the same text (tests and the audit walker know them); in the tabs layout they may be visually hidden with a class, not removed.
8. **Type and spacing pass** for the session screen only: sizes limited to 13, 14, 16, 17, 20 px (the clock digits excepted); card padding 16 px; 12 px between cards; 24 px above a block header; one card radius (16 px) and one shadow (`--sh`). Remove the browser default 13.33 px that leaks into buttons, inputs and selects by setting `font: inherit` on them inside the session.

## Out of scope
- The full screen clock, the Today card, Progress, History, Settings.
- Any change to session content, weeks, timers, audio, cues, logging rules or the export.
- New features. If something looks like a feature, leave it and note it for James.

## Acceptance
- Every existing suite passes untouched, apart from the three tabs suites named above.
- New `tests/test_v61.py`, `test_v62.py`, `test_v63.py` cover: no week row or strip in an open day and Back to the list; first block header y ≤ 330 at 390 × 844; the top bar shows title and "n of m" and updates on a tick; the collapsed question expands to the three chips; the stop signs line and `#safe1` are visible with their full text on a strength day, a run day and an off plan day; the next row marker moves on a tick; kg placeholder shows the last weight; every button and input in an open session is at least 44 px high; contrast of the new text in light and dark; nothing in the session intersects the Back button, the dock or the tab bar at 375 × 667.
- `CLAUDE.md` gets one bullet per release, as for earlier versions.
- Final message to James: what changed in plain words, what was only tested in the simulator, and anything left out.
