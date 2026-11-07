# Handover for the Health & Fitness bot (Grokbot) · pc-v37 · 7 Nov 2026

What James's Pump + Cardio app now records, how it reaches you, and what to write back. Read this with
`CLAUDE.md` (data format) when you add a week.

## 1. What changed in pc-v35 to pc-v37

**Running is logged as what actually happened, never as the plan.**
- Run days show an *Actual* card: distance (km, decimals), elapsed time (mm:ss), effort word
  (easy / steady / moderate), feel 1 to 10, notes. Nothing is prefilled from the prescription.
- **Did a different run** (pc-v37): if James replaces the prescribed run (for example your Zone 2 12 min
  becomes a 5K easy run) he taps *Did a different run* and types what he ran. The log then carries
  `sub` (what he ran) and `plan` (the prescribed piece, for example "Easy run 5 km 31:00"). This is a
  substitution, not an extra session.
- **Add a run** (pc-v35): a run on top of another session (strength day plus a run) is a separate
  `type:"extra"` entry named "Extra run" on the same date.

**Every session gets an outcome** (pc-v37): *as planned / modified / cut short / skipped*, saved as `oc`.
Strength days also have a notes box ("anything Grokbot should know"), saved as `notes` when the log has
none. A skipped day is still logged (0 sets, `oc:"skipped"`), so you can tell "skipped" from "forgot".

**EMOMs** (pc-v35): the card and the clock both show one group per minute of the cycle, derived from the
labels you write (see section 4).

## 2. How the data reaches you

James taps **History → Export history** and shares the text. It has three parts:

1. **SUMMARY** (new in pc-v37), the part to read first:
   - `Last weights and reps:` the most recent logged kg and reps per exercise, with the date.
     Reps show per set, "–" for a set not done, and "8@20/8@22 (kg)" when the weight changed mid block.
   - `Runs by week:` `w/c <Monday>: n runs · km · min` (prescribed runs, substitutes and extra runs all
     count; `min` is the elapsed time he typed).
   - `Swapped days:` which calendar day showed which day's session (he can swap two days in a week).
   - `Different runs:` `<date>: <what he ran> instead of <plan>`.
   - `Outcomes:` dates grouped under modified / cut short / skipped (as planned is not listed).
   - `Planned but not logged:` programmed past days with no log at all. Treat these as unknown, not skipped.
2. One line per logged day, newest first:
   `2026-11-02 · Easy 5 km Run (main) · 28 min · 5 km · 28:30 · easy · did 5K easy run instead of Easy run 5 km 31:00 · felt 7/10`
   Type in brackets is main / backup / run (run instead) / quick / extra.
3. `--- JSON (wo_log) ---` the raw log array if you want to parse it.

Nothing leaves the phone unless he shares it.

## 3. Log entry fields (JSON part)

| Field | Meaning |
|---|---|
| `date`, `name`, `sid`, `type` | calendar date, session name, session id, main / backup / run / quick / extra |
| `min` | session minutes (a run with no other timing uses the elapsed time) |
| `sets`, `of` | sets ticked / sets prescribed (strength) |
| `wt` | `{exerciseId: "kg"}` weight used per exercise |
| `rp` | `{exerciseId: {v: [reps per set], u: "" or "s"/"m", k?: [kg per set]}}` |
| `sc` | AMRAP scores `{blockId: {r: rounds, kg, e}}` |
| `km`, `time`, `effort`, `feel`, `notes`, `breaks` | actual run values, feel 1 to 10, walk breaks |
| `sub`, `plan` | pc-v37: what he ran instead, and the prescribed piece it replaced |
| `oc` | pc-v37: planned / modified / cut short / skipped |
| `extra` | 1 on an added run (`type:"extra"`) |
| `ri` | 1 when the Run instead version was used |

All new fields are optional. Older entries simply lack them.

## 4. What to write back (so the app shows it well)

- Keep the weekly format in `CLAUDE.md` (one `// ==== WEEK N` block, `PROG` / `BK` dates, `docs/programme-weekN.md`).
- Progress from `Last weights and reps`, not from the plan. If a block shows `–` sets or `cut short`,
  hold the load; if all sets hit the top of the rep range at RPE 6 to 7, nudge the weight.
- A `Different runs` pattern (he keeps choosing a 5K easy run over a short Zone 2 piece) is a signal to
  prescribe what he actually does, within the effort bands.
- `skipped` with a note usually explains itself; `Planned but not logged` does not, ask James.
- EMOMs: `h:"EMOM 60 s × N"`, labels `Complex · left` / `Complex · right` / `<move> ×N [+ <move> ×N]`,
  `list` entries `Name – ×N[ each side]`. The app derives the minute groups and the clock from these.
- Hard rules still apply: RPE 6 to 7 strength (2 RIR), no hard (RPE 8+) conditioning, no breath holding,
  no head-down positions, no heavy spinal loading, stop-signs line in every session. Effort words are
  single words with their band (easy RPE 3–4 · steady RPE 5–6 · moderate RPE 7). Distances in km and m,
  no paces.

## 5. Not done, on purpose

Dark mode, a "repeat last week" fallback when no week is loaded, and automatic upload of the export.
Everything stays on the phone until James shares it.
