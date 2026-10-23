# Let the doctor say when to come back, and let customers ask for a reminder

## Recommendation
Add a required next-screening field to the ophthalmologist's evaluation, print the recommended date in the report, and put an "Erinnern Sie mich" [remind me] button in the existing result e-mail. A click is the customer's consent; at the date, Mirantus sends one reminder in the optician's name.

## Why this
- Nothing prompts a return: no interval in the report, no contact after, even for those who ticked "reminders" [JOURNEY] [INT-02].
- It fits the rules: the date is the doctor's, in the report; consent is asked in a message the customer already receives; the reminder carries the optician's name, pending legal [CONSTRAINTS].

## What ships first
1. Required interval field (12/24/36 months [INT-04], "per referral practice"): "It takes five seconds." [INT-04]; [ASSUMPTION] the form can change, else a fixed assessment-text line.
2. Report: one line with the doctor's recommended date.
3. Result e-mail, now in the optician's name: "Erinnern Sie mich" button (not for referrals, holdout, opted-out stores, mobile units); says the report holds the recommendation, without stating it.
4. Reminder at the date: Mirantus domain, optician's name as sender, booking link to the store.
5. Partners: one-time notice with opt-out to independent stores and chain HQs [SURVEY-7], plus a call to each HQ.
6. Date stored; 20% see no button [TARGET].

## Cut, and why
- Optician opt-in round, opticians' own domains: optician effort.
- Mirantus-branded reminder: breaks "on the optician's behalf" [CONSTRAINTS]; opticians object [SURVEY-4] [INT-03].
- Calendar, SMS/WhatsApp, translations, risk questions, mobile units: later.
- Optician due-list: phone follow-up is associated with 8.2% (n=452) [CSV], but self-reported, few stores, and needs staff time [SURVEY-9].

## Trade-off
Only clickers get reminded; non-German speakers open the German e-mail less (37.8%, n=1633, vs 71.8%, n=7367) [CSV]. Effects show 15 months after launch; no optician work in return.

## Success metric
- **Name:** On-time return rate
- **Definition:** customers screened again at any mira location by interval + 3 months (early counts) / customers whose interval + 3 months has passed
- **Cohort:** first screenings from launch with a numeric interval, per interval
- **Window:** interval + 3 months [TARGET], as returns spread around the peak [CSV]; first readout at launch + 15 months, directional
- **Baseline:** proxy 4.7% within 15 months (n=3511) [CSV]; true baseline: the no-button group.
- **Target:** 12-month group, button vs no button: +2pp [TARGET]. Low confidence: optician e-mail follow-up: 4.6% (n=1120) vs none 4.0% (n=1939) [CSV]. Leading indicators: interval on 90% of evaluations [TARGET]; 20% of result-e-mail recipients click [TARGET].

## Guardrails
- Report turnaround within 48 hours [JOURNEY].
- Report open rate at least 65.6% (n=9000) [CSV].
- Optician opt-outs or reminder unsubscribes above 5% pause reminders [TARGET].
- Interval mix by age and result, monthly: no defaulting [INT-04].

## 2-week test with real users
Live v0 (items 1–3 plus click storage), German only, built before the two weeks start. Four stores give about n=24 result e-mails [CSV]: too few, so we use all stores.
- **Week 0:** opt-out notice to all partners (chains via HQ); doctors and legal approve copy; legal confirms the notice counts as "on the optician's behalf", else opt-in [ASSUMPTION].
- **Weeks 1–2:** live at every store that didn't opt out: about n=330 result e-mails [CSV]. Age and consent splits are directional.
- **Decision rule:** roll out if opt-outs stay below 5% [TARGET], doctors fill 90% [TARGET] and 20% of recipients click [TARGET]. Few clicks: rework wording. Doctors won't fill: stop. Clickers get their reminder regardless.
