# Brief: Swap days in the week (for Claude Code)

*Approved by James on 5 Nov 2026. Read `CLAUDE.md` first (architecture, hard rules, localStorage compatibility), then this brief.*

**Goal:** Let James **swap two day slots in the current week** so the weekly plan stays intentional, but the session he actually trains shows on the calendar day he does it. Logs attach to that calendar date.

This is **not** more alternate workouts. **Run instead**, **backup**, and **Quick option** stay as they are. Do **not** expand option menus or add easy-out pickers.

Ship as **one release** (next `pc-vNN` after whatever is live when you start), one commit, tests green.

## Why

The week is a Marcus Filly–style build (compound + supersets, progression). He wants that plan to stay. Sometimes travel or life means he catches up Thursday’s Lower on Friday — he needs those two **day slots** swapped so Friday opens Lower, and Finish workout logs Friday.

Existing **Run instead** already covers “can’t do the gym session, do a run”. Leave it alone.

## UX (phone-first, simple)

1. From the **week strip** or **Edit plan**: let him pick any two days **in the visible current week** and swap them.
   - Acceptable patterns: Edit plan → tap day A → tap day B to swap; or long-press a day → **Swap with…** → tap the other day.
   - Prefer clear labels: **Swap days** / **Swap with…** — do **not** overload the existing **“Swap today’s session”** control (that one is the mailto / `wo_swaps` Health-bot request queue; leave that feature and its UI alone).
2. After the swap, the week strip labels and the opened session for each date reflect the moved mains.
3. Undo: swapping the same pair again (or a small **Reset week order** while in Edit plan) is enough; no heavy history UI.
4. Match whatever theme is live (beauty pass may land first). Do not invent a new palette; reuse current CSS variables.

## Behaviour

- Swapping date **A** and date **B** exchanges which **main** programme session each calendar date shows (the `PROG` / `OVR` resolution for that slot).
- **Finish workout** still logs against the **calendar date** he has open (the day he trained). Ticks / `wo_<date>` stay keyed by that calendar date — as today.
- **Backup**, **Run instead**, and **Quick option** remain available as they are today. Prefer that their session lookups **follow the main session’s source day** after a swap (so Lower’s backup travels with Lower). If that is awkward, document the choice in the commit message and keep behaviour consistent and tested — but do **not** add new alternate pickers.
- Only dates in the **current Mon–Sun week** are swappable. No cross-week moves in this brief.
- Past logged days: allow swap only if it does not corrupt an already-logged day, **or** block swap when either day already has a log (simplest safe rule — pick one and test it). Never rewrite old `wo_log` entries.

## Persistence (compatibility)

Prefer a **new optional localStorage key** so existing `wo_plan` Rest toggles keep working unchanged.

**Recommended key:** `wo_daymap`

| Key | Shape | Meaning |
|---|---|---|
| `wo_daymap` | `{ "YYYY-MM-DD": "YYYY-MM-DD", ... }` | On calendar date **K**, show the main session that `baseSid` would resolve for source date **V** (usually another day in the same week). Missing key = identity (no remap). |

Resolution sketch (keep `wo_plan` Rest / quick / backup toggles working):

1. Start from calendar date `k`.
2. `src = (wo_daymap[k] || k)`.
3. Resolve main id via existing `baseSid(src)` / `OVR` / `PROG`.
4. Apply `wo_plan[k] == "Rest"`, then quick / backup / run-instead toggles as today (keyed by calendar `k` or by `src` per the choice above — document it).

**Rules:**

- Readers must tolerate a missing `wo_daymap`.
- **Never** rename or remove existing keys (`wo_log`, `wo_<date>`, `wo_plan`, `wo_alt`, `wo_ri`, `wo_quick`, `wo_swaps`, …).
- No migration that rewrites old logs. If you need a version bump flag, make it idempotent and optional-field only.

If you find a cleaner approach that only extends `wo_plan` without breaking Rest / legacy values, that is acceptable — but **document the key and value shape in `CLAUDE.md`’s localStorage table**.

## In scope

- Week-strip / Edit plan UI to swap two days in the current week
- Persistence + resolution wired through `sid` / `S_` / week labels
- Playwright coverage for swap → correct session on date → log date unchanged
- `CLAUDE.md` localStorage row for the new key

## Out of scope

- New workout alternatives, bigger menus, or replacing Run instead / backup
- Changing session content, timers, list/clock modes, or beauty-pass tokens
- Cross-week moves, drag-and-drop calendars, multi-select
- Touching the mailto **Swap today’s session** / `wo_swaps` Health-bot flow (except renaming UI copy if needed to avoid confusion)
- Second user profiles

## Process

1. **Pull `main` first.** Beauty-pass brief/docs, **pc-v32 week 4**, and **pc-v31** list + clock modes must remain. Confirm live `sw.js` version before choosing `NN`.
2. Implement swap UX + `wo_daymap` (or documented alternative).
3. Update / add Playwright tests (new `tests/test_vNN.py` or extend an existing suite).
4. `bash scripts/test.sh` — all green.
5. `bash scripts/bump.sh NN`, build, **one** commit: `pc-vNN: swap days in the current week`.
6. Push `main`; confirm Pages.

## Success criteria

- [ ] Two days in the current week can be swapped from the week strip / Edit plan in a few taps.
- [ ] After swap, each date opens the moved main session; week-strip short labels match.
- [ ] Finish workout logs against the calendar date trained.
- [ ] Run instead / backup / quick unchanged as product options (no new pickers).
- [ ] Old installs without `wo_daymap` behave exactly as before.
- [ ] `bash scripts/test.sh` passes; version bumped and live.

## Product reminder

The plan stays intentional. This feature only **moves slots**, it does not offer an easier session. If a request drifts into “pick any workout”, stop and flag it.
