# BRIEF: whole app polish (pc-v61 to pc-v69)

Status: approved by James on 10 Nov 2026 with the scope widened to every screen ("I want everything added to scope. Nothing stays out of scope. We have lots of time to be able to make this legit.").
Read `CLAUDE.md` first (hard rules, build, test, deploy). The work targets the tabs layout (pc-v58 onwards).

## How to run this job
- Do the parts in order, A to I. One release per part: bump, build, full `bash scripts/test.sh` green, one commit, push to `main`, confirm the Pages deploy, then start the next part. Never leave `main` red or half done.
- Never run two copies of `scripts/test.sh` at once, and never commit while one is running (`test_sw.py` rewrites `sw.js` for a moment). Check `head -c 22 sw.js` before every commit.
- Look before you ship: screenshots in light and dark at 390 × 844 and 375 × 667 of every screen the part touches, read with your own eyes, compared with the screenshot from before the change.
- If a part cannot be made green after three honest attempts, revert that part, write down what blocked it in the final message, and go on to the next part.
- James is asleep. Do not ask questions; take the sensible default, and list every judgement call in the final message.

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
An app that looks designed, not assembled: every screen has one clear job, one type scale, one spacing rhythm, one set of controls, in light and in dark. Start with the session screen (parts A to C), then the clock, Today, Week, Progress with History, Settings with every sheet, and finish with a system pass and a fresh walkthrough. No change to what is saved.

## Rules for this job
- **Keep the flat layout working.** `wo_flat=1` exists so 33 older suites and the audit keep running. Scope page layout changes under `body.tabs`. Shared pieces (the full screen clock, the sheets, the saved card, toasts, buttons, inputs) may be restyled for both layouts, as long as every older suite still passes; change an older suite's expectation only where this brief changes the behaviour it checks, and say so in the commit message.
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

## Part D (pc-v64): the full screen clock
The clock is what James looks at mid effort, at arm's length, with sweaty hands. Keep NOW, the digits and NEXT exactly as readable as now; fix the controls and the clutter.
1. **Controls in the thumb zone.** Move the control row to the bottom of the screen above the safe area. One large primary button, Pause / Resume, at least 64 px high and the widest. `◀ Back` and `Next ▶` either side as secondary buttons. Keep every id (`#tback`, `#tpause`, `#tnext`, `#stop`, `#tlock`).
2. **Stop is separate and asks first.** Stop moves away from Pause (top right corner of the clock, text button "Stop"). A tap asks "Stop this timer? Your place is not saved." with Stop and Keep going. The "finished while locked" prompt is unchanged.
3. **Lock** uses an inline SVG padlock (not the emoji), with the word. While locked, only Unlock responds, and the locked state is obvious (controls dimmed, "Locked · tap to unlock").
4. **One block progress bar**: a thin bar across the top of the clock showing elapsed of total for the block. It replaces nothing; the "Minute 3 of 15" counter stays.
5. **NEXT never repeats NOW.** When the next segment has the same label as the current one, show "Next: same again" or the round number, not the same words twice. Sides always read "each side" (never "each hand") unless the move name itself contains it.
6. **Session time** stays visible on the clock, small, top left, as plain text (no pill, no stop button). Lap still works by tapping it.
7. Dark and light both keep the current phase colours. The cue wash and the 3-2-1 pulse are unchanged.

## Part E (pc-v65): Today
1. **Header that means something.** Keep the brand kicker and the session title. Replace the lone ring with a week ring: sessions done of planned this week, with the number inside ("2/5"). Under the title: the date and one status word (Not started, In progress, Paused, Logged, Skipped, Rest day).
2. **The session card** (the block preview) becomes the centrepiece: block name, a small type tag (Warm-up, Superset, Carry, Flow), time or rounds right aligned, a tick on finished blocks, and the first unfinished block marked "Up next". The card is still one tap target that opens the session without starting the clock.
3. **After logging**, the card turns into a summary: what was done (session name or the replacement), minutes, sets or km, feel if given, and one line "Tomorrow: <session name> · ≈ N min" (or "Tomorrow: rest"). The button reads View today. No percentage that contradicts "Logged".
4. **Rest day and unplanned week** get a proper empty state: a short friendly line, what is next ("Wednesday: Hill Hunter Run"), and the one useful action.
5. **Prompts stack in a fixed order with one orange button on the screen at most:** today's action first, then yesterday's prompt, then the Sunday review. Secondary prompts use neutral buttons and can each be dismissed.
6. **Settings** stays reachable from Today as a 44 px button with a cog icon (inline SVG) in the top right of the header, clear of the ring. Remove the text link under the card.

## Part F (pc-v66): Week
1. **Rows with clear states**, as small chips on the right: Done (green tick), Skipped (grey), Not logged (amber outline), Today (orange), Rest (no chip, quieter row), future (no chip). A replaced day shows what was done with "instead of …" under it.
2. **A week header card** above the list: the dates ("9 to 15 Nov"), sessions done of planned as seven small dots (filled, hollow, dash for rest), runs and km. The arrows sit either side of the dates. Swiping the list left or right changes the week, as the strip did.
3. **Edit plan** becomes a clearly labelled button under the list ("Edit this week's plan"). In edit mode the strip appears with its existing behaviour and a "Done" button; explain the two gestures in one line ("Tap a day to cycle it. Swap days moves two sessions.").
4. **Unplanned week**: one card saying nothing is planned yet, what to do (Settings, Import week), and that any activity can still be logged on a day.

## Part G (pc-v67): Progress and History
1. **Four tiles that line up**: same height, number, unit, label, and one comparison line in the same place on each ("last week 3"). Sessions, runs, km, running minutes.
2. **Last 4 weeks as bars**: one row per week with a slim bar for sessions done of planned and the run total beside it. Keep the text values (the tests read them); the bar is decoration with `aria-hidden`.
3. **Strength by exercise**: one card per exercise with the last three entries and the trend arrow; tapping the card opens the existing exercise history sheet. Show five, with "Show all".
4. **Recent runs**: date, distance, time, effort as a tidy four column row.
5. **A real empty state** when nothing is logged: one friendly line and what will appear here.
6. **History as cards**: date and name on the first line, minutes right aligned, details under it in 14 px. The three controls (change type, Edit run, Delete) move behind one "…" button per entry that opens a small action sheet. Delete still confirms. History is open by default on this tab (no bare disclosure triangle). Export and the backup line sit together in one card at the top: "Last backup 3 days ago" + "Export history".

## Part H (pc-v68): Settings and every sheet
1. **Settings in sections** with headings: Timers (auto rest), Cues (flash, beep on silent with its music warning as a second line of small text), Plan (the weeks list, Import week), About (the app version from the meta tag, "Data stays on this phone", Reset is not here). Tick boxes become switches drawn in CSS on the same `input type="checkbox"` elements (ids unchanged), orange when on, 51 × 31 px, the whole row tappable.
2. **One sheet style for all sheets** (How-to, exercise history, Edit run, Import week, Export, score, swap, settings, the new action sheet): same radius, grab handle, title size, close button position and size (44 px), padding, and a scrim that closes on tap. Sheets never leave the dock or the tab bar tappable underneath.
3. **Forms**: every text and number field in the app uses the Part C input style. Labels 14 px above the field. Chips have one size and one selected style everywhere.
4. **The saved card**: same card style, the minutes large, the details list left aligned and readable, Done as the one orange button, Undo as a text link. The praise line uses `--accent-ink`.
5. **Toasts**: one style, above the dock, never covering a primary button; an optional action ("Undo") is supported and used for the one tap Skipped on yesterday's prompt, so that flow becomes a single tap with a 6 second Undo.

## Part I (pc-v69): system pass and a fresh walkthrough
1. **Tokens.** Add CSS variables for the type scale (13, 14, 16, 17, 20, 28), spacing (4, 8, 12, 16, 24), radius (12, 16, pill) and use them across the stylesheet where it is safe. Remove dead rules left by earlier themes only when you can show they match nothing (search the built page and the renderers first).
2. **Icons.** One small inline SVG set, same stroke width, used for every icon in the app (tabs, cog, more, lock, tick, close, back, timer). No emoji as controls.
3. **Dark mode audit** of every screen and sheet: no white surfaces, no borders that vanish, contrast measured for every text colour on its background.
4. **Access.** Every button has a name; sheets trap focus and restore it; `prefers-reduced-motion` turns off the wash animation and transitions (the flash setting still governs whether cues show); text scales sensibly with the phone's larger text setting up to 120% without clipping.
5. **Sizes.** Check 375 × 667, 390 × 844, 430 × 932 and landscape 844 × 390: no horizontal scroll, nothing clipped, nothing under the notch or the home indicator.
6. **Walkthrough.** Send three fresh testers through the finished app, as in the pc-v58 walk (everyday use; visual design in light and dark; navigation and edge cases), with the same rule that they change no files. Fix every finding they rate blocker or annoying in the same release; list the polish items you left.

## What never changes (these are guardrails, not scope)
James asked for everything to be in scope. Every screen and every visual detail is. These are not scope items and stay as they are:
- Saved data: no key renamed, no field's meaning changed, old logs keep rendering.
- The medical safety rules in `CLAUDE.md`, the stop signs line in full on every session, the effort words and the banned terms.
- Session content, weeks, timer maths, audio behaviour (music first), and the export format that Grok reads.
- No network calls, trackers or external files; the app works offline.
- New features that change what the app does (as opposed to how it looks and flows) are noted for James, not built.

## Acceptance
- Every existing suite passes. Expectations change only where a part of this brief changes the behaviour checked.
- One new suite per release (`tests/test_v61.py` to `test_v69.py`), added to `FULL` and `FAST` in `scripts/test.sh`. Parts D to I each check their numbered points the same way (positions, sizes, text, contrast, ids still present, old behaviour intact). For parts A to C they cover: no week row or strip in an open day and Back to the list; first block header y ≤ 330 at 390 × 844; the top bar shows title and "n of m" and updates on a tick; the collapsed question expands to the three chips; the stop signs line and `#safe1` are visible with their full text on a strength day, a run day and an off plan day; the next row marker moves on a tick; kg placeholder shows the last weight; every button and input in an open session is at least 44 px high; contrast of the new text in light and dark; nothing in the session intersects the Back button, the dock or the tab bar at 375 × 667.
- `CLAUDE.md` gets one bullet per release, as for earlier versions.
- Final message to James, in his style (UK English, bottom line first, short lines, no em dashes or hyphens in prose): what shipped per release, what was only tested in the simulator, every judgement call, anything reverted or left out, and what to check on his phone.
