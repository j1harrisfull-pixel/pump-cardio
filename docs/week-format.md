# Week file format (pc-v39)

A week is **one JSON object**. The app validates it, builds the sessions with the same builders the code uses, and
shows it in the week strip. Two ways in:

1. **Built in:** save it as `weeks/<monday>.json` in the repo. `scripts/build.sh` inlines every file there, so a
   push to `main` ships it (no JavaScript to edit). `tests/test_v39.py` validates every file.
2. **Imported on the phone:** History → **Import week** → paste → **Check** → **Save week**. Stored in
   localStorage (`wo_weeks`), applied on top of the built-in weeks. Remove it from the same list.

A week never replaces a session id that already exists in the app, so logs keep rendering. Re importing the same
Monday replaces that import.

`docs/week-sample.json` is a complete working example (sessions of every kind, a backup with a run version).

## Top level
| Key | Required | Meaning |
|---|---|---|
| `v` | yes | `1` |
| `week` | yes | the Monday, `YYYY-MM-DD` |
| `title`, `notes` | no | free text (title shows in the Weeks list) |
| `x` | no | new exercises: `id: [display name, suggested weight text, weight range, weighted 0/1]`. Each needs a How-to in `ht` under the same id |
| `ht` | no | How-to entries: `key: {q: demo search, u: one line summary, s: [steps, 12 words or fewer], c: [tips], m: common mistake, z: safety line}`. Key = exercise id, or the move name used in flows and lists |
| `hal` | no | aliases `other name: ht key` |
| `sess` | yes | sessions, see below |
| `days` | yes | `date: {main: id, backup?: id, quick?: id}` for each day of the week. Use `rest0` for a rest day |
| `ri`, `rin`, `ris` | no | Run instead versions: `ri.<sessionId>.<blockId>` = a block spec with the **same total seconds**; `rin.<sessionId>` = `[name, short]`; `ris.<sessionId>` = safety line |

## Session
```json
"up0105":{"name":"Strength · Upper","short":"Upper","safe":"Breathe out on every rep, stop 2 reps short (2 RIR). RPE 6–7.","g0":0,"blocks":[…]}
```
`short` is the week strip label (one word). `safe` is the safety line (160 characters max; strength sessions should
say breathe out). Backups use `"g0":100`. Ids: lower case letters and digits, new every week (`up0105`, `bk0105`).

## Block kinds
Every timer block needs a unique `id`, `h` (the header type) and `name`. `note` is the instruction line and
`small` the small print (string or array). Timer headers: `Warm-up`, `Steady`, `Intervals`, `Circuit × N`,
`EMOM 60 s × N`, `Every 2:00 × N`, `Flow`, `Cool-down`.

| `k` | Builds | Fields |
|---|---|---|
| `flow` | a guided flow (warm-up, cool-down, mobility) | `moves: [[name, seconds], …]` with `– each side` or `– left` / `– right` in the name; `phase`: `WARM-UP`, `STRETCH` (default), `MOBILITY`, `FLOW`; `dir`: `up` (standing last) or `down` |
| `tm` | one steady piece | `sec`, `phase` (`JOG`, `EASY`, `STEADY`, `WALK`, `COOL-DOWN`, `WARM-UP`); add `"counter":1` on a run so the walk break counter and the Actual card appear |
| `iv` | intervals, no trailing rest | `n`, `work`, `rest` (seconds), `wl` effort word for the work label, `rl` rest label |
| `core` | a round based circuit | `rounds`, `moves: [[name, work s, set-up s, sided 0/1], …]`, `rest` between rounds, plus `list` for the How-to links |
| `emom` | EMOM / Every | `rounds`, `win` (seconds per window), `cycle`: one label per window (`Single-arm press · left`, `Kettlebell swing ×12`, `Complex · right`), `list`: `Name – ×N[ each side]` for the How-to links. The app derives the minute groups and the clock from these |
| `timer` | raw segments | `segs: [[PHASE, seconds, label], …]` |
| `ex` | strength (list mode) | `h` (`A · Straight sets`, `B · Superset`, `C · Tri-set`), `mode: "sup"`, `n` sets or rounds, `rr: [lo, hi]` rest seconds, `tid` unique id, `items: [{x: exercise id, lab: "A1", rp: reps, tp: "3011" tempo, side: 1 for each side, ru: "s" or "m" for timed or distance items, cue}]` |
| `fields` | the Actual run card | `dist` label, e.g. `"Distance (m, from PM5)"` for a rower day |
| `rest` | rest day card | `name`, `note` |

## Rules the validator enforces
- Monday week, every day inside it, every referenced session exists, no reused session id, unique block ids.
- Every exercise id and every move name resolves to a How-to.
- No barbell, back squat, conventional deadlift, snatch, inversions, Valsalva. No RPE 8+ and no "hard".
- Effort words only `easy` (RPE 3–4), `steady` (RPE 5–6), `moderate` (RPE 7); no paces or splits.
- Run instead blocks keep the same total time as the block they replace.
Warnings (not blocking): steps over 12 words, timed blocks without an effort word, EMOM without a list.
