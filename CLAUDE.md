# CLAUDE.md – Pump + Cardio (pump-cardio)

## Project overview
This is a personal workout PWA for **James Harris**. It runs as an iPhone Home Screen web app, live at
https://j1harrisfull-pixel.github.io/pump-cardio/ (GitHub Pages, `main` branch, repo root).

- **Week strip:** Mon to Sun with the planned session for each day. Tap a day to open the session panel.
- **Each day:** a **main** session, an optional **backup** (lower-energy) session, and on some days a **Run instead** variant or a **Quick option** (e.g. Sat 17 Oct "15-min KB Flow (16 kg)").
- **Two screen types (pc-v30 workout mode, see BRIEF-workout-mode.md):**
  - **List mode** for strength, supersets and carries: one card per block, rows of set | kg | reps | tick (supersets alternate B1, B2), tempo chips and How-to sheets. Ticking a set starts the rest bar (−15 s / +15 s / Skip, "Next: set 3 · Name 6 @ 60 kg"). No block timer.
  - **Clock mode** for EMOM, Every, intervals, circuits, flows, steady pieces and AMRAP: one full-screen clock with the block name + counter, NOW (large), the clock (largest), NEXT (small), and Back / Pause / Next / Stop / Lock. One 10 s get-ready at the start, 3-2-1 + a long beep at each change, a double beep at the end.
- **Logging:** "Finish workout" logs the day (name, type, weights, sets, km, feel, notes). History lets you change a logged day's type (Main / Backup / Run instead / Quick option).
- **Actual running (pc-v35):** run days have an *Actual* card (distance km with decimals, elapsed time mm:ss, effort word, feel, notes), never prefilled from the plan. Other sessions get a small **+ Add a run**, which saves one `type:"extra"` log entry ("Extra run") for that date, updated in place. **Edit run** in History edits either kind. **Export history** in History builds a readable text + the raw `wo_log` JSON and hands it to the iOS share sheet (fallback: a copy sheet). Nothing leaves the phone otherwise.
- **Outcome + different run (pc-v37):** every non-rest session ends with a **How did it go?** card: one-tap chips *as planned / modified / cut short / skipped* (`wo_<date>.oc`, saved to the log as `oc`) and, on non-run days, a Notes box (`wo_<date>.nt`, becomes `notes` if the log has none). Run days have **Plan: As prescribed / Did a different run** chips on the Actual card (`wo_run_<date>.sub` + `sl` text); Finish then logs `sub` (what was run) and `plan` (the prescribed piece, from `planOf`, e.g. "Easy run 5 km 31:00") and the log line reads "did 5K easy run instead of Easy run 5 km 31:00". Edit run in History can set or clear it. Since pc-v38 `hasRun(S)` (a `fields` block **or** a counted run block such as "KB EMOM 15 + Run") decides whether a session gets the Actual card and logs km / time / effort / sub; only sessions without any run get **+ Add a run**. The export starts with a **SUMMARY** (`exportSummary`): last weights and reps per exercise, runs by week (w/c Monday · count · km · min), swapped days, different runs, outcomes, planned but not logged days. `docs/grok-handover.md` describes the data for the Health & Fitness bot.
- **Progression in the app (pc-v40):** `suggest(x, it)` reads the last logged sets of the same exercise (`lastSets`): every set at or above the target reps → one step up (`kstep`: 2 kg dumbbells, 4 kg kettlebells), a short set → same weight, always qualified "only if it felt RPE 6–7". The line sits under the move in list mode with a **Use N kg** button (`fillKg`: fills the unticked sets, writes `wo_<date>.kg` and `wo_wt`). Timed and distance items (`ru`) get no suggestion. **Progress** (a `details` above History, `progress()`): last 4 weeks (done of planned from `PROG`, rest sessions excluded, skipped and extra runs not counted as done; runs, km, min), strength by exercise with the last 3 entries and a trend arrow, recent runs.
- **Offline:** works offline via `sw.js`. Since pc-v36 the worker is **cache first** (the app opens at once on a weak signal; the network copy refreshes the cache in the background), so a new version only arrives through the update prompt / `reg.update()`.

**Read first:** `app-style-standard.md` (the approved layout standard). **Next approved jobs:** `BRIEF-beauty-pass.md` (white + orange visual beauty pass), then **`BRIEF-day-swap.md`** (swap two day slots in the current week). Older briefs: `BRIEF-workout-mode.md`, `BRIEF.md`.
Background notes are in `docs/`: the week-1 programme, terminology audit with sources, and premium-app research.

## Repo layout
```
index.html            BUILT single-file app (served by Pages). Never edit by hand; run bash scripts/build.sh
sw.js                 service worker; cache name var V="pc-vNN" (must match the page marker)
manifest.json         PWA manifest with embedded icons (leave as is)
.nojekyll             serve files as-is on Pages
src/top.html          <head>, CSS (theme variables; beauty pass → white + orange) and the static markup (#bar, #rbar, panels)
src/app.js            all logic and session data (the script continues straight from top.html)
scripts/build.sh      index.html = src/top.html + src/app.js
scripts/bump.sh NN    pc-vOLD -> pc-vNN in src/top.html, sw.js, tests/test_sw.py
scripts/test.sh [--fast | suite…]  build, serve the repo root on :8765, run the Playwright suites in parallel (JOBS=3)
tests/lib.py          shared test library: page setup (view), timers (run_block), the style-standard audit (audit_view), week discovery
tests/test_audit.py   data-driven audit of every view in every programmed week + every guided block + data rules (WEEK=current for this week only)
weeks/                one JSON file per programme week (pc-v39), inlined by build.sh; see docs/week-format.md
tests/test_*.py       per-release regression suites (Playwright, Python sync API, iPhone viewport 390×844)
docs/                 programme notes, research; beauty-pass-mocks/ + beauty-pass-research.md for the light theme
app-style-standard.md layout standard + 159-deviation audit
BRIEF-beauty-pass.md  next job: white + orange visual beauty pass (approved 5 Nov 2026)
BRIEF-day-swap.md     next job after beauty pass: swap two days in the current week (approved 5 Nov 2026)
BRIEF.md              older brief (pc-v28 layout/timer); kept for history
```

## Architecture
**Single-file PWA, no framework and no build tooling beyond `cat`.** It's plain ES5-style JS with global functions. Everything ends up inline in `index.html`, so keep it dependency-free.

### Session data model (`src/app.js`)
- **`X`**: exercise library, `id -> [display name, suggested weight text, weight range, hasWeight 0/1]`.
- **`HT`**: How-to sheets keyed by exercise id or display name: `{q: demo search, u: summary, s: steps (≤12 words each), c: tips, m: mistake, z: safety}`.
  - **`HAL`**: maps alternative names to HT keys. `hkey(name)` strips "(…)", " – …" and ", …" before the lookup.
  - Every move shown must resolve to a How-to; test_v18 checks this.
- **`MV`**: reusable move lists for warm-up and cool-down flows.
- **`SESS`**: `id -> {name, short (week-strip label), safe (safety line), g0 (tick-index offset: 100 for backups, 200 for quick), was? (old names, see `ALIAS`), blocks:[…]}`. Block kinds:
  - `{k:"timer", id, h, name, note, segs:[[PHASE, seconds, label], …], list?, groups?, small?, flow?, counter?}`: a guided timer. Since pc-v28 `h` is the §1 format (Warm-up, Intervals, Circuit × 2, Steady, Flow, Cool-down, Every 2:00 × N), `note` the fixed §2 instruction line and `small` (string or array) the small print. Button labels come from the renderer (`Start guided flow` / `Start guided timer` · m:ss).
    - PHASE is one of READY, WORK, REST, WARM-UP, EASY, STEADY, JOG, FLOW, STRETCH, MOBILITY, FINISH, …
    - **`clk(b, segs)` normalises every guided block in the post-pass**, so session data keeps its existing format (READY set-ups, "– left side · round 2/4" labels, `iv`/`ivr`/`core`/`fl` builders all still work):
      - EMOM / Every blocks (`h` "EMOM 60 s × N" / "Every 2:00 × N") become one `WORK` segment per window; sides go inside the minute ("· left", "· right" or "· each side"); rest is never timed and the last window is full length.
      - Other blocks drop READY prep (the first one, and every one in flows); a READY between moves becomes or joins a `REST`. Labels lose "Interval k of n" / "round r/n" / "switch →" text and sides read "Name · left" / "Name · right".
      - Interval work labels become `Machine · m:ss · effort` (e.g. "Row · 0:50 · moderate"). Segments carry the round number as an optional 4th element.
      - `b.amrap` (with `list`) gives an AMRAP: one countdown, the whole round as NOW, a "+1 round" button and a score sheet at the end (`wo_<date>.sc[id] = {r, kg, e}`).
      - **EMOM groups (pc-v35):** `emomPlan(b)` derives one group per minute of the cycle from the normalised minute labels plus `list`: the cycle is the shortest repeating run of labels; a minute labelled `… · left` / `… · right` takes the `list` moves marked `each side`, any other minute takes the unsided moves named in its label (`Swing ×15 + goblet squat ×5` → "15 swings, then 5 goblet squats"). The card shows `Minute 1 · Left` groups, a "Repeat this three minute cycle five times." line and "Start each group on the minute. Rest for whatever remains of that minute."; `small` is not shown for EMOMs (every minute is a full window). The clock reads the same plan (`T.plan`): NOW = side, `#nowd` = the moves, NEXT = next minute. So when the bot writes an EMOM: labels `Complex · left` / `Complex · right` / `<move> ×N [+ <move> ×N]`, and `list` entries `Name – ×N[ each side]`.
  - `{k:"ex", h ("A · Superset"), mode:"sup", n, rr:[lo, hi], tid, items:[{x, lab, rp, side, tp (tempo e.g. "3011"), ru ("s" | "m"), sw, cue}], fill?, gn?}`: a strength or carry block, rendered in list mode by `listBlock`.
    - No guided timer and no header time: the header reads `N · A · Superset · 4 rounds`, the line `Each round: A1 → A2. Rest 60–90 s.`
    - `b.rest` = middle of `rr`; the rest timer starts with it when the last move of a round is ticked (each tick for a one-move straight set) (`maybeRest`). `b.est` (`bEst`, no segments) is the estimated time used in the `≈` day total.
    - `mode:"emom"` / `mode:"every"` build a clock from the items (`bEmom` / `bEvery`: one `WORK` segment per minute / round, label "Name × reps [each side]"). Unused so far.
  - `{k:"fields"}` holds optional log fields; `{k:"rest"}` marks a rest day.
- **Builders:**
  - `fl(id, h, name, note, moves, phase, dir)` builds flows. It merges "– left/– right" and "– each side" moves into cued halves, orders standing → kneeling → floor (warm-ups the reverse) using `posOf`, and adds GET READY only on a position change.
  - `iv` / `ivr` build intervals with no trailing rest.
  - `tm(...)` builds a single-segment timer.
- **Totals:** a post-pass sets `S.tot`, `S.nt` and `S.est` (strength estimates included, so the day note shows `≈ NN min`). Displayed block times must equal the real timer totals (enforced by tests).
- **Calendar lookups** (date `YYYY-MM-DD` -> session id):
  - `PROG`: the week's main sessions.
  - **`OVR`**: one-day override of the main session (backups unchanged).
  - `BK`: backup for each day.
  - `QK`: quick option for each day.
  - `RI` / `RIN` / `RIS`: Run-instead block replacements, names and safety lines. Run-instead must keep identical segment totals; the code throws otherwise.
  - `ALIAS`: renamed session → old names. `sameE` treats a log saved under an old name as that day's log, and updating it keeps the old name.
  - Legacy days up to `LEGACY_END` use `PAT` / `DEFP` / `LEG`.
- **Resolution:** `sid(date)` resolves rest override (wo_plan) → quick (`wo_quick`) → backup (`wo_alt`) → main.
  - **Swap days (pc-v34):** `srcOf(k)` reads `wo_daymap`; `baseSid`, `bkOf`, `qkOf` use the source date, so a moved session brings its backup, quick option and run-instead version with it. The toggles (`wo_alt`, `wo_ri`, `wo_quick`, `wo_plan` Rest), ticks (`wo_<date>`) and logs stay on the calendar date. Only days in the current week can be swapped, and never a day that is logged or has ticks / done flags (`swapBlock`). The coach-request "Swap today's session" (`wo_swaps`) is a separate feature.
  - `S_(date)` returns the session, wrapped as a run view when Run instead is on.
  - `curType(date)` returns `main`, `backup`, `run` or `quick`.
  - `typeOpts` / `setType` drive the history Edit dropdown.
- **Timer engine:** timestamp-based (`T.t0`, pause stores `T.pa`). `setInterval(loop, 250)` only renders. `startT` prepends one `["READY",10,"Get ready"]` (`T.pre`); the header time and block total exclude it. `ctr()` writes the top line (Minute x of N, Round x of N, or elapsed of total).
  - A gap over 2.5 s after the end (phone locked) shows "FINISHED WHILE LOCKED · Mark done / Not done".
  - Audio uses one AudioContext, resumed on every tap and on `visibilitychange`. It handles the iOS "interrupted" state. `beep()` also pushes to `window.__bp` for tests.
  - **Never rely on `navigator.vibrate`**: iOS has no vibration API.
  - **Silent switch (pc-v36):** iPhone mutes Web Audio when the ring switch is on silent unless an audio element is playing, so `keepAudio(true)` loops the tiny silent clip `#snda` while a guided or rest timer runs and `relWake()` pauses it when both are stopped. Untested on a real iPhone so far.
  - Screen Wake Lock is held while today's panel is open.

### localStorage keys (all JSON). Compatibility rules
| Key | Content |
|---|---|
| `wo_log` | array of logged days `{date, name, type: main/backup/run/quick/extra, sid, min, sets, of, w, wt, rp: {id: {v, u, k?}}, sc?, km, time?, effort?, feel, notes, breaks, ri, custom, mig, extra?}` (`rp[id].k` per-set kg and `sc` AMRAP scores are optional, pc-v30; `time` "mm:ss", `effort` easy/steady/moderate and `type:"extra"` + `extra:1` for an added run are optional, pc-v35; `oc` planned/modified/cut short/skipped, `sub` what was run instead and `plan` the prescribed piece are optional, pc-v37) |
| `wo_<date>` | that day's ticks/state `{t: {"gi_round": true}, rp: {"gi_round": reps}, kg?: {"gi_round": "kg"}, w, r, s: {timerId: 1}, sc?: {timerId: {r, kg, e}}, start, oc?, nt?}` (`kg` and `sc` are optional, pc-v30; `oc` outcome chip and `nt` notes draft, pc-v37) |
| `wo_run_<date>`, `wo_runstart_<date>` | run-day fields `{b: walk breaks, d: km, t?: "mm:ss", e?: effort word, f: feel, n: notes, s}` and start time (pc-v35 adds `t`, `e`; pc-v37 adds `sub` 0/1 and `sl` the different-run text; on non-run days the same key holds the Add a run draft) |
| `wo_wt` | weights `{exerciseId: {date: "kg"}}` (feeds "Last: 16 kg") |
| `wo_alt`, `wo_ri`, `wo_quick` | per-day `{date: 1}` toggles for backup / run instead / quick option |
| `wo_plan` | user plan edits (e.g. `{date: "Rest"}`) |
| `wo_daymap` | swapped day slots in a week `{calendarDate: sourceDate}` (pc-v34, optional). Calendar date K shows the main session of source date V; missing key or a bad value = no remap. Written in pairs by Edit plan → Swap days; identity entries are deleted |
| `wo_timer`, `wo_rest`, `wo_restlast`, `wo_autorest` | running guided timer, running rest timer, last manual rest, auto-rest setting (default on) |
| `wo_swaps` | queued "swap today's session" requests |
| `wo_startdate`, `wo_ver` | programme start date and data version (migrations in `migrate()`) |

**Rules:**
- **Never break saved logs.** Never rename or delete keys or change the meaning of existing fields. New fields must be optional, and readers must tolerate missing or old shapes.
- Any data fix is a **one-time, idempotent migration** in `migrate()`, guarded by a flag or version. See the 2026-10-14 v24 migration.
- **Exercise ids** (keys of `X`) and **block / timer ids** are persisted in ticks, weights and done-flags, so never rename them. Add new ids instead.
- **Tick indices:** item `gi` indices are positional within a session, offset by `g0`. Don't reorder or insert items in a session that already has logged ticks for past days. Append, or create a new session id and point the calendar at it.
- Sessions for past dates must keep rendering, so keep old session ids in `SESS`.

## Build, test, deploy
```bash
pip install -r requirements-dev.txt && python -m playwright install chromium   # once
bash scripts/build.sh                     # after every edit to src/
bash scripts/test.sh --fast               # this week's audit + app/v31/v34/v35: about 3 min, for every change
bash scripts/test.sh                      # every suite in parallel, about 10 min, before a release; or: bash scripts/test.sh test_v26
CHROME=/usr/bin/google-chrome bash scripts/test.sh   # optional: system Chrome instead of bundled Chromium
```
- **Write new tests with `tests/lib.py`** (`from lib import *`): `view(b, date, seed)` opens a day, `run_block(p, tid)` drives a guided block to the end in a fraction of a second (it jumps inside segments and ticks across every boundary, so beeps, countdown and the done flag are still checked), `audit_view` is the standard audit, `fin(p)` finishes a workout. Don't copy helpers between suites.
- `test_audit.py` finds the weeks in `PROG` itself and audits every main / backup / quick / run-instead view, so **a new week needs no new rendering or timer tests**; only week-specific content checks (progression, How-to, limits) go in a `tests/test_vNN.py`.
- The tests serve the repo root at `http://localhost:8765/index.html` and use Playwright's fake clock.
  - Use `page.clock.run_for(ms)` to advance timers.
  - `fast_forward` simulates a locked phone and triggers the "finished while locked" prompt.
- `test_sw.py` temporarily rewrites `sw.js` and restores it (the runner keeps it on its own, after the parallel batch). Afterwards, check that `head -c 22 sw.js` shows `var V="pc-vNN"`.
- **Update or add tests with every change.** Name new suites `tests/test_vNN.py`; the existing suites must keep passing (update their expectations only when the brief changes the behaviour).

**Deploy = push to `main`.** GitHub Pages serves the repo root. For each release:
1. `bash scripts/bump.sh NN`. This updates `<meta name="app-version" content="pc-vNN">` in `src/top.html`, the `sw.js` cache name and `tests/test_sw.py`.
2. `bash scripts/build.sh`, then `bash scripts/test.sh`. Everything must pass.
3. Make **one commit per change** (index.html, sw.js, src and tests together) and push.
4. Confirm it's live: `curl -s https://j1harrisfull-pixel.github.io/pump-cardio/sw.js | head -c 22` shows the new version, and the live `index.html` is identical to your local build (`cmp`). Pages takes about 30–90 s.

Keep `index.html`, `sw.js` and `manifest.json` at the repo root: the installed PWA depends on these paths.

## Hard rules
### Safety (James has a pituitary macroadenoma; endocrine admission Wed 28 Oct 2026)
- **Effort:** RPE 6–7 for strength, stopping 2 reps short of failure (2 RIR). Conditioning uses the effort bands below; **hard (RPE 8+) is not used**.
- **No breath-holding / Valsalva.** Every strength move says to breathe out on the effort.
- **No head-down or inverted positions.** No maximal lifts, heavy barbell work or **heavy spinal loading**. No snatches to fatigue.
- The **stop-signs line** must stay visible in every session: "Stop and get checked if you get a sudden or severe headache, any vision change, dizziness or feel sick."
- If a request conflicts with these rules, don't build it; flag it to James.

### Terminology
- Use standard fitness terms: Superset, Tri-set, EMOM, Every 2:00, Intervals, Zone 2, RPE, RIR, tempo (e.g. 3011), Assault Runner.
- **Single effort words only**, always written with their RPE band: **easy RPE 3–4 · steady RPE 5–6 · moderate RPE 7 · hard 8+ (unused)**. No combined or hyphenated terms ("moderate-hard", "steady (moderate)").
- Distances in **km** (runs) and **m** (rows from the PM5, carries). Rower work follows the **Concept2 PM5 format**: "6 × 1:00 / 1:00 rest", stroke rate in s/m, damper 4–5.
- **No exact paces or speeds:** no min/km, km/h, /500 m splits, drag factor, or distances derived from pace.
- No "Based on…" source lines or glossary in the app; sources live in `docs/`.
- Move names spell out kettlebell/dumbbell. "each side" is always spelled out.

### Product and process
- Keep it **simple and readable** on an iPhone. Theme: **white + orange** beauty pass (`BRIEF-beauty-pass.md`; CSS variables in `src/top.html`). Since pc-v36 text on orange fills is near black (`#111`, 8:1) and small orange text uses `--accent-ink` `#B34F00` (5.2:1 on white); `#FF8A3D` stays for fills, the ring and the day pill. Follow `app-style-standard.md` for layout wording.
- Make **one commit per change** with a clear `pc-vNN: …` message.
- **Never break saved logs** (see the compatibility rules above).
- Don't add trackers, external scripts or network calls; the app must work offline.

## Weekly sessions
**Since pc-v39 a week is data, not code.** One JSON object per week (`docs/week-format.md`, worked example `docs/week-sample.json`):
`{v:1, week:"<monday>", x, ht, hal, sess:{id:{name, short, safe, g0?, blocks:[spec…]}}, days:{date:{main, backup?, quick?}}, ri, rin, ris}`.
Block specs (`flow`, `tm`, `iv`, `core`, `emom`, `timer`, `ex`, `fields`, `rest`) are built by `mkBlock` with the same builders the code uses.
`validateWeek` enforces the hard rules (Monday week, ids, How-to coverage, banned terms, effort words, run-instead totals) and `applyWeek`
merges into `X`, `HT`, `HAL`, `SESS`, `PROG`, `BK`, `QK`, `RI`, `RIN`, `RIS` before the post-pass. Two routes in:
- **`weeks/<monday>.json` in the repo**: `scripts/build.sh` inlines every file as `WEEKS_BUILTIN`; `tests/test_v39.py` validates each file. This is how the Health & Fitness bot should add a week now (no JavaScript edits, no new test suite needed; the data-driven audit covers rendering and timers).
- **Import on the phone**: History → Weeks → Import week → paste → Check → Save (`wo_weeks`, applied after the built-in weeks, removable from the same list). The page reloads to rebuild.
A week never replaces a session id that already exists in the code. Weeks 1 to 4 stay as JavaScript (`// ==== WEEK N` blocks); Claude Code should not change session content unless asked.


- How a week is added today (pc-v29, week 2): one `// ==== WEEK N …` block in `src/app.js`, just above `// ---- backups`. It holds new `X` ids with `HT` How-to entries, `HAL` aliases, and `Object.assign(SESS,{…})` with that week's main sessions (`mob19`, `up20`, …) and backups (`bk19`…, `g0:100`). It's followed by date entries in `PROG` / `BK`, plus `Object.assign(RI/RIN/RIS,…)` for Run-instead versions. The weekly plan and rationale go in `docs/programme-weekN.md`. Rendering, the style audit and the timer runs of the new week are covered automatically by `tests/test_audit.py`; add only the week's content checks (programme mapping, progression vs last week, time limits) to `tests/test_vNN.py`, written with `tests/lib.py` (see `test_v32.py` for the shape), and add it to `FULL` in `scripts/test.sh`.
- **Writing timed blocks (pc-v30):** EMOMs use `h:"EMOM 60 s × N"` with 2–3 moves rotating by minute, one task per minute that fits in about 30–40 s; the same rotation every round; sides alternate by minute or are "× n each side" inside one minute (see BRIEF-workout-mode.md). Old-style segments still load: `clk()` converts them.
- **Future improvement (not done yet; only on request):** make weekly additions lower-touch with one clear `WEEKS` data section, e.g. `WEEKS["2026-10-19"]={days:{mon:{main:"mob19",backup:"bk19"},…}}`. `PROG`, `BK`, `QK` and the RI tables would be derived from it, and the test `DAYS` / `VIEWS` would be generated from it. Session ids and block ids must stay unchanged so saved logs keep working.
