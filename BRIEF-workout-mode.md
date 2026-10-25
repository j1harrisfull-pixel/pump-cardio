# Brief: Workout mode rework (for Claude Code)
Goal: one glance per set, then the phone goes down. Simple, not extravagant. Research: docs/workout-mode-research.md (don't put citations in the app).

## Rules that still apply
Single effort words (easy/steady/moderate/hard). Standard terms; km; Concept2 format. Timers only where timing is the workout. No vibration. iPhone PWA: no audio/timers while locked → keep wake lock and the existing "mark done?" prompt. Keep existing rest bar (+15/−15/Skip), logging, history, swap button.

## Two screen types only
**A. List mode** (strength, supersets, carries, accessories) — no block timer.
**B. Clock mode** (EMOM, intervals, AMRAP/flow/circuit, timed mobility) — one full-screen clock.

## A. List mode
- Block card: header "A · Front squat · 4 × 6 · rest 2:00". Rows: set no. | kg | reps | tick (prefilled from plan/last time; last time shown small, grey).
- Tick set → rest timer auto-starts (block's rest). Rest bar at bottom: big M:SS, "Next: set 3 · Front squat 6 @ 60 kg", +15 / −15 / Skip. Beep at 3-2-1 and at 0.
- Supersets (B1/B2): rows alternate B1, B2; rest timer starts only after the last move of the pair (short transition between B1→B2 untimed).
- Carries: row = distance or time (e.g. "Suitcase carry · 40 m · L then R"); tick → rest timer. No countdown during the carry.
- Remove READY/WORK countdown segments from strength/superset/carry blocks (`bSup`, `pushW` usage).

## B. Clock mode (full screen while running)
Layout top to bottom:
1. Small: block name + "Minute 4 of 12" (EMOM) / "Round 3 of 6" (intervals) / elapsed-of-total (AMRAP/flow). Counts work rounds only.
2. **NOW** — one line, very large (≈ 40–48 px, bold): e.g. "Swing × 10" or "Press × 5 · left".
3. **Clock** — biggest element (≈ 96–120 px, tabular digits).
4. **NEXT** — one line, small (≈ 16–18 px, grey): "Next: Goblet squat × 8".
5. Controls row, small icons (≈ 32–36 px tap targets with text labels): Back · Pause · Next · Stop. Optional lock toggle to stop stray taps.
Phase colour: background tint warm orange for work, neutral/dark for rest. Nothing else on screen (no full block list; tap block name to peek).

### EMOM
- One segment per interval (default 60 s). Clock counts that minute down. NOW = this minute's task. Rest = whatever's left; **not separately timed, no READY segment, no auto side switch.**
- Alternating EMOM (min 1 A, min 2 B…): NOW follows the rotation; NEXT shows next minute's task.
- Unilateral: write the side into the minute ("Press × 5 · left", next minute "Press × 5 · right") or "× 5 each side" inside one minute. Never split a minute into timed L/R halves.
- Sounds: 3-2-1 short beeps, long beep at top of minute. Optional single beep at 30 s (off by default).
- Replace `bEmom()` with: for r in rounds, for item in items → one ["WORK", win, label] segment.

### Intervals (row/run/bike)
- Work and rest are both timed (this is the workout). NOW: "Row · 1:00 · moderate"; rest phase NOW: "Rest · easy paddle". Round x of n. 3-2-1 + long beep at each change. Keep a 10 s get-ready only at the very start.

### Flow / circuit / AMRAP
- AMRAP: one countdown for the whole block; NOW shows the whole round as a short list (max 4 lines) since you move at your own pace; tap "+1 round" to count rounds. Beep at halfway (optional) and last 3-2-1.
- Fixed-time flow (e.g. 40 s on / 20 s off per move): treat as intervals — one move per segment, NOW + NEXT.
- Score/rounds/weight entered **once at the end** in a small sheet (rounds, kg, effort word), then auto-tick the block.

### Timed mobility / warm-up
- Same clock mode, one move per segment, NEXT shown; or untimed list if not time-based.

## Sizes / look (whole app)
- Icons 20–24 px in lists, controls 32–36 px tap targets (min 44 px tap height per iOS HIG), fewer buttons. Clock digits tabular, largest thing in clock mode. Body text 16 px. Keep warm orange theme and FD icon.
- Header/time shown only when exact (existing rule).

## Audio (Web Audio, screen on)
- Clock mode: 3 short beeps (3-2-1) + 1 long at each segment change; final double beep at block end.
- Rest timer: 3-2-1 + long at 0.
- Keep `beep()`; unlock AudioContext on Start tap. No speech required (optional later).
- Locked phone: no sound possible → on return, existing "mark done?" prompt.

## Remove
- READY prep segments before every move (keep one 10 s start countdown per clock block only).
- Combined labels like "· switch → right side · round 2/4"; auto L/R split (`pushW` side halves).
- Timers on strength/superset/carry work.
- Rest segments inside EMOM minutes.
- Any secondary small timers competing with the main clock.

## Tests
Update Playwright: EMOM 12 min → exactly 12 segments of 60 s, labels have no "switch"/"READY"; superset block has no timer; ticking a set starts rest bar; clock screen shows NOW/clock/NEXT/minute counter; bump version + sw.js cache.

## Session writing changes (Health & Fitness bot, not code)
1. EMOMs: max 2–3 moves rotating by minute, one task per minute that fits in ~30–40 s, leaving real rest.
2. Repeating patterns: the same rotation every round so it's memorised after round 1; no extra moves mid-block.
3. Sides: either alternate by minute (L minute, R minute) or "× n each side" within a minute — never a timed switch mid-sequence. Prefer bilateral/goblet moves in EMOMs with one 16 kg bell.
