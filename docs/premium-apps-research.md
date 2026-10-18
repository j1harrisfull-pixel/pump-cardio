# Premium training apps: guided-workout research + Pump+Cardio timer audit
*Research only, 16 Oct 2026. The app was not changed, committed or pushed.*

## 1. What the premium apps do (sourced)

| App | What's documented | Source |
|---|---|---|
| **Hevy** | The rest timer **starts automatically when you mark a set complete**. You set it per exercise or as a global default. **+15 / −15 / Skip** controls. A **Live Activity** on the iOS Lock Screen and Dynamic Island shows the rest countdown, current exercise, the next set, prescribed weight and reps, and last session's numbers. You can **mark a set complete from the lock screen**. You log weight, reps, RPE or duration per set; supersets and notes are supported. | help.hevyapp.com "Rest Timer & Default Rest Timer"; hevyapp.com/features/live-activity; help.hevyapp.com "How to Use Hevy's Live Activity"; hevyapp.com/features/track-workouts |
| **Strong** | Default **2:00 rest timer triggers immediately after a set is completed**. It shows in the top-left during the workout. Tap it for **full screen**, where you can change the duration or **Skip**. Duration can be set per exercise, with separate values for warm-up and working sets. Timer sound is configurable. | help.strongapp.io/article/231-rest-timer |
| StrongLifts (for comparison) | A Live Activity on the Lock Screen and Dynamic Island shows rest time and the next set. | support.stronglifts.com/article/126-live-activities |
| **Future** | Coach-built plan. You press **Play** and hear the coach's voice, with video demos and cues. In-workout tools: **Flag** (swap an exercise), **Report Your Reps**, **Adjust Your Weight**, **Repeat Cues**, **Record My Form**, **Exercise History**. Moving on is a **Next button on the phone or Apple Watch**; the Watch auto-counts reps for some moves and **vibrates for rest and next set**. App Store reviews mention Watch "next" taps sometimes failing. | faq.future.co "What should I expect from a Future Pro workout?"; Good Housekeeping review; WIRED review; The Verge; App Store reviews |
| **Ladder** | Timed, coach-voiced sessions with looping demos. Users report **rest starting automatically**. **Pace Settings** let you pause after every set and **swipe to progress**, or let it run automatically. You can **add seconds before each new movement** to set up; **swipe left to skip and right to go back**; pause is available. *Auto-Check* (Feb 2026) ticks movements in the journal automatically when the timer ends. | r/ladderapp threads; Ladder release notes, Feb 2026 (r/ladderapp) |
| **TrainHeroic** | **Start Session** starts a session timer and a readiness survey. **Coach Instructions** sit at the top. You tick each set or tap the table to enter results with a keypad; **+/− buttons add or remove sets**. A 3-dot menu has history, swap, % calculator and exercise tips. You swipe between blocks. At the end you set a session RPE slider and leave comments. **Built-in rest, AMRAP and EMOM timers.** Sessions can be edited afterwards. | support.trainheroic.com "Logging your Training Session" and "edit my logged session"; trainheroic.com/athlete |
| **Functional Bodybuilding / Persist (Marcus Filly)** | The program app provides logging, video demos, **tempo instructions**, a calendar and week-to-week tracking of logged loads. The sources do not confirm a built-in tempo or rep timer. | functional-bodybuilding.com/pages/persist and the getting-started pages |
| **Mayhem (Streamline / Athlete)** | Runs on the btwb platform: a **built-in workout timer on phone and Apple Watch**, round and movement **split tracking**, and coach notes vs athlete notes. | Mayhem affiliate FAQ PDF; btwb.com |
| **PRVN** | **In-app timers and interval trackers**, digital training journal, calculators, daily programming, coach access. | App Store "PRVN Fitness" |
| **SugarWOD / BTWB** | Built-in **AMRAP, EMOM and interval timers**; whiteboard-style logging of results and PRs. BTWB adds deeper analytics and automatic PRs. | sugarwod.com; App Store SugarWOD; btwb.blog; beyondthewhiteboard.com |
| **Apple Fitness+** | On-screen live **time (remaining or elapsed, user's choice)**, heart rate, calories and interval timers. The Burn Bar compares your effort with others. | support.apple.com/108761; Standard review |
| **Peloton** | The strength timeline shows **time left per movement and upcoming movements**. That source reported this on Peloton Guide only. | connectthewatts.com (secondary source only) |
| **Nike Training Club** | Pause, skip and advance between moves, including from Apple Watch. A persistent "next" preview was not confirmed. | App Store "Nike Training Club" |
| **Runna** | Audio cues, Apple Watch app, workout mirroring (**pause, resume and end from either device**). **Double-tap to end a lap or skip a section.** Automatic interval progression unless track or open warm-up modes are on. | support.runna.com (audio cues, Apple Watch, mirroring) |
| **Concept2 PM5 / ErgData** | Interval workouts are defined as work plus **rest time**. The PM5 **shows the rest countdown** (top left) and starts the next interval automatically. *Undefined rest* waits for you to start. ErgData lets you choose the data boxes. | concept2.com/support/ergdata; Concept2 PM5 how-to; r/Rowing; ErgZone FAQ |

**Patterns across the apps**
1. **Rest starts automatically when a set is logged** (Hevy, Strong, Ladder), with **+15/−15 and Skip**.
2. **Lock-screen presence:** native apps use Live Activities or Dynamic Island (Hevy, StrongLifts) or the Watch with haptics (Future, Runna). Web apps cannot do this. Their closest option is Web Push on iOS 16.4+ for a Home Screen web app, which needs a push server.
3. **Now and Next:** the current set, reps and weight, plus the next set, all on one card or widget (Hevy Live Activity, Peloton timeline, PM5).
4. **Transitions:** user-set prep time before each movement (Ladder's "add seconds"), or manual swipe to progress.
5. **Coach notes:** a session-level note at the top (TrainHeroic Coach Instructions, Future's audio intro), and cues per exercise you can tap to replay (Future "Repeat Cues").
6. **Logging speed:** one tap ticks a set with the prescribed values pre-filled; tap a cell for a keypad (TrainHeroic, Hevy). Previous numbers are shown inline (Hevy).
7. **Adaptation:** coach-led (Future, TrainHeroic) or history-led (Hevy previous values, TrainHeroic predicted 1RM, Persist week-to-week loads).
8. **Visuals:** dark mode, one big countdown, a compact list. Apple Fitness+ lets you choose remaining vs elapsed time.

**iOS web-app limits (relevant to us):** a Home Screen web app cannot run JS timers or play audio while locked or in the background; JS is suspended (progressivewebapps.com; Stack Overflow; prototyp.digital). Web Push to Home Screen web apps works on iOS 16.4+ (webkit.org/blog/13878). The Screen Wake Lock bug in Home Screen web apps was fixed in iOS 18.4 (WebKit bug 254545; Safari 18.4 notes). Safari on iOS has **no `navigator.vibrate`** (caniuse), so it is a no-op on iPhone.

## 2. Timer audit of our app (pc-v24, read-only)

### Engine
- **Timestamp-based, no drift.** `tstate()` works out the current segment from `Date.now() - T.t0`. `setInterval(loop,250)` only redraws. Because nothing counts ticks, missed ticks cannot pile up into error. Worst-case display lag is about 250 ms. ✅
- The timer **survives a reload or app relaunch**: `wo_timer` is saved to localStorage with `t0`. ✅
- Uses wall-clock `Date.now()`. A system clock change mid-session would shift it. This is rare, and the alternative (`performance.now`) does not survive a reload. Low risk.
- The countdown uses `ceil` with a minimum of 1, so "1" shows until the boundary. The 3-2-1 beeps fire on the last three seconds. ✅

### Lock / background behaviour (from the code plus the iOS limits above)
1. **While locked or backgrounded nothing fires.** JS is suspended, so there are no beeps and no segment-change cues. On return the bar jumps to the correct segment silently, and the transitions he missed are never announced.
2. **If the whole timer runs out while he is locked, `doneT()` marks the block done on return**, even if it wasn't done. It plays one DONE beep.
3. **Audio may stay suspended after returning.** `unlock()` only runs on pointerdown or touchend, so the first beeps after unlocking can be silent until he taps.
4. **`navigator.vibrate(200)` does nothing on iPhone** (not supported), so there are no haptics.
5. **Wake Lock** keeps the screen on only on iOS 18.4+ in a Home Screen app. Wake Lock is released when the page is hidden; `visibilitychange` asks for it again on return. ✅ It is taken only while a timer runs.
6. **Controls:** only **Stop**. There is **no pause, skip/next, back, or ±15 s**. Stopping loses the position, so restarting begins the block from zero.

### Prescription vs timer mismatches (every one found)
**A. "Each side" moves timed as one segment with no switch cue (no half-time beep).**

Guided flows:
- **Mon:** Ankle rocks (40 s, warm-up); Thoracic open book (60 s, mobility finisher)
- **Tue:** Thoracic open book (40 s, warm-up and cool-down); Seated lat reach (40 s, cool-down)
- **Wed:** Half-kneeling hip flexor (40 s); Thoracic open book (40 s), both in the cool-down
- **Thu:** Couch stretch (active), each side (75 s)
- **Fri:** Half-kneeling hip flexor (40 s); Thoracic open book (40 s)
- **Sat:** Half-kneeling hip flexor (40 s); Thoracic open book (40 s)
- **Sun:** Ankle rocks (40 s); 90/90 (50 s); Thoracic open book (50 s)
- **Backups:** the same pattern in bk12–bk18. The bk18 stretch flow has five 90 s "each side" holds.

Optional rest fillers: Tue and Fri superset rests ("20 s hip flexor reach / couch stretch each side" inside a 75 s rest).

**B. Unilateral sets: one WORK segment covers both sides, with no "switch sides" cue.**
| Day | Move | Prescribed | WORK segment | Tempo time |
|---|---|---|---|---|
| Tue | B2 half-kneeling press | 6/side @2010 | 45 s | 36 s |
| Fri | B1 reverse lunge | 6/side @2011 | 55 s | 48 s |
| Fri | B2 dead bug | 5/side @2020 | 45 s | 40 s |
| Fri | C2 side plank | 20 s/side | 50 s | 40 s |
| Fri | C3 calf raise | 8/side @2010 | 55 s | 48 s |
| Sat | A1 single-arm KB row | 5/side @2011 | 45 s | 40 s |
| bk13 | A1 KB floor press | 5/side @3010 | 45 s | 40 s |
| bk13 | B1 KB row | 8/side | 70 s | 64 s |
| bk13 | B2 halo | 5/side | 45 s | 40 s |
| bk16 | A1 split squat | 5/side | 45 s | 40 s |
| bk16 | B1 single-leg RDL | 6/side | 65 s | 60 s |
| bk16 | B2 side plank | 20 s/side | 50 s | 40 s |
| bk16 | C2 calf raise | 10/side | 65 s | 60 s |

WORK time is worked out as reps × tempo sum + 5 s, rounded up to the next 5 s. So every set gets 5–10 s of padding beyond the tempo. That is fine as buffer, but the timer doesn't match the reps.

**C. "Every 2:00 × 4" blocks are shorter than 8:00.** The last round has no rest. Tue 7:30, Fri 7:35, Sat 7:40, bk13/bk16/bk17 7:45. The section header shows the real time; the block name implies 8:00.

**D. "Every 75 s" stations (Sat B, bk17 B).** WORK is 60 s (55 s for the farmer's carry) and covers both the set and the rest. There is no cue for when the set ends and rest begins. The prescription is reps or metres, not time:
- Sat B: swings 10 reps, sumo deadlift 8, suitcase carry 30 m, farmer's carry 30 m
- bk17 B: squat-press 8 reps, pull-up/dip 6, farmer's carry 30 m

**E. Distance prescribed, timed as a fixed window.** Carries of 30 m sit inside a fixed 55–60 s window, so distance is not tracked.

**F. Interval blocks end with a rest.** Wed 6 × 1:00 ends with a 55 s paddle. Mon and the backups' run/walk and walk intervals end with a recovery walk. This matches the "12:00" and "8:00" totals shown, so it is consistent, but the final rest isn't needed.

**G. Rest is not tied to logging.** Ticking a rep pill does not start a rest timer. Rest exists only inside the guided block timer.

**No mismatch found:** run-instead versions match their originals second for second (test-enforced). Every guided move has a 10 s GET READY. Strength READY segments are 10/15/20 s. Wed intervals give 5 s ready + 1:00 work + 55 s paddle, which is the stated "1:00 rest".

## 3. Ranked improvements for our app
| # | Improvement | Effort | Fixes |
|---|---|---|---|
| 1 | **Pause / Resume, Skip ▶, Back ◀ and ±15 s** on the timer bar. Store `pausedAt` and shift `t0`; keep it timestamp-based. | M | Audit 6. Matches Hevy, Strong, Ladder, Runna. |
| 2 | **Side-switch cues:** split "each side" and "/side" segments into L and R halves (or add a mid-segment "Switch sides" beep and label) without changing totals. | S | Audit A and B, the most common mismatch. |
| 3 | **Don't auto-complete blocks after a lock.** If the timer ended while hidden, show "Timer finished while locked: mark done?" instead of silently ticking it. On return, show a short "you missed: X → Y" note. | S | Lock 1 and 2. |
| 4 | **Resume audio on visibility return** (call `ac.resume()` in `visibilitychange`) and show a "tap to enable sound" hint if it stays suspended. Remove the vibrate dependency on iOS. | S | Lock 3 and 4. |
| 5 | **Work/rest split in "Every 75 s" stations:** WORK = estimated set time, then a REST cue for the rest of the window. Show reps/metres as the target, not a time. | S | Audit D and E. |
| 6 | **Optional auto-rest after ticking a set** (per-block rest, ±15, skip), like Hevy and Strong, for when he isn't using the guided timer. | M | Audit G. |
| 7 | **Now / Next card:** a bigger "Now" with reps, tempo and kg, plus "Next" with its first cue. Tap to see the How-to without stopping the timer. | S | Clearer transitions, like Hevy's Live Activity and the Peloton timeline. |
| 8 | **Prep-time preference:** let him set GET READY to 10, 15 or 20 s (like Ladder's "add seconds"), keeping totals honest. | S | Transitions. |
| 9 | **"Every 2:00" naming:** label it "Every 2:00 × 4 (last round no rest)" or add the final rest so it's a true 8:00. | S | Audit C. |
| 10 | **Lock-screen alerts via Web Push** (iOS 16.4+, Home Screen app). The server schedules a push at each segment end. Needs a push backend; only the end-of-rest and end-of-block alerts are worth sending. | L | The lock-screen gap compared with native Live Activities. |
| 11 | **Drop the trailing rest** in interval blocks, or label it as cool-down. | S | Audit F. |
| 12 | **Progress view per exercise:** last 3 sessions' kg and reps inline (we already show "Last"), plus a simple trend. | M | Adaptation, like Hevy previous values and Persist loads. |

## Gaps in this research
- **Not confirmed from sources:** Persist's in-app timers, Nike Training Club's next-exercise preview, and Peloton's non-Guide timeline.
- **Detail is thin for:** Mayhem/Streamline and PRVN (FAQ and store pages only).
- **Lock-screen findings for our app:** these come from the code plus documented iOS limits. I did not test them on a real iPhone.

## Appendix: full mismatch list (generated from the live session data, 64 rows)
```
easyrun12 | Active warm-up | 'Ankle rocks – each side' 40 s is one segment – no side-switch cue at half-time
easyrun12 | Mobility finisher | 'Thoracic open book – each side' 60 s is one segment – no side-switch cue at half-time
strA | Active warm-up | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
strA | A · Every 2:00 × 4 | Every 2:00 × 4: timer 7:30 (last round has no rest) vs nominal 8:00
strA | B · Superset × 3 | 'Rest · optional 20 s hip flexor reach each side' 75 s is one segment – no side-switch cue at half-time
strA | B · Superset × 3 | 'Rest · optional 20 s hip flexor reach each side' 75 s is one segment – no side-switch cue at half-time
strA | B · Superset × 3 | B2 hk-db-press 6/side @2010: WORK 45 s for both sides (tempo time 36 s, +9 s) – no 'switch sides' cue
strA | Active cool-down | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
strA | Active cool-down | 'Seated lat reach at bench – each side' 40 s is one segment – no side-switch cue at half-time
row | Active cool-down | 'Half-kneeling hip flexor with reach – each side' 40 s is one segment – no side-switch cue at half-time
row | Active cool-down | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
mob | Guided flow | 'Couch stretch (active) – each side' 75 s is one segment – no side-switch cue at half-time
strB | A · Every 2:00 × 4 | Every 2:00 × 4: timer 7:35 (last round has no rest) vs nominal 8:00
strB | B · Superset × 3 | 'Rest · optional 20 s couch stretch each side' 75 s is one segment – no side-switch cue at half-time
strB | B · Superset × 3 | 'Rest · optional 20 s couch stretch each side' 75 s is one segment – no side-switch cue at half-time
strB | B · Superset × 3 | B1 reverse-lunge 6/side @2011: WORK 55 s for both sides (tempo time 48 s, +7 s) – no 'switch sides' cue
strB | B · Superset × 3 | B2 dead-bug 5/side @2020: WORK 45 s for both sides (tempo time 40 s, +5 s) – no 'switch sides' cue
strB | C · Pump tri-set × 2 | C2 side-plank 20/side @None: WORK 50 s for both sides (tempo time 40 s, +10 s) – no 'switch sides' cue
strB | C · Pump tri-set × 2 | C3 calf-raise 8/side @2010: WORK 55 s for both sides (tempo time 48 s, +7 s) – no 'switch sides' cue
strB | Active cool-down | 'Half-kneeling hip flexor with reach – each side' 40 s is one segment – no side-switch cue at half-time
strB | Active cool-down | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
kb | A · Every 2:00 × 4 | Every 2:00 × 4: timer 7:40 (last round has no rest) vs nominal 8:00
kb | A · Every 2:00 × 4 | A1 kb-sa-row 5/side @2011: WORK 45 s for both sides (tempo time 40 s, +5 s) – no 'switch sides' cue
kb | B · Every 75 s × 4 stations × 3 | B1 kb-swing 10 reps: WORK 60 s = work + rest combined, no rest cue/split
kb | B · Every 75 s × 4 stations × 3 | B2 kb-sumo-dl 8 reps: WORK 60 s = work + rest combined, no rest cue/split
kb | B · Every 75 s × 4 stations × 3 | B3 suitcase-carry 30 m: WORK 60 s = work + rest combined, no rest cue/split
kb | B · Every 75 s × 4 stations × 3 | B4 farmers-carry 30 m: WORK 55 s = work + rest combined, no rest cue/split
kb | Active cool-down | 'Half-kneeling hip flexor with reach – each side' 40 s is one segment – no side-switch cue at half-time
kb | Active cool-down | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
walk | Active warm-up | 'Ankle rocks – each side' 40 s is one segment – no side-switch cue at half-time
walk | Stretch | '90/90 hold with lift-offs – each side' 50 s is one segment – no side-switch cue at half-time
walk | Stretch | 'Thoracic open book – each side' 50 s is one segment – no side-switch cue at half-time
bk12 | Mobility | 'Thoracic open book – each side' 50 s is one segment – no side-switch cue at half-time
bk13 | Active warm-up | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
bk13 | A · Every 2:00 × 4 | Every 2:00 × 4: timer 7:45 (last round has no rest) vs nominal 8:00
bk13 | A · Every 2:00 × 4 | A1 kb-floor-press 5/side @3010: WORK 45 s for both sides (tempo time 40 s, +5 s) – no 'switch sides' cue
bk13 | B · Superset × 3 | B1 kb-sa-row 8/side @2011: WORK 70 s for both sides (tempo time 64 s, +6 s) – no 'switch sides' cue
bk13 | B · Superset × 3 | B2 kb-halo 5/side @2020: WORK 45 s for both sides (tempo time 40 s, +5 s) – no 'switch sides' cue
bk13 | Active cool-down | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
bk13 | Active cool-down | 'Seated lat reach at bench – each side' 40 s is one segment – no side-switch cue at half-time
bk14 | Active warm-up | 'Ankle rocks – each side' 40 s is one segment – no side-switch cue at half-time
bk14 | Active cool-down | 'Half-kneeling hip flexor with reach – each side' 40 s is one segment – no side-switch cue at half-time
bk14 | Active cool-down | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
bk15 | Breathe + stretch | 'Calf stretch on block – each side' 50 s is one segment – no side-switch cue at half-time
bk15 | Breathe + stretch | 'Seated lat reach at bench – each side' 50 s is one segment – no side-switch cue at half-time
bk15 | Breathe + stretch | '90/90 hold with lift-offs – each side' 50 s is one segment – no side-switch cue at half-time
bk16 | A · Every 2:00 × 4 | Every 2:00 × 4: timer 7:45 (last round has no rest) vs nominal 8:00
bk16 | A · Every 2:00 × 4 | A1 split-squat 5/side @3010: WORK 45 s for both sides (tempo time 40 s, +5 s) – no 'switch sides' cue
bk16 | B · Superset × 3 | B1 single-leg-rdl 6/side @3011: WORK 65 s for both sides (tempo time 60 s, +5 s) – no 'switch sides' cue
bk16 | B · Superset × 3 | B2 side-plank 20/side @None: WORK 50 s for both sides (tempo time 40 s, +10 s) – no 'switch sides' cue
bk16 | C · Pair × 2 | C2 calf-raise 10/side @2010: WORK 65 s for both sides (tempo time 60 s, +5 s) – no 'switch sides' cue
bk16 | Active cool-down | 'Half-kneeling hip flexor with reach – each side' 40 s is one segment – no side-switch cue at half-time
bk16 | Active cool-down | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
bk17 | A · Every 2:00 × 4 | Every 2:00 × 4: timer 7:45 (last round has no rest) vs nominal 8:00
bk17 | B · Every 75 s × 3 stations × 3 | B1 db-squat-press 8 reps: WORK 60 s = work + rest combined, no rest cue/split
bk17 | B · Every 75 s × 3 stations × 3 | B2 pullup-dip 6 reps: WORK 60 s = work + rest combined, no rest cue/split
bk17 | B · Every 75 s × 3 stations × 3 | B3 farmers-carry 30 m: WORK 55 s = work + rest combined, no rest cue/split
bk17 | Active cool-down | 'Half-kneeling hip flexor with reach – each side' 40 s is one segment – no side-switch cue at half-time
bk17 | Active cool-down | 'Thoracic open book – each side' 40 s is one segment – no side-switch cue at half-time
bk18 | Stretch flow | 'Doorway/rack chest stretch – each side' 90 s is one segment – no side-switch cue at half-time
bk18 | Stretch flow | 'Seated lat reach at bench – each side' 90 s is one segment – no side-switch cue at half-time
bk18 | Stretch flow | 'Calf stretch on block – each side' 90 s is one segment – no side-switch cue at half-time
bk18 | Stretch flow | '90/90 hold with lift-offs – each side' 90 s is one segment – no side-switch cue at half-time
bk18 | Stretch flow | 'Thoracic open book – each side' 90 s is one segment – no side-switch cue at half-time
```
