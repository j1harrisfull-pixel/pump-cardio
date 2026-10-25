# Workout mode research: what established apps show during a session
*Research only, 25 Oct 2026. App not changed or pushed. Builds on premium-apps-research.md (16 Oct).*
Legend: **V** = verified in a cited source; **I** = inferred (not stated outright).

## 1. App by app

### Strong (logger)
- Workout = one scrolling list of exercises; each set is a row (previous | kg | reps | tick). Tick a set → **2:00 rest timer starts automatically**, shown small top-left; tap for full screen to adjust or Skip. Per-exercise rest, separate warm-up rest. Configurable sound. **V** — help.strongapp.io/article/231-rest-timer
- Logging happens during the session, one tick per set, prescribed values pre-filled. **V/I**
- No EMOM/interval timer for whole blocks. **I** (not in help docs)

### Hevy (logger)
- Same row model: tick set → rest timer auto-starts; **+15 / −15 / Skip**. Live Activity (lock screen) shows rest countdown, current exercise, next set, weight/reps, previous numbers. **V** — help.hevyapp.com "Rest Timer & Default Rest Timer"; hevyapp.com/features/live-activity
- Previous numbers shown inline next to each set. **V** — hevyapp.com/features/track-workouts
- Lock-screen widget is native-only (not possible in a PWA). **V** — webkit.org, caniuse

### TrainHeroic (coach-programmed)
- Coach instructions at top of session; tick each set or tap the cell for keypad; +/− sets; swipe between blocks; session RPE + comments **at the end**. Built-in **rest, AMRAP and EMOM timers** per block. **V** — support.trainheroic.com "Logging your Training Session"; trainheroic.com/athlete
- Block-level timer, not per-rep segmentation. **I**

### Future (coach + Watch)
- Press Play; coach audio and video; **Next button** on phone or Watch to move on; report reps / adjust weight per set; "Repeat Cues". **V** — faq.future.co; WIRED, The Verge reviews
- Watch haptics for rest and next set — not applicable (no vibration rule, and PWA can't). **V**

### Ladder (coach-timed player)
- Player times each movement and rest; coach audio calls movement, pace and rest. **V** — joinladder.com "How it works"
- Workout Player 2.0: **swipe to navigate, add prep time, preview next movement during rest, double-tap replay, skip sections, larger text and controls**. **V** — instagram.com/reel/CyBYJ2lOIBp (Ladder official)
- Pace setting: pause after every set and swipe on, or run automatically. **V** — r/ladderapp
- "Log reps and weight as you go". **V** — joinladder.com
- Lesson: even Ladder added *larger text, fewer controls, next-move preview in rest* after feedback.

### Functional Bodybuilding / Persist (Marcus Filly)
- Program app: daily session list, video demos, **tempo instructions in text**, logging and week-to-week load tracking. No guided per-rep timer found. **V/I** — functional-bodybuilding.com/pages/persist
- Sessions are written as **A / B1-B2 / C** blocks with sets × reps × tempo and rest in text; the athlete follows the prescription. **V** (programme style) / **I** (how the screen lays it out)

### SmartWOD Timer (timer app)
- EMOM: set total time + interval length; **beep every time one interval ends and the next begins**. Integrated **round counter**, big clear display, landscape large numbers. **V** — play.google.com net.smartwod.timer; apps.apple.com id1248966041
- Cues per interval: **start, halfway, 10 s, 3-2-1** (user review, Jan 2026). **V** (review)
- Shows a whole EMOM as **one minute clock + round count**; workout text optional on screen/watch notes. **V** — smartwod.app/faq-watch
- Two colour schemes incl. "max-visibility"; voice countdown "so you know where you are without looking". **V** — smartwod.app/wod-timer
- Reviews: sound drifts or stops when screen off (Android) — same risk class as our PWA. **V**

### Seconds (interval timer)
- Full-screen, **large time readable from across the room**; **current and next interval names shown**; **whole background colour = interval type**, "so you don't even need to read the name". **V** — play.google.com com.runloop.seconds
- Text-to-speech speaks interval names with advance warning; halfway alert option. **V** — intervaltimer.com/help/editors/intervals
- Left/right: option **"Split interval left/right"** with optional **pause between sides** — sides are explicit, labelled halves, not hidden inside a combined label. **V** — same help page
- **Lock button** to stop stray taps pausing. **V** — App Store listing
- "Exclude from count": round counter counts only work intervals, not rests/warm-ups. **V**

### Wodify / SugarWOD / BTWB (box apps)
- Built-in AMRAP/EMOM/interval timers; whiteboard-style result logging **after** the workout (score, rounds, load). **V** — sugarwod.com; btwb.com (see 16 Oct doc)

## 2. Patterns that recur
1. **Two kinds of screen, never mixed.** Loggers (Strong, Hevy, TrainHeroic, Persist) show a set list + a rest timer started by ticking a set. Timers (SmartWOD, Seconds) show one big clock for timed formats. Nobody puts a segmented countdown inside a strength set.
2. **EMOM = one clock per interval + round counter.** Beep at the top of each minute, 3-2-1 before it. Work/rest split inside the minute is **not timed** — rest is what's left. (SmartWOD, Seconds, TrainHeroic.)
3. **Now + Next.** Current move big, next move small (Seconds, Ladder rest preview, Hevy Live Activity).
4. **Glanceable from a distance.** Very large digits, short labels, colour signals the phase (Seconds, SmartWOD max-visibility, Ladder "larger text and controls").
5. **Sound replaces looking.** Beeps/voice at changes, 3-2-1 and optional halfway (all timer apps, Ladder, Future).
6. **Few controls, protected.** Pause, skip/next, back; Seconds adds a lock against stray taps.
7. **Rest timer: auto-start, +15/−15, Skip.** (Strong, Hevy.)
8. **Logging is one tap with prefilled values;** timed-block scores are entered once **at the end** (TrainHeroic RPE, SugarWOD whiteboard).
9. **Sides are explicit:** either "×5 each side" as text, or a split labelled Left / Right interval (Seconds). Never a mid-interval auto switch with a combined label.
10. **Counters count work rounds only** (Seconds "exclude from count").

## 3. What this says about our app (pc-v28/29, read from src/app.js)
- `bEmom()` breaks each EMOM minute into READY (prep) + WORK (sometimes split left/right) + REST segments, each with its own countdown and label like "Press · switch → right side · round 2/4". No app researched does this; it's the cause of the confusion James reported.
- `bSup()` adds READY/WORK timed segments to supersets — the loggers don't time strength work at all.
- Interval blocks (`ivr`) are close to the timer-app model and can stay, simplified.

## 4. Gaps
- Could not view in-app screenshots directly for Future, TrainHeroic or Persist; layout details for those are from help docs/reviews (marked I where inferred).
- iOS PWA: no audio or timers while locked; Screen Wake Lock works in Home Screen apps from iOS 18.4 (see 16 Oct doc).
