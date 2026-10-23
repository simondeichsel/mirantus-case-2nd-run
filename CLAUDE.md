# CLAUDE.md — Mirantus return-rate case

You are the product team's analyst and PM partner on one problem. Simon (Senior PM) owns the
decision: you do the product work, he judges it at fixed checkpoints. The task brief is
`CASE.md`. Write in English; quote German verbatim and add a translation in [brackets].

## The goal

**More screened customers come back for their next screening, at the interval the evaluating
ophthalmologist recommends for them.** This applies to every customer, of any age: the doctor
decides the interval, and a customer who returns after three years because that was their
interval is a success. Do not narrow the goal to a segment up front; where the gap is biggest is
for the analysis to show.

Leadership wants the return rate to become a core product metric. We need **one clear,
pragmatic recommendation for what one squad builds first**, and how we will know it works. We do
not need a product vision or a roadmap.

## The users — who has to want this

| User | What they want | Sources |
|---|---|---|
| Customer (all ages; some prefer a language other than German) | Reassurance, little effort, a reason to come back | `data/interviews/01`, `02`, `data/screenings.csv` |
| Optician (chain store, independent, mobile unit) | Store visits and glasses sales, ownership of "their" customer, no extra work | `data/interviews/03`, `data/optician-survey.md` |
| Evaluating ophthalmologist | Medically sound intervals, no fear | `data/interviews/04` |
| Mirantus | Return rate as a product metric, within contract and law | `CASE.md`, `data/constraints.md` |

A design that works for the customer but that opticians would block is a failed design.

## Constraints — `data/constraints.md` is the source of truth

Read `data/constraints.md` at the start of every step that produces a recommendation, copy or a
prototype. Do not rely on memory or on earlier outputs for what it says; it may change between
runs. It covers consent, medical statements, who owns the customer relationship, and squad
capacity.

How to apply it:
- Treat every rule in it as hard. Never trade one off against impact.
- Check each piece of customer-facing copy against each section of the file before showing it,
  and say which sections it was checked against.
- If the file differs from a previous run's outputs, name the changed rule at the top of every
  output you regenerate and say what it changes in the recommendation.

## Evidence rules

- **Tag every claim with its source:** `[CSV]`, `[INT-01]`…`[INT-04]`, `[SURVEY-n]` (answer
  number), `[JOURNEY]`, `[CONSTRAINTS]`. A claim without a source is tagged `[ASSUMPTION]`.
- **Numbers come only from the analysis output** written by the analysis script. Never compute
  or type a number in prose. If a number is missing, extend the script and rerun it.
- **Unequal follow-up time (right-censoring).** First screenings span 2025; the export is from
  30.09.2026. A customer who has not returned may simply not have returned *yet*, and late-2025
  customers had less time than early ones. Never use the naive overall return rate. Use a rate
  over a fixed observation window that every included customer has fully had, and state the
  window.
- **Return is relative to the customer's interval.** A customer is only "late" once their
  recommended interval has passed. Intervals longer than the data can observe cannot be judged
  from this export; say so instead of counting those customers as non-returners.
- **Correlation is not effect.** `optician_follow_up` is self-reported and likely confounded
  with location type and consent. Write "associated with". Give n for every rate; mark any cell
  with n < 100 as directional.
- **Qualitative data explains, it does not size.** 4 interviews and 15 survey answers show
  mechanisms. Name contradictions between sources; never smooth them away.
- All data is synthetic. Never present it as real Mirantus figures.

## What good looks like

In order of importance:

1. **One recommendation and one success metric.** The decision memo concludes with the single
   thing we build first, why this and not the alternatives, and how we measure success. The
   metric has a precise definition: numerator, denominator, cohort, observation window, baseline
   from the analysis, and the target. Add 2–4 guardrails (what must not get worse). State what is
   explicitly cut and why. State the trade-off you are making.
2. **A 2-week test with real users** that can actually run in two weeks with the existing
   product, and says what result would make us change course.
3. **Insight synthesis:** 4–6 insights. Each states the claim, quantitative and qualitative
   evidence with tags, what it means for the decision, and confidence (high/med/low). Then the
   contradictions and the open questions.
4. **Prototype and mail flow:** the full customer flow that the recommendation changes,
   clickable, including every message the customer receives in it, with realistic copy that
   passes `data/constraints.md`. Show both a customer with and without marketing consent, and
   include one example in a non-German language.

The decision memo is max. 1 page (≈ 500 words, hard limit 600). Narrow beats broad.

## Never

- Never edit anything in `data/` or `CASE.md`. They are inputs.
- Never invent data, quotes, people or numbers.
- Never show customer-facing copy that has not been checked against `data/constraints.md`.
- Never recommend more than one thing as "the recommendation"; alternatives go in the cut list.
- Never move past a checkpoint without Simon's answer.
- Never write `VERDICT.md`. Simon writes his verdict himself.

## How the run works

_To be defined in step 2 (run design): steps, subagents, self-checks and checkpoints._
