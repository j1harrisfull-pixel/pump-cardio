# Brief for Grok: how you deliver a week to Pump + Cardio (from pc-v39)

**James's decision, 9 Nov 2026: he does not want to import anything by hand.** You push each week to `main`
yourself, so it appears in the app when he refreshes. A week is one JSON file, `weeks/<monday>.json`. The app
validates it and builds the sessions itself. You do not edit src/app.js or any JavaScript: Claude Code still
owns the app's feature code. If you are asked for "this week's workouts", the pushed week is the deliverable.

## What you produce
One JSON object per week. Follow docs/week-format.md in the repo and copy docs/week-sample.json as your
starting point (it is a complete, valid week). Shape:

{"v":1,"week":"2026-11-09","title":"Week 5 · short title",
 "x":{ new exercises: "id":["Display name","suggested weight text","range",1] },
 "ht":{ How to entries for every new exercise id or new move name },
 "hal":{ optional aliases },
 "sess":{"up1110":{"name":"Strength A5 · Upper","short":"Upper","safe":"…","blocks":[ … ]},
         "bk1110":{"name":"Backup · …","short":"Walk","g0":100,"safe":"…","blocks":[ … ]}},
 "days":{"2026-11-09":{"main":"run1109"},"2026-11-10":{"main":"up1110","backup":"bk1110"}, … all 7 days},
 "ri":{ run instead versions }, "rin":{ their names }, "ris":{ their safety lines }}

## Block specs (data, not code)
- flow: warm up, cool down or mobility. "moves":[["Name – each side",40],["Cat-cow",40]], "phase":"WARM-UP" | "STRETCH" | "MOBILITY".
- tm: one steady piece. "sec", "phase" ("JOG","EASY","STEADY","WALK","COOL-DOWN","WARM-UP"). Put "counter":1 on a run so the walk break counter and the Actual card appear.
- iv: intervals. "n","work","rest" in seconds, "wl" effort word, "rl" rest label. No trailing rest.
- core: round based circuit. "rounds", "moves":[["Name",work s,setup s,sided 0/1]], "rest", plus "list" for the How to links (3 or more moves).
- emom: "rounds", "win" (seconds per window), "cycle": one label per window ("Single-arm press · left","Kettlebell swing ×12"), "list": "Name – ×N[ each side]".
- ex: strength in list mode. "h" ("A · Straight sets","B · Superset"), "mode":"sup", "n" sets or rounds, "rr":[lo,hi] rest seconds, "tid" unique id, "items":[{"x":"db-bench","lab":"A1","rp":6,"tp":"3011"}].
- fields: the run log card ({"k":"fields"}). rest: a rest day card.
Every timer block needs a unique id, h (header type) and name; note is the instruction line.

## Rules the app enforces (get them right first time)
- week is the Monday. Every day of the week has a main (use "rest0" for a rest day).
- Session ids and block ids are new every week (for example up1110, bk1110, s1110a). Never reuse an id from an earlier week.
- Every exercise id and every move name must resolve to a How to entry, either one already in the app or one in your ht.
- Banned: barbell, back squat, conventional deadlift, snatch, handstand or any inversion, Valsalva, breath holding. No RPE 8 or above and no "hard". Effort words only easy (RPE 3 to 4), steady (RPE 5 to 6), moderate (RPE 7); never "brisk" or "jog" (week 5 had both and the validator now rejects them). No paces, splits or speeds. Kettlebell and dumbbell spelled out, "each side" spelled out.
- A run instead block must total exactly the same seconds as the block it replaces.
- Safety line under 160 characters; strength sessions say breathe out on the effort.
- Strength at RPE 6 to 7, two reps in reserve. Keep sessions around 30 to 40 minutes.

## Delivery (James's decision, 9 Nov 2026)
Push the week to `main` yourself; James should never have to paste or import anything. For each week:
1. Write `weeks/<monday>.json` and the rationale in `docs/programme-weekN.md`.
2. Add the week's content checks in `tests/test_vNN.py` (written with `tests/lib.py`) and add the suite to `FULL` in `scripts/test.sh`.
3. Bump the version (`bash scripts/bump.sh NN`), build (`bash scripts/build.sh`) and run the tests.
4. Push to `main`, then check the live `sw.js` shows the new version.
In chat, send James a short plain summary of the week (rationale and progression notes), not the JSON.
History → Weeks → Import week stays in the app as a fallback only.

## What you get back
His exported history. It shows, per day, planned versus actual for each exercise ("planned 4 × 6 → 22 kg ·
6/6/5/–"), which blocks were finished, run substitutions ("did 5K easy run instead of …"), outcomes
(modified, cut short, skipped), a feel average, planned but not logged days, and whether next week is
planned. Progress from what he actually did, not from your previous plan. The app already suggests the
next weight from his last sets (2 kg dumbbells, 4 kg kettlebells, only if it felt RPE 6 to 7); you set reps,
tempo, rest and the session shape.
