# BRIEF: next approved job (pc-v28)
*Approved by James on 18 Oct 2026. Read `CLAUDE.md` first (architecture, hard rules, compatibility), then `app-style-standard.md`.*
Ship it as **one release, pc-v28**, in one commit, with the tests updated. Don't change the programme content (exercises, sets, reps, weights) beyond what this brief requires.

## (a) Apply the layout standard everywhere
Apply `app-style-standard.md` to **every session**: the 7 main sessions, the 7 backups, the quick option and the 4 Run-instead views (Wed main and backup, Sat backup, Sun main).
- **Work list:** use the **159-deviation audit list** in `app-style-standard.md` §12 ("Audit against this standard"). Clear every row, unless (b) below supersedes it.
- **Shared code first:** most rows come from shared code, so fix these once rather than per session:
  - block header formats (§1);
  - the generated instruction lines for Superset / Every / EMOM (§2);
  - flow notes becoming "Each move: time shown · sides cued.";
  - button labels (§9);
  - small print for the last-round note, machine settings (stroke rate, damper) and optional rest fillers.
- **Effort bands:** use the approved non-overlapping bands (§6) everywhere: notes, safety lines, timer labels and run-instead text:
  - **easy = RPE 3–4**: walks, warm-up and cool-down walks/rows, recovery.
  - **steady = RPE 5–6**: Zone 2 runs, steady rows.
  - **moderate = RPE 7**: all interval work.
  - **hard = RPE 8+**: not used.
  - Relabel every phrase whose word and RPE disagree under these bands. For example, "Easy run (Zone 2), RPE 6" becomes steady effort, and "steady run, RPE 7" intervals become moderate. Agree any renamed session or card titles with James if a title contains an effort word, e.g. "Easy Run" becomes "Zone 2 Run".
  - §12's R3 rows were generated against the old overlapping draft, so re-check all effort text.
- **Also from the audit:**
  - Spell out kettlebell/dumbbell in move names (R5). This is a display-name change only; **keep the exercise ids**.
  - Split "Assisted pull-ups or dips" into one default move with the alternative in its How-to.
  - Shorten long titles and the quick-option safety line to the §11 limits (R7).
  - Expand the Wed core moves (R10).

## (b) Timer rework
1. **Strength and carry blocks** have **no guided timer and no block time**. This covers straight sets, supersets, tri-sets/pairs and carry blocks.
   - Show `sets × reps` (or `× metres` for carries), plus the rest as **"Rest 60–90 s"**, using the block's prescribed range.
   - The **rest timer starts when a set is ticked**: after each tick for straight sets, and after the last move of a round for supersets/tri-sets. It uses the existing `#rbar` (−15 s / +15 s / Skip, beep and flash at 0) and keeps the auto-rest setting and the manual "⏱ Rest timer" button.
   - Convert the current "Every 2:00 × 4" strength A-blocks and the KB "Every 75 s" carry stations: either to rest-timer strength blocks, or keep them as true EMOM/Every blocks only if (2) below holds. Choose per block, and list each choice in the commit message.
2. **Keep the guided timer only for EMOM, Every X, intervals and flows** (warm-up, cool-down and mobility flows included).
   - In every guided block, **the work must fit inside the window with real rest left**. Each window needs ≥15 s of genuine rest after set-up and work, including both sides for sided moves.
   - No trailing rest. Switch-sides cues on every sided move. GET READY only on position changes in flows.
3. **Headers show time only when it's exact,** i.e. it equals the guided-timer total. Otherwise show a count, e.g. `3 · B · Superset · 3 rounds`.
   - Remove the "≈m:ss" estimates.
   - The session total in the day note (`· NN min`) becomes the sum of the exact guided times plus an estimate for strength blocks, labelled "≈". It can be omitted if James prefers.
4. Keep Pause/Back/Next/Stop, beeps on every segment (AudioContext, never vibration), the "finished while locked → Mark done / Not done" prompt and the audio resume on return.

## (c) Acceptance criteria
- [ ] Every session view matches `app-style-standard.md`. A new automated audit in `tests/test_v28.py` reports **0 deviations**. It re-implements the §1/§2/§6/§9/§11 checks against the rendered DOM of all 19 views and replaces the one-off audit script.
- [ ] Effort words appear only with an RPE inside their band (easy 3–4, steady 5–6, moderate 7). No "hard", no combined or hyphenated terms, no numeric paces.
- [ ] Strength and carry blocks have no `[data-t]` guided-timer button and no time in the header. They show "Rest X–Y s", and ticking a set starts `#rbar` with the prescribed rest (and doesn't when auto-rest is off).
- [ ] Every remaining guided block is EMOM / Every / intervals / flow.
  - In each window, set-up + work ≤ window − 15 s.
  - No trailing REST.
  - Sided moves are cued.
  - Header time = timer total.
- [ ] Full-session Playwright run on every day type (main, backup, quick, run-instead) at 390×844. Every guided block counts down and beeps on every segment (`window.__bp`), and no `navigator.vibrate` calls are made.
- [ ] **Saved logs are untouched.** Seed `wo_log`, `wo_<date>`, `wo_wt`, `wo_alt`, `wo_ri` and `wo_quick` with pc-v27-shaped data. After the upgrade, history, "Last: kg", ticks, done-flags and the history Edit dropdown still work, and no entry changes name or type.
- [ ] Safety unchanged: the stop-signs line is visible on every session, the RPE 6–7 / 2 RIR wording is kept, and there are no head-down moves or breath-holds.
- [ ] `bash scripts/test.sh` passes on all suites. `bash scripts/bump.sh 28` has been run, so `sw.js` has `pc-v28`, plus the page marker. There's one commit, and it's confirmed live (curl + cmp).

## Tests to update
- **`tests/test_v25.py`:**
  - `superset has no guided timer` becomes all strength/carry blocks;
  - the h2 totals-equal-timer check applies to exact-time headers only;
  - the rest-bar tests extend to straight sets;
  - drop the expectations for the `kemom` / `kcirc` / `x13a` / `x16a` / `x17a` / `x17b` / `aemom` / `bemom` timers that become rest-timer blocks.
- **`tests/test_v18.py`:**
  - the header-totals-add-up check (`labelled block times add up`) must handle "N rounds" headers;
  - the `aemom` / `kcirc` timer walkthroughs change or move to the remaining guided blocks;
  - the How-to coverage stays.
- **`tests/test_v20.py`:** the effort-word and terminology checks move to the new bands. It reads `docs/terminology-audit.md` and `docs/programme-week1.md`, so update those docs with the new bands too.
- **`tests/test_v26.py`:** the quick-option card text, header time (only if it stays exact) and the shorter safety line.
- **`tests/test_app.py`, `tests/test_wt.py`, `tests/test_v24.py`:** should pass unchanged. Adjust only where a header or button label changed.
- **New `tests/test_v28.py`:** the automated standard audit, window-fit checks, the log-compatibility seed test and the per-day full-session run.

## Out of scope
Any new sessions or weeks, programme changes, a redesigned theme, or new dependencies/build tools.
