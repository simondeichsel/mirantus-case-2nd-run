---
name: run-case
description: Run, or rerun from a given step, the Mirantus return-rate case. Arguments are an optional start step (1-5, default 1) and an optional mode (auto). Example "/run-case 3 auto".
---

# Run the Mirantus case

Arguments: `$ARGUMENTS`. The first number is the step to start from (default 1); every later
step runs too. The word `auto` selects auto mode; otherwise the mode is interactive.

## Before step 1 (or the start step)

1. Run `python3 scripts/check_outputs.py --stale`. It lists inputs that changed since each step
   last ran and which steps are now out of date. Tell Simon what it found in two lines.
2. Read `data/constraints.md` fresh. If it differs from what earlier outputs assumed, note the
   changed rule; every regenerated output names it at the top (see `CLAUDE.md`).
3. Read `outputs/CHECKPOINTS.md` if it exists: it holds Simon's earlier decisions.

After every step: run `python3 scripts/check_outputs.py`, fix every failure, then run
`python3 scripts/check_outputs.py --record <step>`.

## Steps

**Step 1: data analysis.** Run the `data-analyst` subagent. Output: `outputs/01-expectations.md`
(written before it looks at the data), `outputs/01-data-analysis.md` (written by
`scripts/analyze.py`) and `outputs/01-data-interpretation.md`.

**Step 2: qualitative evidence.** Run the `qual-researcher` subagent. Output:
`outputs/02-qual-evidence.md`. Steps 1 and 2 are independent: when both run, start them in
parallel.

*Interactive mode only: analysis walkthrough.* After steps 1 and 2, stop and walk Simon through
the analysis: what was done and why (cohort, window, data-quality handling), which expectations
held and which were refuted, the main findings with n, and what the data cannot show. Wait for his questions before continuing. No decision is
needed here.

**Step 3: insight synthesis.** Write `outputs/03-insights.md` from 01, 02 and the constraints:

- 4–6 insights, each a section headed `## Insight N: <claim>` with: quantitative evidence,
  qualitative evidence, what it means for the decision, confidence (high/med/low) with the reason.
- `## Contradictions` and `## Open questions`.
- `## Framings`: 2–3 ways to frame the problem we solve this quarter. Per framing: the problem
  statement in one sentence, the insights it rests on, what it would lead us to build, what it
  leaves out, and the main risk.

Run the `reviewer` subagent on 03 and fix its BLOCKING findings.

**CP1: framing.** Interactive: ask Simon with AskUserQuestion, "Are these the right insights?
Which framing do we take?", one option per framing, with your recommendation first. Auto: see
below. Log the outcome in `outputs/CHECKPOINTS.md`.

**Step 4: decision memo.** Use the `decision-memo` skill to write `outputs/04-decision-memo.md`
for the chosen framing. Run the `reviewer` subagent on it and fix its BLOCKING findings.

**CP2: sign-off.** Interactive: ask Simon with AskUserQuestion, "Sign off on the recommendation,
the cut list and the metric?", with options to sign off, or to change one of the three. Auto: see
below. Log the outcome in `outputs/CHECKPOINTS.md`.

**Step 5: prototype and mail flow.** Write `outputs/05-prototype-spec.md`: the brief for building
the prototype in Claude Design. It contains:

- the flow the memo recommends, screen by screen, in order, with what the user sees and can tap;
- every message the customer receives in that flow (e-mail or other channel), with sender name,
  subject and full body copy, in German;
- the variants: with marketing consent and without it (only the service messages that
  `data/constraints.md` allows), and one full message in a non-German language the CSV shows;
- under each piece of copy, one line naming the sections of `data/constraints.md` it was checked
  against;
- a ready-to-paste prompt for Claude Design at the end.

Run the `reviewer` subagent on it and fix its BLOCKING findings. Then tell Simon the spec is ready
to paste into Claude Design and that he should put the prototype link into
`outputs/05-prototype-link.md`.

## Checkpoint log format

Append to `outputs/CHECKPOINTS.md`, one block per checkpoint:

```
## CP<n>: <date>, <interactive|auto>
Options: <short list>
Decision: <the choice>
By: <Simon | Claude (auto)>
Reason: <why>
Would change if: <what evidence would reverse it>
```

## Auto mode

No stops; nothing waits for Simon. Instead:

- **No walkthrough.** Steps 1–5 run back to back.
- **At each checkpoint, decide and log.** If `outputs/CHECKPOINTS.md` holds an earlier decision
  by Simon for this checkpoint, keep it unless the changed inputs undermine its reasoning; if so,
  say exactly which input and why. Otherwise choose by: passes `data/constraints.md`, strongest
  evidence, fits the squad this quarter, largest gap shown by the analysis, in that order.
- **Reviewer still runs.** Fix BLOCKING findings, at most two review rounds per output. List any
  findings still open at the top of that output.
- **Stamp every output** produced in auto mode with a first line: `> Auto run <date>, not signed
  off by Simon.`
- **Finish with a change report:** run `git diff --stat -- outputs/` and summarise for Simon in
  under 10 lines which outputs changed, what changed in the recommendation, and why.
