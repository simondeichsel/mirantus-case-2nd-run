# Mirantus Product Case Study: Make prevention a habit

Thanks for taking the time. This case is part of our hiring process for the
[Senior Product Manager](https://www.mirantus.com/en/careers/senior-product-manager) role.

**The short version:** you have 2 hours. Don't do the product work yourself — set Claude up so
that it does the product work well, and judge what comes out. Afterwards we review it together
with you for 30 minutes, followed by our regular interview.

## Context

Mirantus brings eye screenings to where people already go: the optician. With our platform
**mira**, an examiner at the optician runs a 15-minute screening (vision, retinal images, eye
pressure, slit-lamp photos). An ophthalmologist evaluates the results remotely within 48 hours,
and the customer receives a report. mira runs at 350+ locations with 450+ physician partners and
has screened over 25,000 customers.

Most customers come once. Eye diseases like glaucoma progress silently, so prevention only works
if people come back regularly. For the optician, a returning customer is also a returning store
visit.

## The problem

Only a small share of screened customers come back for a second screening. Leadership wants the
return rate to become a core product metric. You own this problem.

## Your data pack

Everything in `data/` is **synthetic**. It is realistic in shape, but no number in it is a real
Mirantus figure, and no person in it exists.

| File | What it is |
|---|---|
| [`data/screenings.csv`](data/screenings.csv) | 9,000 customers first screened in 2025, exported on 30.09.2026. Columns explained in [`data/README.md`](data/README.md) |
| [`data/interviews/`](data/interviews/) | 4 interview notes: 2 customers, 1 optician, 1 ophthalmologist. Messy, partly contradictory, partly German |
| [`data/optician-survey.md`](data/optician-survey.md) | 15 free-text answers from a partner survey |
| [`data/customer-journey.md`](data/customer-journey.md) | What a customer experiences today, step by step, including every e-mail |
| [`data/constraints.md`](data/constraints.md) | Consent rules, what counts as medical advice, who owns the customer relationship |

## Your task (max. 2 hours)

Your job is not to do the product work yourself. Your job is to set Claude up so it does the
product work well, and to judge what comes out. The times are a guide.

1. **Brief Claude (~30 min).** Write the context Claude works from, e.g. a `CLAUDE.md`: the goal,
   the users, the constraints, what good looks like, and what Claude must never do.
2. **Design the run (~30 min).** Split the work into steps — for example data analysis, interview
   synthesis, problem framing, prototype, memo. Use subagents, skills, a workflow, whatever you
   think fits. Decide where Claude checks its own work and where it stops to ask you.
3. **Let it run (~40 min).** Claude should produce:
   - an insight synthesis grounded in the data pack,
   - a decision memo (max. 1 page): the recommendation, what ships first and what is cut, the
     success metric and its guardrails, and how to test with real users in the next two weeks,
   - a clickable prototype in Claude Design of the one flow that matters most.

   Step in only at your checkpoints.
4. **Review and sign off (~20 min).** Write your own verdict (max. half a page): what you would
   keep, where Claude went wrong, and what you would change in the setup next time. Write this
   part yourself.

**Make it rerunnable.** Add a short README saying how to run it again. In the review session we
will change one input and ask you to rerun it live.

A clear setup with good checkpoints beats a big one. A narrow, well-argued recommendation beats a
full product vision.

## Tools

- **Claude Code** for the setup and the run, **Claude Design** for the prototype. A Claude Pro
  account covers both. If you don't have one, tell us and we'll give you a temporary seat for
  7 days.
- Keep your Claude Code session going while you work, and export it at the end with `/export`.
- Other tools are fine, but we look at how you work with Claude.

## How to submit

At least 24 hours before your review session, send us a link to **your own** repository (public,
or private with access for us). Please don't open pull requests or issues here. It should contain:

- [ ] your setup: `CLAUDE.md`, agents, skills or workflow files, and a README on how to rerun it
- [ ] what the run produced: insight synthesis, decision memo, prototype link
- [ ] the exported Claude Code transcript
- [ ] your own verdict (max. half a page)

Stop at 2 hours. If you ran out of time, write down what you would have done next — that counts
too.

## The review session (30 minutes)

- **Walkthrough (8 min):** show us your setup, then what it produced. No slides.
- **Live rerun (15 min):** we change one input; you adjust your setup and rerun the steps it
  affects, sharing your screen.
- **Deep-dive (7 min):** a couple of questions on your transcript and your verdict.

Our regular interview follows directly — that's where your own questions have room.

Questions before you start? Reply to your invitation e-mail.
