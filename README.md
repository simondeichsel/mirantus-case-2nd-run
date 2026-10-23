# Mirantus product case: making return screenings a habit

My submission for the [Mirantus product case study](CASE.md). Claude Code does the product work
from the setup in this repository; I judge it at fixed checkpoints. All data in `data/` is
synthetic and unchanged from the case.

## What is where

| Path | What |
|---|---|
| `CLAUDE.md` | The brief: goal, users, evidence rules, definition of good, what Claude must never do |
| `.claude/skills/run-case/` | The workflow: steps, checkpoints, interactive and auto mode |
| `.claude/skills/decision-memo/` | The one-page memo template |
| `.claude/agents/` | `data-analyst`, `qual-researcher`, `reviewer` (independent, fresh context) |
| `scripts/analyze.py` | All numbers. Written in step 1, rerun on every run |
| `scripts/check_outputs.py` | Deterministic checks and staleness tracking |
| `data/` | Case inputs. Never edited by Claude |
| `outputs/` | What the run produced, plus `CHECKPOINTS.md` (decisions taken) |
| `transcripts/` | Exported Claude Code sessions: building the setup, and the run |

## How to rerun

Requirements: Claude Code and Python 3 (standard library only). Open Claude Code in this folder.

```
/run-case              full run, interactive: stops for the analysis walkthrough, CP1 and CP2
/run-case auto         full run, no stops; Claude decides at the checkpoints and logs why
/run-case 3 auto       rerun from step 3 onwards
```

**After changing an input**, find out what to rerun:

```
python3 scripts/check_outputs.py --stale
```

It compares every step's inputs with the state recorded at its last run and prints the step to
rerun from. As a guide:

| Changed input | Rerun from |
|---|---|
| `data/screenings.csv`, `data/README.md` | step 1 (then 3–5) |
| `data/interviews/*`, `data/optician-survey.md` | step 2 (then 3–5) |
| `data/constraints.md` | step 3 |
| `data/customer-journey.md` | step 2 |

In auto mode, my earlier checkpoint decisions in `outputs/CHECKPOINTS.md` stay in force unless the
changed input undermines them; Claude then says which input and why. The run ends with a short
report of what changed in the outputs. The prototype in Claude Design is rebuilt by hand from the
updated `outputs/05-prototype-spec.md`.

## Self-checks

- `python3 scripts/check_outputs.py` after every step: every rate and n in the outputs must
  appear in `outputs/01-data-analysis.md` (targets are tagged `[TARGET]`), source tags must point
  to existing interviews and survey answers, the memo is at most 600 words and has every
  section, and the memo and customer copy contain no fear phrases.
- The `reviewer` subagent before every checkpoint: constraints, evidence, logic, users, focus.
