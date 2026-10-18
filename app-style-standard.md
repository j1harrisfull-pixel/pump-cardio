# Pump + Cardio: session layout standard (draft for James's approval)
*Written 17 Oct 2026 (pc-v27); approved by James 18 Oct 2026 with the effort bands in section 6. Applied in pc-v28 with the BRIEF.md timer rework (strength headers show `N rounds`, rest as "Rest 60–90 s"); tests/test_v28.py re-runs the audit below and reports 0 deviations.*
*Based on the patterns in premium-apps-research.md: TrainHeroic coach line at the top; Hevy/Strong one-line set rows with a rest timer that starts on tick; Ladder/Peloton "Now / Next" with moves and reps; Apple Fitness+ one big countdown; PM5 work/rest intervals; Functional Bodybuilding tempo chips.*

## 1. Block header: `N · [Letter ·] Format · Time`
- **N** = block number. **Letter** (A, B, C) only for blocks that number their moves (A1, A2 …).
- **Time** = the exact guided-timer length (m:ss). Self-paced strength blocks show `≈m:ss`.
- **Format** must be one of these:

| Format | Use for | Timer |
|---|---|---|
| `Warm-up` | first block(s): mobility flow or easy walk/row | guided |
| `Straight sets × N` | one move, rest between sets | rest timer |
| `Superset × N` | 2 moves back to back, then rest | rest timer |
| `Tri-set × N` | 3 moves back to back, then rest | rest timer |
| `Every 2:00 × N` | new round on the clock | guided |
| `EMOM 75 s × N` | one station per 75 s window (N = rounds) | guided |
| `Intervals` | work/rest on one machine or run/walk | guided |
| `Circuit × N` | timed stations (core, carries) with set rest | guided |
| `Steady` | one continuous effort (run, walk, row) | guided |
| `Flow` | timed mobility/stretch sequence in the main part | guided |
| `Cool-down` | last block(s): stretch flow or easy walk | guided |

Purpose words ("Active", "Main", "Conditioning finisher", "Pump", "Pair", "stations") don't go in the header. The card title says what it is (e.g. "Row intervals", "Easy run (Zone 2)").

## 2. One fixed instruction line per format (≤60 characters, first line under the title)
| Format | Line template | Example |
|---|---|---|
| Superset / Tri-set / Straight sets | `Each round: B1 → B2 · rest N s.` | Each round: B1 → B2 · rest 75 s. |
| Every 2:00 | `Each round: A1 → A2 · rest = time left.` | Each round: A1 → A2 · rest = time left. |
| Every 2:00, sided single bell | `Each round: 45 s left · 45 s right · 20 s rest. RPE 6–7.` | (KB flow, pc-v27) |
| EMOM | `Each 75 s: set up · work · rest.` | Each 75 s: set up · work · rest. |
| Intervals | `Each round: W work · R rest. <word> pace, RPE n.` | Each round: 1:00 work · 1:00 rest. Moderate pace, RPE 7. |
| Circuit | `Each round: N s per move · R s rest.` | Each round: 25 s per move · 15 s rest. |
| Steady | `<Word> pace, RPE n.` (+ Zone where standard) | Steady pace, Zone 2, RPE 5–6. |
| Warm-up / Flow / Cool-down (flows) | `Each move: time shown · sides cued.` | Each move: time shown · sides cued. |
| Warm-up / Cool-down (walk or row) | as Steady | Easy walk, RPE 3–4. |

Anything else goes in **small print** (13 px, one line, ≤70 characters). That covers the "last round has no rest" note, machine settings (damper 4–5, stroke rate), optional rest fillers, and how the rest timer works.

## 3. How moves are written
- **Strength cards:** `A1 Name` on the title line. The prescription line is `sets × reps [each side]` then the **tempo chip** (e.g. `4 × 6  [3011]`), with the tempo meaning underneath. Reps pills are pre-filled; weight is entered with `+ kg`. The suggested weight and the cue sit under **More**.
- **Timed moves:** `Name – 30 s` or `Name – 30 s each side`. Carries: `Name – 30 m`.
- **Rep-based moves in a guided block:** `Name ×5`. "each side" is written once, in the group heading.
- **"each side"** is always spelled out. It's never "per side", "/side" or "L/R". The guided timer splits each side and cues `SWITCH SIDES`.
- **One move per line.** No "A or B" names; if there's a choice, name the default and put the alternative in the How-to.
- Every move name is tappable for its How-to.

## 4. Alternating rounds
When rounds alternate, group the moves under round headings, expanded, with "each side" in the heading:
`ROUNDS 1 · 3 · 5  each side` → Swing ×5 · Clean ×3 · Press ×3
`ROUNDS 2 · 4  each side` → Front-rack squat ×4 · Row ×6
The Now/Next bar shows the round's moves with reps (e.g. "Swing ×5, Clean ×3, Press ×3 · left side · round 1/5").

## 5. Warm-up and cool-down
- The header is `1 · Warm-up · m:ss` (a second walk/row warm-up is `2 · Warm-up · m:ss`). The last block(s) are `Cool-down`.
- **Card:** title (what: "Dynamic stretch – upper"), the fixed instruction line, then the collapsed `Show N moves` list, then `Start guided flow · m:ss`.
- Order goes standing → kneeling → floor (warm-ups the other way round). GET READY only appears when the position changes.

## 6. Effort wording (approved 18 Oct 2026: non-overlapping bands)
- Single words only, always written with the RPE from their band:

| Word | RPE | Talk test | Typical use |
|---|---|---|---|
| **easy** | 3–4 | full sentences, nasal breathing | walks, warm-up/cool-down walks or rows, recovery |
| **steady** | 5–6 | sentences, a little breathless | Zone 2 runs, steady rows, long continuous work |
| **moderate** | 7 | short phrases | all interval work |
| **hard** | 8+ | – | **not used** (medical) |

- Strength and kettlebell blocks state `RPE 6–7` with 2 reps in reserve (the safety line), and need no effort word.
- No numeric paces (min/km, km/h, /500 m, drag factor). Stroke rate (s/m) and damper go in small print only.
- *(Superseded: the pc-v27 draft used overlapping bands, easy 3–6 / steady 6–7 / moderate 7. Section 12's R3 rows were generated against that draft, so re-check every effort phrase against the table above.)*

## 7. Terminology
- Standard names: Superset, Tri-set, EMOM, Every 2:00, Intervals, Zone 2, RPE, RIR, Assault Runner, PM5.
- Spell out **kettlebell** and **dumbbell** in move names (KB/DB only in the week-strip short names).
- Units: `s`, `m`, `kg`, times as `m:ss`. Use `×` for reps and rounds, `·` as the separator, and `→` for order.
- Safety line ≤160 characters, ending with the RPE/RIR. The stop-signs line stays global.

## 8. Which timer appears where
- **Guided timer** (Pause / Back / Next / Stop, switch-sides cues, beeps): Warm-up, Every, EMOM, Intervals, Circuit, Steady, Flow, Cool-down.
- **Rest timer** (auto-starts when the last move of a round is ticked; −15 s / +15 s / Skip): Straight sets, Superset, Tri-set. The manual `⏱ Rest timer` button is always there.

## 9. Button labels
- `Start guided timer · m:ss` for every guided block that isn't a flow (including Steady and Intervals).
- `Start guided flow · m:ss` for flows (warm-up, flow, cool-down).
- When done: `✓ Done · run guided timer again · m:ss`. Counters: `+1 walk break · N`.
- No other wording ("Start 15:00", "Start row", "Start flow", "Start core", "Start walk" all change).

## 10. Expanded vs collapsed
- **Expanded:** strength move cards (title, prescription, tempo, pills), round groups, interval/circuit move lists, the instruction line.
- **Collapsed:** the warm-up / flow / cool-down move lists (`Show N moves`), the cue, suggested weight and How-to (under `More`), and the optional log fields.

## 11. Maximum text lengths (iPhone 390 px)
| Element | Max |
|---|---|
| Block header | 32 chars |
| Card title | 30 chars |
| Instruction line | 60 chars (one line) |
| Small print | 70 chars |
| Move line | 36 chars |
| Safety line | 160 chars |

## 12. Audit against this standard (pc-v27 live data)
**159 deviations** across 19 session views (7 main, 7 backup, 1 quick option, 4 run-instead). Blocks shared between views (e.g. the same warm-up under Run instead) are counted once.

| Rule | Count |
|---|---|
| R1 header | 45 |
| R10 expanded/collapsed | 2 |
| R2 instruction line | 65 |
| R3 effort | 13 |
| R5 terminology | 5 |
| R7 length | 10 |
| R9 button | 19 |

The biggest groups, which each need one code change rather than per-session edits:
- **R1 headers (45):** "Active warm-up/cool-down" → Warm-up/Cool-down, "Main"/"Easy finisher" → Steady, "Conditioning finisher" → Intervals, "Pair"/"Pump tri-set" → Superset/Tri-set, "Every 75 s × N stations × 3" → EMOM 75 s × 3, "Core" → Circuit × 2.
- **R2 instruction lines (65):** the Every/Superset/EMOM generated lines are 89–117 chars. Flow notes ("Gentle", "No forcing") become the fixed "Each move:" line. Interval notes are 80–97 chars and become "Each round: … RPE n." with s/m and damper moved to small print.
- **R9 buttons (19):** "Start 5:00", "Start row", "Start flow", "Start core", "Start walk", "Start run", "Start intervals" → Start guided timer · m:ss.
- **R3 effort (13):** "steady run, RPE 7" in intervals (→ moderate), effort words without RPE (warm-up/cool-down walks and rows), "Sustainable pace"/"RPE 6 max" in safety lines.
- **R5 terminology (5):** "KB"/"DB" in move names (Single-arm KB row ×2, Half-kneeling one-arm DB press, Single-leg KB RDL) and "Assisted pull-ups or dips".
- **R7 lengths (10):** long card titles (31–42 chars) and the quick-option safety line (198 chars).
- **R10 (2):** the Wed core circuit moves are hidden behind "Show 3 moves".

### Full list by session

**Easy Run** (16)
- R1 header · 1 · Active warm-up · 4:30: 'Active warm-up' → 'Warm-up'
- R2 instruction line · 1 · Active warm-up · 4:30: 'Smooth and easy' (15 chars) → fixed line for its format, ≤60 chars
- R2 instruction line · 2 · Warm-up · 5:00: '5:00 easy pace' (14 chars) → fixed line for its format, ≤60 chars
- R3 effort · 2 · Warm-up · 5:00: effort word without RPE: '5:00 easy pace' → add RPE from the section 6 bands (easy 3–4 · steady 5–6 · moderate 7)
- R9 button · 2 · Warm-up · 5:00: 'Start 5:00' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R1 header · 3 · Main · 15:00: 'Main' → 'Steady'
- R2 instruction line · 3 · Main · 15:00: '15:00 · RPE 6 · 1:00 walk break whenever needed' (47 chars) → fixed line for its format, ≤60 chars
- R3 effort · 3 · Main · 15:00: RPE without effort word: '15:00 · RPE 6 · 1:00 walk break whenever needed' → pair with the single effort word
- R9 button · 3 · Main · 15:00: 'Start 15:00' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R2 instruction line · 4 · Cool-down · 5:00: '5:00 easy walk' (14 chars) → fixed line for its format, ≤60 chars
- R3 effort · 4 · Cool-down · 5:00: effort word without RPE: '5:00 easy walk' → add RPE from the section 6 bands (easy 3–4 · steady 5–6 · moderate 7)
- R9 button · 4 · Cool-down · 5:00: 'Start 5:00' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R1 header · 5 · Flow finisher · 5:00: 'Flow finisher' → 'Flow'
- R7 length · 5 · Flow finisher · 5:00: title 32 chars: 'Standing → kneeling → floor flow' → ≤30 chars
- R2 instruction line · 5 · Flow finisher · 5:00: 'Slow and controlled, nasal breathing. Move with the timer; sides are cued.' (74 chars) → fixed line for its format, ≤60 chars
- R3 effort · safety line: 'Easy run, Zone 2, RPE 6 max: easy, conversational pace. Run …' → single effort word + RPE

**Backup · Easy Row + Mobility [backup]** (8)
- R1 header · 1 · Active warm-up · 4:40: 'Active warm-up' → 'Warm-up'
- R2 instruction line · 1 · Active warm-up · 4:40: 'Gentle' (6 chars) → fixed line for its format, ≤60 chars
- R1 header · 2 · Main · 24:10: 'Main' → 'Steady'
- R2 instruction line · 2 · Main · 24:10: '24:00 easy pace, 18–20 s/m, damper 4–5' (38 chars) → fixed line for its format, ≤60 chars
- R3 effort · 2 · Main · 24:10: effort word without RPE: '24:00 easy pace, 18–20 s/m, damper 4–5' → add RPE from the section 6 bands (easy 3–4 · steady 5–6 · moderate 7)
- R9 button · 2 · Main · 24:10: 'Start row · 24:10' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R1 header · 3 · Mobility · 4:50: 'Mobility' → 'Flow'
- R2 instruction line · 3 · Mobility · 4:50: 'Controlled, keep breathing' (26 chars) → fixed line for its format, ≤60 chars

**Strength A · Upper** (13)
- R1 header · 1 · Active warm-up · 4:40: 'Active warm-up' → 'Warm-up'
- R2 instruction line · 1 · Active warm-up · 4:40: 'No forcing' (10 chars) → fixed line for its format, ≤60 chars
- R2 instruction line · 2 · A · Every 2:00 × 4 · 7:30: 'Start a new round every 2:00. Rest is whatever is left. The last round ends after its last set, so the block is 7:30.' (117 chars) → fixed line for its format, ≤60 chars; extra into small print
- R2 instruction line · 3 · B · Superset × 3 · ≈8:30: 'Rest 75 s after each round · the rest timer starts when you tick the last move of a round' (89 chars) → fixed line for its format, ≤60 chars; extra into small print
- R5 terminology · 3 · B · Superset × 3 · ≈8:30: abbreviation in move name: 'B2Half-kneeling one-arm DB press' → spell out kettlebell/dumbbell
- R1 header · 4 · C · Pump tri-set × 2 · ≈6:15: 'C · Pump tri-set × 2' → 'C · Tri-set × 2'
- R2 instruction line · 4 · C · Pump tri-set × 2 · ≈6:15: 'Rest 75 s after each round · the rest timer starts when you tick the last move of a round' (89 chars) → fixed line for its format, ≤60 chars; extra into small print
- R1 header · 5 · Conditioning finisher · 3:40: 'Conditioning finisher' → 'Intervals'
- R7 length · 5 · Conditioning finisher · 3:40: title 31 chars: 'Row intervals 3 × (0:50 / 0:30)' → ≤30 chars
- R2 instruction line · 5 · Conditioning finisher · 3:40: 'Work 0:50 steady pace, 22–24 s/m · rest 0:30 light paddle, 18–20 s/m · damper 4–5 · RPE 6–7' (91 chars) → fixed line for its format, ≤60 chars
- R9 button · 5 · Conditioning finisher · 3:40: 'Start flow · 3:40' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R1 header · 6 · Active cool-down · 3:30: 'Active cool-down' → 'Cool-down'
- R2 instruction line · 6 · Active cool-down · 3:30: 'Breathe out into each stretch' (29 chars) → fixed line for its format, ≤60 chars

**Backup · Upper (KB + Bodyweight) [backup]** (13)
- R1 header · 1 · Active warm-up · 4:40: 'Active warm-up' → 'Warm-up'
- R2 instruction line · 1 · Active warm-up · 4:40: 'No forcing' (10 chars) → fixed line for its format, ≤60 chars
- R2 instruction line · 2 · A · Every 2:00 × 4 · 7:45: 'Start a new round every 2:00. Rest is whatever is left. The last round ends after its last set, so the block is 7:45.' (117 chars) → fixed line for its format, ≤60 chars; extra into small print
- R2 instruction line · 3 · B · Superset × 3 · ≈9:45: 'Rest 75 s after each round · the rest timer starts when you tick the last move of a round' (89 chars) → fixed line for its format, ≤60 chars; extra into small print
- R5 terminology · 3 · B · Superset × 3 · ≈9:45: abbreviation in move name: 'B1Single-arm KB row' → spell out kettlebell/dumbbell
- R1 header · 4 · C · Pair × 2 · ≈4:00: 'C · Pair × 2' → 'C · Superset × 2'
- R2 instruction line · 4 · C · Pair × 2 · ≈4:00: 'Rest 60 s after each round · the rest timer starts when you tick the last move of a round' (89 chars) → fixed line for its format, ≤60 chars; extra into small print
- R1 header · 5 · Conditioning finisher · 3:50: 'Conditioning finisher' → 'Intervals'
- R7 length · 5 · Conditioning finisher · 3:50: title 31 chars: 'Row intervals 4 × (0:40 / 0:20)' → ≤30 chars
- R2 instruction line · 5 · Conditioning finisher · 3:50: 'Work 0:40 steady pace, 22–24 s/m · rest 0:20 light paddle · damper 4–5 · RPE 6–7' (80 chars) → fixed line for its format, ≤60 chars
- R9 button · 5 · Conditioning finisher · 3:50: 'Start flow · 3:50' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R1 header · 6 · Active cool-down · 3:30: 'Active cool-down' → 'Cool-down'
- R2 instruction line · 6 · Active cool-down · 3:30: 'Breathe out into each stretch' (29 chars) → fixed line for its format, ≤60 chars

**Rower Intervals** (16)
- R1 header · 1 · Active warm-up · 4:40: 'Active warm-up' → 'Warm-up' (also in 1 other view)
- R2 instruction line · 1 · Active warm-up · 4:40: no instruction line → add the fixed line for its format (also in 1 other view)
- R2 instruction line · 2 · Warm-up · 4:00: '4:00 build from easy to steady pace, 18–22 s/m, damper 4–5' (58 chars) → fixed line for its format, ≤60 chars
- R3 effort · 2 · Warm-up · 4:00: effort word without RPE: '4:00 build from easy to steady pace, 18–22 s/m, damper 4–5' → add RPE from the section 6 bands (easy 3–4 · steady 5–6 · moderate 7)
- R9 button · 2 · Warm-up · 4:00: 'Start 4:00' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss') (also in 1 other view)
- R7 length · 3 · Intervals · 11:05: title 34 chars: 'Row intervals 6 × 1:00 / 1:00 rest' → ≤30 chars
- R2 instruction line · 3 · Intervals · 11:05: '6 × 1:00 moderate pace, 24–26 s/m, RPE 7 · 1:00 rest (5 s ready + 0:55 light paddle) · damper 4–5' (97 chars) → fixed line for its format, ≤60 chars
- R9 button · 3 · Intervals · 11:05: 'Start intervals · 11:05' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss') (also in 1 other view)
- R2 instruction line · 4 · Steady · 4:00: '4:00 steady pace, 20–22 s/m, RPE 6' (34 chars) → fixed line for its format, ≤60 chars
- R9 button · 4 · Steady · 4:00: 'Start 4:00' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss') (also in 1 other view)
- R1 header · 5 · Core finisher · 6:30: 'Core finisher' → 'Circuit × 2' (also in 1 other view)
- R2 instruction line · 5 · Core finisher · 6:30: 'Exhale slowly, no breath-holding' (32 chars) → fixed line for its format, ≤60 chars (also in 1 other view)
- R10 expanded/collapsed · 5 · Core finisher · 6:30: main-work moves hidden behind 'Show N moves' → expand by default (also in 1 other view)
- R9 button · 5 · Core finisher · 6:30: 'Start core · 6:30' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss') (also in 1 other view)
- R1 header · 6 · Active cool-down · 3:10: 'Active cool-down' → 'Cool-down' (also in 1 other view)
- R2 instruction line · 6 · Active cool-down · 3:10: 'Slow and easy' (13 chars) → fixed line for its format, ≤60 chars (also in 1 other view)

**Backup · Run/Walk + Core [brun]** (12)
- R1 header · 1 · Active warm-up · 4:30: 'Active warm-up' → 'Warm-up' (also in 1 other view)
- R2 instruction line · 1 · Active warm-up · 4:30: 'Gentle' (6 chars) → fixed line for its format, ≤60 chars (also in 1 other view)
- R1 header · 2 · Walk intervals · 15:10: 'Walk intervals' → 'Intervals' (also in 1 other view)
- R1 header · 3 · Core · 6:10: 'Core' → 'Circuit × 2' (also in 1 other view)
- R2 instruction line · 3 · Core · 6:10: 'Exhale slowly, no breath-holding' (32 chars) → fixed line for its format, ≤60 chars (also in 1 other view)
- R10 expanded/collapsed · 3 · Core · 6:10: main-work moves hidden behind 'Show N moves' → expand by default (also in 1 other view)
- R9 button · 3 · Core · 6:10: 'Start core · 6:10' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss') (also in 1 other view)
- R1 header · 4 · Active cool-down · 3:10: 'Active cool-down' → 'Cool-down' (also in 1 other view)
- R2 instruction line · 4 · Active cool-down · 3:10: 'Slow and easy' (13 chars) → fixed line for its format, ≤60 chars (also in 1 other view)
- R7 length · 2 · Walk intervals · 15:10: title 36 chars: 'Run/walk intervals 8 × (1:00 / 1:00)' → ≤30 chars
- R2 instruction line · 2 · Walk intervals · 15:10: 'Work 1:00 easy run, RPE 6 · rest 1:00 recovery walk' (51 chars) → fixed line for its format, ≤60 chars
- R9 button · 2 · Walk intervals · 15:10: 'Start intervals · 15:10' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')

**Backup · Runner Walk + Core [backup]** (3)
- R7 length · 2 · Walk intervals · 15:10: title 32 chars: 'Walk intervals 8 × (1:00 / 1:00)' → ≤30 chars
- R2 instruction line · 2 · Walk intervals · 15:10: 'Work 1:00 power walk · rest 1:00 recovery walk · Assault Runner' (63 chars) → fixed line for its format, ≤60 chars
- R9 button · 2 · Walk intervals · 15:10: 'Start walk · 15:10' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')

**Run Intervals [run]** (6)
- R2 instruction line · 2 · Warm-up · 4:00: '4:00 easy pace' (14 chars) → fixed line for its format, ≤60 chars
- R3 effort · 2 · Warm-up · 4:00: effort word without RPE: '4:00 easy pace' → add RPE from the section 6 bands (easy 3–4 · steady 5–6 · moderate 7)
- R7 length · 3 · Intervals · 11:05: title 36 chars: 'Run/walk intervals 6 × (1:00 / 1:00)' → ≤30 chars
- R2 instruction line · 3 · Intervals · 11:05: 'Work 1:00 run, moderate pace, RPE 7 · rest 1:00 recovery walk (5 s ready + 0:55 walk)' (85 chars) → fixed line for its format, ≤60 chars
- R1 header · 4 · Easy run · 4:00: 'Easy run' → 'Steady'
- R2 instruction line · 4 · Easy run · 4:00: '4:00 easy pace, RPE 6 · walk break whenever needed' (50 chars) → fixed line for its format, ≤60 chars

**Active Mobility Flow** (2)
- R1 header · 1 · Guided flow · 15:00: 'Guided flow' → 'Flow'
- R2 instruction line · 1 · Guided flow · 15:00: 'CARs and end-range holds. Standing → kneeling → floor; 10 s to set up only when you change position.' (100 chars) → fixed line for its format, ≤60 chars

**Backup · Easy Walk + Breathing [backup]** (6)
- R1 header · 1 · Walk · 10:00: 'Walk' → 'Steady'
- R2 instruction line · 1 · Walk · 10:00: '10:00 easy pace · nasal breathing' (33 chars) → fixed line for its format, ≤60 chars
- R3 effort · 1 · Walk · 10:00: effort word without RPE: '10:00 easy pace · nasal breathing' → add RPE from the section 6 bands (easy 3–4 · steady 5–6 · moderate 7)
- R9 button · 1 · Walk · 10:00: 'Start 10:00' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R1 header · 2 · Breathe + stretch · 4:30: 'Breathe + stretch' → 'Cool-down'
- R2 instruction line · 2 · Breathe + stretch · 4:30: 'Slow, calm' (10 chars) → fixed line for its format, ≤60 chars

**Strength B · Lower + Core** (13)
- R1 header · 1 · Active warm-up · 4:20: 'Active warm-up' → 'Warm-up'
- R2 instruction line · 1 · Active warm-up · 4:20: 'No forcing' (10 chars) → fixed line for its format, ≤60 chars
- R2 instruction line · 2 · A · Every 2:00 × 4 · 7:35: 'Start a new round every 2:00. Rest is whatever is left. The last round ends after its last set, so the block is 7:35.' (117 chars) → fixed line for its format, ≤60 chars; extra into small print
- R2 instruction line · 3 · B · Superset × 3 · ≈9:15: 'Rest 75 s after each round · the rest timer starts when you tick the last move of a round' (89 chars) → fixed line for its format, ≤60 chars; extra into small print
- R1 header · 4 · C · Pump tri-set × 2 · ≈7:40: 'C · Pump tri-set × 2' → 'C · Tri-set × 2'
- R2 instruction line · 4 · C · Pump tri-set × 2 · ≈7:40: 'Rest 60 s after each round · the rest timer starts when you tick the last move of a round' (89 chars) → fixed line for its format, ≤60 chars; extra into small print
- R1 header · 5 · Conditioning finisher · 2:20: 'Conditioning finisher' → 'Intervals'
- R7 length · 5 · Conditioning finisher · 2:20: title 42 chars: 'Assault Runner intervals 2 × (0:40 / 0:50)' → ≤30 chars
- R2 instruction line · 5 · Conditioning finisher · 2:20: 'Work 0:40 steady run, RPE 7 · rest 0:50 recovery walk' (53 chars) → fixed line for its format, ≤60 chars
- R3 effort · 5 · Conditioning finisher · 2:20: interval work at RPE 7 called 'steady' → 'moderate pace, RPE 7'
- R9 button · 5 · Conditioning finisher · 2:20: 'Start flow · 2:20' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R1 header · 6 · Active cool-down · 3:10: 'Active cool-down' → 'Cool-down'
- R2 instruction line · 6 · Active cool-down · 3:10: 'Breathe out into each stretch' (29 chars) → fixed line for its format, ≤60 chars

**Backup · Lower (Single-leg + Floor) [backup]** (13)
- R1 header · 1 · Active warm-up · 4:20: 'Active warm-up' → 'Warm-up'
- R2 instruction line · 1 · Active warm-up · 4:20: 'No forcing' (10 chars) → fixed line for its format, ≤60 chars
- R2 instruction line · 2 · A · Every 2:00 × 4 · 7:45: 'Start a new round every 2:00. Rest is whatever is left. The last round ends after its last set, so the block is 7:45.' (117 chars) → fixed line for its format, ≤60 chars; extra into small print
- R2 instruction line · 3 · B · Superset × 3 · ≈10:00: 'Rest 75 s after each round · the rest timer starts when you tick the last move of a round' (89 chars) → fixed line for its format, ≤60 chars; extra into small print
- R5 terminology · 3 · B · Superset × 3 · ≈10:00: abbreviation in move name: 'B1Single-leg KB RDL (hand on rack)' → spell out kettlebell/dumbbell
- R1 header · 4 · C · Pair × 2 · ≈5:20: 'C · Pair × 2' → 'C · Superset × 2'
- R2 instruction line · 4 · C · Pair × 2 · ≈5:20: 'Rest 60 s after each round · the rest timer starts when you tick the last move of a round' (89 chars) → fixed line for its format, ≤60 chars; extra into small print
- R1 header · 5 · Easy finisher · 3:10: 'Easy finisher' → 'Steady'
- R2 instruction line · 5 · Easy finisher · 3:10: '3:00 easy pace, 18–20 s/m, damper 4–5 · flush the legs' (54 chars) → fixed line for its format, ≤60 chars
- R3 effort · 5 · Easy finisher · 3:10: effort word without RPE: '3:00 easy pace, 18–20 s/m, damper 4–5 · flush the legs' → add RPE from the section 6 bands (easy 3–4 · steady 5–6 · moderate 7)
- R9 button · 5 · Easy finisher · 3:10: 'Start row · 3:10' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R1 header · 6 · Active cool-down · 3:10: 'Active cool-down' → 'Cool-down'
- R2 instruction line · 6 · Active cool-down · 3:10: 'Breathe out into each stretch' (29 chars) → fixed line for its format, ≤60 chars

**KB + Carry Flow** (9)
- R1 header · 1 · Active warm-up · 4:40: 'Active warm-up' → 'Warm-up'
- R2 instruction line · 1 · Active warm-up · 4:40: no instruction line → add the fixed line for its format
- R2 instruction line · 2 · A · Every 2:00 × 4 · 7:40: 'Start a new round every 2:00. Rest is whatever is left. The last round ends after its last set, so the block is 7:40.' (117 chars) → fixed line for its format, ≤60 chars; extra into small print
- R5 terminology · 2 · A · Every 2:00 × 4 · 7:40: abbreviation in move name: 'A1Single-arm KB row' → spell out kettlebell/dumbbell
- R1 header · 3 · B · Every 75 s × 4 stations × 3 · 14:50: 'B · Every 75 s × 4 stations × 3' → 'B · EMOM 75 s × 3'
- R2 instruction line · 3 · B · Every 75 s × 4 stations × 3 · 14:50: 'Every 75 s: 15–20 s to set up, work, then rest until the next station. No rest after the final station.' (103 chars) → fixed line for its format, ≤60 chars; extra into small print
- R1 header · 4 · Active cool-down · 3:10: 'Active cool-down' → 'Cool-down'
- R2 instruction line · 4 · Active cool-down · 3:10: 'Slow and easy' (13 chars) → fixed line for its format, ≤60 chars
- R3 effort · safety line: 'Sustainable pace, RPE 6–7. Exhale on every swing, put the be…' → single effort word + RPE

**Backup · Dumbbell Flow (no KB) [backup]** (12)
- R1 header · 1 · Active warm-up · 4:40: 'Active warm-up' → 'Warm-up' (also in 1 other view)
- R2 instruction line · 1 · Active warm-up · 4:40: no instruction line → add the fixed line for its format (also in 1 other view)
- R2 instruction line · 2 · A · Every 2:00 × 4 · 7:45: 'Start a new round every 2:00. Rest is whatever is left. The last round ends after its last set, so the block is 7:45.' (117 chars) → fixed line for its format, ≤60 chars; extra into small print (also in 1 other view)
- R1 header · 3 · B · Every 75 s × 3 stations × 3 · 11:05: 'B · Every 75 s × 3 stations × 3' → 'B · EMOM 75 s × 3' (also in 1 other view)
- R2 instruction line · 3 · B · Every 75 s × 3 stations × 3 · 11:05: 'Every 75 s: 15–20 s to set up, work, then rest until the next station. No rest after the final station.' (103 chars) → fixed line for its format, ≤60 chars; extra into small print (also in 1 other view)
- R5 terminology · 3 · B · Every 75 s × 3 stations × 3 · 11:05: two moves in one name: 'B2Assisted pull-ups or dips' → one move per line (also in 1 other view)
- R1 header · 4 · Easy finisher · 5:10: 'Easy finisher' → 'Steady' (also in 1 other view)
- R2 instruction line · 4 · Easy finisher · 5:10: 'Assault Runner easy walk · RPE 3' (32 chars) → fixed line for its format, ≤60 chars
- R9 button · 4 · Easy finisher · 5:10: 'Start walk · 5:10' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R1 header · 5 · Active cool-down · 3:10: 'Active cool-down' → 'Cool-down' (also in 1 other view)
- R2 instruction line · 5 · Active cool-down · 3:10: 'Slow and easy' (13 chars) → fixed line for its format, ≤60 chars (also in 1 other view)
- R3 effort · safety line: 'Dumbbells only. Sustainable pace, RPE 6. Breathe out on ever…' → single effort word + RPE

**15-min KB Flow (16 kg) [quick]** (4)
- R2 instruction line · 1 · Warm-up · 3:00: 'Slow and smooth with the 16 kg bell.' (36 chars) → fixed line for its format, ≤60 chars
- R1 header · 3 · Finish · 2:20: 'Finish' → 'Cool-down'
- R2 instruction line · 3 · Finish · 2:20: 'Long, slow exhales to wind down for the evening.' (48 chars) → fixed line for its format, ≤60 chars
- R7 length · safety line: 198 chars → ≤160 chars

**Backup · Dumbbell Flow + Easy Run [brun]** (2)
- R9 button · 4 · Easy finisher · 5:10: 'Start run · 5:10' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss')
- R3 effort · safety line: 'Dumbbells only. Sustainable pace, RPE 6. Breathe out on ever…' → single effort word + RPE

**Easy Long Walk** (7)
- R1 header · 1 · Active warm-up · 4:30: 'Active warm-up' → 'Warm-up' (also in 1 other view)
- R2 instruction line · 1 · Active warm-up · 4:30: 'Gentle' (6 chars) → fixed line for its format, ≤60 chars (also in 1 other view)
- R1 header · 2 · Main · 25:00: 'Main' → 'Steady' (also in 1 other view)
- R2 instruction line · 2 · Main · 25:00: '25:00 easy pace · RPE 3–4' (25 chars) → fixed line for its format, ≤60 chars
- R9 button · 2 · Main · 25:00: 'Start 25:00' → 'Start guided timer · m:ss' (flows: 'Start guided flow · m:ss') (also in 1 other view)
- R1 header · 3 · Stretch · 6:20: 'Stretch' → 'Cool-down' (also in 1 other view)
- R2 instruction line · 3 · Stretch · 6:20: 'Breathe out into each stretch' (29 chars) → fixed line for its format, ≤60 chars (also in 1 other view)

**Backup · Long Stretch + Breathe [backup]** (2)
- R1 header · 1 · Stretch flow · 15:20: 'Stretch flow' → 'Flow'
- R2 instruction line · 1 · Stretch flow · 15:20: 'Gentle holds' (12 chars) → fixed line for its format, ≤60 chars

**Easy Run [run]** (2)
- R7 length · 2 · Main · 25:00: title 34 chars: 'Easy run (Zone 2) with walk breaks' → ≤30 chars
- R2 instruction line · 2 · Main · 25:00: '25:00 easy pace · RPE 5–6 · 1:00 walk break whenever needed' (59 chars) → fixed line for its format, ≤60 chars
