---
name: decision-memo
description: Template and rules for the one-page Mirantus decision memo (outputs/04-decision-memo.md). Use when drafting or revising the memo.
---

# Decision memo

Max. 1 page: about 500 words, hard limit 600 (checked by `scripts/check_outputs.py`). Every
claim is tagged. Every number comes from `outputs/01-data-analysis.md`; a target is a decision, not
data, so tag it `[TARGET]`. Write for a leadership reader who has not seen the analysis.

The memo argues for **one** recommendation. If you find yourself recommending two things, one of
them goes into the cut list.

## Template

```markdown
# <Recommendation as a short imperative sentence>

<If an input changed since the last run: one line naming the changed rule and what it changes.>

## Recommendation
2–3 sentences: what we build, for whom, and why it moves the return rate.

## Why this
3 bullets. The insight, the evidence (tags), and why this beats the strongest alternative.

## What ships first
What the squad builds this quarter, in the order it ships. Each item fits the capacity in
`data/constraints.md` and names who does any work (it is never the optician unless optional).

## Cut, and why
The alternatives we are not doing now, one line each with the reason.

## Trade-off
One or two sentences: what we give up by choosing this.

## Success metric
- **Name:**
- **Definition:** numerator / denominator
- **Cohort:** which customers, from when
- **Window:** how long after the first screening, and why this window
- **Baseline:** from the analysis, with n
- **Target:** [TARGET], and why this target is plausible

## Guardrails
2–4 things that must not get worse, each with how we measure it.

## 2-week test with real users
Who (how many, which locations), what they see, what we measure, and the decision rule: what
result makes us continue, change, or stop. It runs on the existing product, without waiting for
the full build.
```
