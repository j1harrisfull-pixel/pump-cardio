# Bug: "I couldn't save sessions" (James, 18 and 23 Nov 2026) – brief for Claude Code

Status: investigated on live pc-v72 by Health & Fitness on Mon 23 Nov 2026. App code, not week data.
Do not change any training content (weeks/*.json, programme docs).

## What James saw
- Wed 18 Nov: "Trying to save a run today and it won't let me save it."
- Mon 23 Nov: "I couldn't save sessions!" His export has nothing after Mon 16 Nov except one `Extra run` on 18 Nov:
  `{"date":"2026-11-18","name":"Extra run","type":"extra","act":"run","km":"11.90","time":"1:11","effort":"steady","feel":"6","notes":"A","min":1}`.
  He ran 11.9 km in 1 h 11 min. The app stored 1 min 11 s.

## What was ruled out
Playwright, 390x844 touch, tabs layout (no `wo_flat`), live URL, clock set to each day, localStorage seeded with his real
`wo_log` and `wo_daymap`, Chromium and WebKit. Every path saved a correct `wo_log` entry, no page errors:
- Week 6 (16–22 Nov) and week 7 (23–29 Nov): main session (strength with supersets/tri-sets/finisher, ticking every set),
  run session (Log my run, and Start session with every guided timer run to the end), EMOM + run, walk, backup session,
  "Doing something else" → different run / something else, and + Add an activity on a rest day and a training day.
- Mon 23 Nov (today) Density Dash: 20/20 sets saved; Tue–Sun of week 7 also save.
So the week files are fine. No hard "Finish does nothing" was reproduced. The confirmed defects below are what makes a
save fail silently or look as if it failed.

## Confirmed defects

### 1. A failed write still says "Workout saved" (silent data loss)
`LS.set` (src/app.js, `var LS=…`) swallows every exception. If `localStorage.setItem` throws (iOS storage full, storage
blocked, private mode, eviction), Finish still shows the **Workout saved** card and nothing is stored.
Repro: open Tue 24 Nov → Log my run → 5.1 km, 31:20 → stub `Storage.prototype.setItem` to throw `QuotaExceededError` for
`wo_log` → Finish workout. Result: "WORKOUT SAVED" card, `wo_log` has no 24 Nov entry.
Fix:
- `LS.set` returns `true`/`false` (catch → `false`), and a new `LS.ok(k,v)` writes, reads back and compares.
- Finish, Save activity (`saveExtra`), Edit run and Save (`fin2`) use it; on failure do not show "Workout saved". Show a
  persistent toast "Couldn't save on this phone. Export history now and tell Health & Fitness." and keep the form filled.
- On load, write/read/delete a probe key; if it fails, show a banner on Today.
- Settings → About: "Saved on this phone: N sessions · last saved <date>" so James can see a save landed.

### 2. "Save activity" (+ Add an activity / rest day) gives no confirmation
`#runsave` calls `saveExtra`, then only re-renders the same form with the same button and a 0.9 s flash. It looks as if
nothing happened (this matches 18 Nov: the entry exists, but he thought it wouldn't save).
Fix: after a successful save, collapse the card to a summary line ("✓ Run saved · 11.9 km · 1:11:00 · Edit") and toast
"Run saved". Same for the quick-form `#fin2` Save on an off-plan day if it does not already show the saved card.
Also: on a rest day Today says "Nothing to log today" with only "Open today". Add a "Log an activity" link there.

### 3. Elapsed time over an hour is read as minutes:seconds
`tnorm`/`tmin` treat any `a:bb` as mm:ss. "1:11" → 1 min. The iPhone decimal pad has no colon, so `1.11.00` is not
understood either (`tnorm("1.11.00")` returns it unchanged, `tmin` = 0).
Fix:
- Accept `h.mm.ss` and `h:mm:ss` with dots (`1.11.00` → `1:11:00`).
- When a distance is present and `a:bb` as mm:ss is faster than 2:30 per km (impossible), read it as h:mm
  (`1:11` with 11.9 km → `1:11:00`, 71 min). Without a distance, keep mm:ss.
- Show the parsed reading under the field as he types: "= 1 h 11 min" / "= 29 min 40 s".
- Placeholder: "29:40 · 29.40 · 1.11.00".
- One-off migration (bump `wo_ver`): the 2026-11-18 `type:"extra"` entry with km 11.90 and time "1:11" becomes
  time "1:11:00", min 71. General rule for old entries: any run with km ≥ 3 whose mm:ss pace is under 2:30/km is re-read as h:mm.

## Acceptance tests (new suite, add to FULL and FAST)
1. Stub `setItem` to throw for `wo_log`: Finish on a run day and on a strength day shows the "Couldn't save" toast, no
   "Workout saved" card, fields still filled; un-stub and Finish again saves.
2. Rest day → + Add an activity → Run 11.9 km, time `1.11.00` → Save activity: toast "Run saved", card collapses to a
   summary, `wo_log` entry has time `1:11:00` and min 71.
3. `tnorm`/`tmin`: `1:11`+11.9 km → 71 min; `1:11` with no km → 1 min 11 s (min 1); `29:40`, `29.40`, `2940` unchanged
   (29:40); `71.00` → 71 min; `1:11:00` → 71 min.
4. Migration turns the 18 Nov entry into 1:11:00 / 71 min and leaves other entries untouched; export summary shows
   "w/c 2026-11-16: 1 run · 11.9 km · 71 min".
5. Regression: Finish on Mon 23 Nov (Density Dash, all sets ticked) and Tue 24 (Lamp-Post Pickups, Log my run) still save
   and show "Workout saved". Probe-key banner does not show when storage works.
6. Existing suites stay green (test_v63 "label chip and name on one line" already failed before this work).

## Not yet known
Whether James's phone actually hit a storage failure or he was saving in a Safari tab rather than the Home Screen app
(iOS keeps separate storage for each). Defect 1's About line and banner will tell us next time.
