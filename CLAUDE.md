# CLAUDE.md – Pump + Cardio (pump-cardio)

## Project overview
This is a personal workout PWA for **James Harris**. It runs as an iPhone Home Screen web app, live at
https://j1harrisfull-pixel.github.io/pump-cardio/ (GitHub Pages, `main` branch, repo root).

- **Week strip:** Mon to Sun with the planned session for each day. Tap a day to open the session panel.
- **Each day:** a **main** session, an optional **backup** (lower-energy) session, and on some days a **Run instead** variant or a **Quick option** (e.g. Sat 17 Oct "15-min KB Flow (16 kg)").
- **Blocks:** warm-up flows, strength blocks (rep pills, kg entry, tempo chips, How-to sheets), guided timers (EMOM / Every 2:00 / intervals / flows) with Pause/Back/Next/Stop and beeps, and an auto rest timer for strength sets.
- **Logging:** "Finish workout" logs the day (name, type, weights, sets, km, feel, notes). History lets you change a logged day's type (Main / Backup / Run instead / Quick option).
- **Offline:** works offline via `sw.js`, with an update prompt when a new version is deployed.

**Read first:** `app-style-standard.md` (the approved layout standard) and `BRIEF.md` (the next approved job).
Background notes are in `docs/`: the week-1 programme, terminology audit with sources, and premium-app research.

## Repo layout
```
index.html            BUILT single-file app (served by Pages). Never edit by hand; run bash scripts/build.sh
sw.js                 service worker; cache name var V="pc-vNN" (must match the page marker)
manifest.json         PWA manifest with embedded icons (leave as is)
.nojekyll             serve files as-is on Pages
src/top.html          <head>, CSS (warm orange dark theme) and the static markup (#bar guided timer, #rbar rest timer, panels)
src/app.js            all logic and session data (the script continues straight from top.html)
scripts/build.sh      index.html = src/top.html + src/app.js
scripts/bump.sh NN    pc-vOLD -> pc-vNN in src/top.html, sw.js, tests/test_sw.py
scripts/test.sh [suite…]  build, serve the repo root on :8765, run the Playwright suites
tests/test_*.py       Playwright (Python, sync API) suites at iPhone viewport 390×844 (test_v28 = automated style-standard audit)
docs/                 programme-week1.md, terminology-audit.md (test_v20 reads both), premium-apps-research.md
app-style-standard.md layout standard + 159-deviation audit
BRIEF.md              next job: acceptance criteria and the tests to update
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
    - A label containing `switch → right side` triggers the SWITCH SIDES cue.
  - `{k:"ex", h ("A · Superset"), mode:"sup", n, rr:[lo, hi], tid, items:[{x, lab, rp, side, tp (tempo e.g. "3011"), ru ("s" | "m"), sw, cue}], fill?, gn?}`: a strength or carry block (pc-v28: all of them).
    - No guided timer and no header time: the header reads `N · A · Superset · 4 rounds`, the line `Each round: A1 → A2. Rest 60–90 s.`
    - `b.rest` = middle of `rr`; the rest timer starts with it when the last move of a round is ticked (each tick for a one-move straight set) (`maybeRest`). `b.est` is the estimated time used in the `≈` day total.
    - `mode:"every"` / `mode:"emom"` (`bEvery` / `bEmom`, guided `b.timer`) are kept for true EMOM blocks but unused; a strength block may only use them if every window leaves ≥15 s of real rest.
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
  - `S_(date)` returns the session, wrapped as a run view when Run instead is on.
  - `curType(date)` returns `main`, `backup`, `run` or `quick`.
  - `typeOpts` / `setType` drive the history Edit dropdown.
- **Timer engine:** timestamp-based (`T.t0`, pause stores `T.pa`). `setInterval(loop, 250)` only renders.
  - A gap over 2.5 s after the end (phone locked) shows "FINISHED WHILE LOCKED · Mark done / Not done".
  - Audio uses one AudioContext, resumed on every tap and on `visibilitychange`. It handles the iOS "interrupted" state. `beep()` also pushes to `window.__bp` for tests.
  - **Never rely on `navigator.vibrate`**: iOS has no vibration API.
  - Screen Wake Lock is held while today's panel is open.

### localStorage keys (all JSON). Compatibility rules
| Key | Content |
|---|---|
| `wo_log` | array of logged days `{date, name, type: main/backup/run/quick, sid, min, sets, of, w, wt, rp, km, feel, notes, breaks, ri, custom, mig}` |
| `wo_<date>` | that day's ticks/state `{t: {"gi_round": true}, w, r, s: {timerId: 1}, start}` |
| `wo_run_<date>`, `wo_runstart_<date>` | run-day counters (walk breaks) and start time |
| `wo_wt` | weights `{exerciseId: {date: "kg"}}` (feeds "Last: 16 kg") |
| `wo_alt`, `wo_ri`, `wo_quick` | per-day `{date: 1}` toggles for backup / run instead / quick option |
| `wo_plan` | user plan edits (e.g. `{date: "Rest"}`) |
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
bash scripts/test.sh                      # all suites (~8 min); or: bash scripts/test.sh test_v26
CHROME=/usr/bin/google-chrome bash scripts/test.sh   # optional: system Chrome instead of bundled Chromium
```
- The tests serve the repo root at `http://localhost:8765/index.html` and use Playwright's fake clock.
  - Use `page.clock.run_for(ms)` to advance timers.
  - `fast_forward` simulates a locked phone and triggers the "finished while locked" prompt.
- `test_sw.py` temporarily rewrites `sw.js` and restores it. Afterwards, check that `head -c 22 sw.js` shows `var V="pc-vNN"`.
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
- Keep it **simple and readable** on an iPhone, using the **warm orange dark theme** (CSS variables in `src/top.html`: `--accent` orange on a dark background). Follow `app-style-standard.md`.
- Make **one commit per change** with a clear `pc-vNN: …` message.
- **Never break saved logs** (see the compatibility rules above).
- Don't add trackers, external scripts or network calls; the app must work offline.

## Weekly sessions
Weekly sessions are added by the Health & Fitness bot directly into the session data; Claude Code should not change session content unless asked, and must keep the session data format stable so weekly additions stay simple.

- How a week is added today (pc-v29, week 2): one `// ==== WEEK N …` block in `src/app.js`, just above `// ---- backups`. It holds new `X` ids with `HT` How-to entries, `HAL` aliases, and `Object.assign(SESS,{…})` with that week's main sessions (`mob19`, `up20`, …) and backups (`bk19`…, `g0:100`). It's followed by date entries in `PROG` / `BK`, plus `Object.assign(RI/RIN/RIS,…)` for Run-instead versions. The weekly plan and rationale go in `docs/programme-weekN.md`; tests go in `tests/test_vNN.py` (copy `test_v29.py` and change `DAYS` / `VIEWS` / `W2P`).
- **Future improvement (not done yet; only on request):** make weekly additions lower-touch with one clear `WEEKS` data section, e.g. `WEEKS["2026-10-19"]={days:{mon:{main:"mob19",backup:"bk19"},…}}`. `PROG`, `BK`, `QK` and the RI tables would be derived from it, and the test `DAYS` / `VIEWS` would be generated from it. Session ids and block ids must stay unchanged so saved logs keep working.
