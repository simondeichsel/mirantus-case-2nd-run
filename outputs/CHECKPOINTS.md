# Checkpoint log

## CP1: 2026-10-23, interactive
Options: A "Nobody tells the customer when to come back" (interval field → next screening in report → optician-named reminder for consenting customers); B "Opticians don't know who is due" (dashboard due-list); C "The report doesn't speak the customer's language" (plain-language, translated result e-mail and first page)
Decision: A
By: Simon
Reason: The interval is missing everywhere in the journey [JOURNEY] [INT-04], so the core metric cannot exist without it and any reminder depends on it; the report reaches customers without consent; it passes Medical advice by keeping the interval the doctor's and in the report.
Would change if: evaluating ophthalmologists will not fill an interval field, or the evaluation form cannot be changed this quarter; or opticians reject even optician-named reminders.

## CP2: 2026-10-23, interactive
Options: sign off; change recommendation; change cut list; change metric
Decision: Signed off with changes to the 2-week test. Simon rejected the research-call test (not feasible with opticians, measures stated intent rather than use) and asked for a lightweight live first version instead. Then he dropped the calendar-entry button (low use among older customers, extra build effort). Final test: v0 at 4 opted-in stores = interval field in the doctor's form, next-screening block in the report, "Erinnerung per E-Mail" [e-mail reminder] opt-in in the result e-mail; measure doctor fill rate and reminder opt-ins per result e-mail. Recommendation, cut list and metric unchanged.
By: Simon
Reason: Only real use gives usable data; a reminder opt-in is the behaviour the feature depends on and collects consent at the same time. Deviates from CLAUDE.md's "test on the existing product": the v0 needs a short build first.
Would change if: legal/medical review rejects relaying the doctor's interval in reminder e-mails; doctors do not fill the interval; opt-in uptake stays low after a wording rework.

## CP2 addendum: 2026-10-23, interactive
Options: keep the step-5 spec as reviewed (all variants, Turkish example, own-domain sending as a later option); or narrow it
Decision: Narrowed. First step tests the reminder mail only, German only. Optician acceptance becomes the first gate of the test (15 opticians offered, 8 opt-ins [TARGET]). Sending stays on a Mirantus domain with the optician's name as sender; asking opticians to authorise their own domains is dropped.
By: Simon
Reason: One step at a time; whether opticians tolerate mail in their name decides everything else; domain authorisation is a hassle for opticians. Deviates from CLAUDE.md's "include one example in a non-German language": translations follow once the German reminder works.
Would change if: fewer than 8 of 15 opticians opt in (rethink who sends the reminder); legal rejects relaying the doctor's interval in a reminder.

## CP2 addendum 2: 2026-10-23, interactive
Options: (a) opt-in round with 15 opticians as a test gate; (b) Simon's proposal: "remind me" button in the existing result e-mail, click = consent, reminder from Mirantus; (c) (b) with the reminder in the optician's name, a one-time notice with opt-out for independent stores, opt-in via HQ for chains
Decision: (c), plus the doctor's recommended date in the report.
By: Simon
Reason: Fewest changes and no optician work; the click is consent asked in a message the customer already receives [CONSTRAINTS, Consent]. A Mirantus-branded reminder would break "on the optician's behalf and with the optician's name on it" [CONSTRAINTS, Relationship], which customer consent does not override. All customers with a numeric interval get the same button, whatever their booking consent.
Would change if: legal says an opt-out notice does not count as "on the optician's behalf" (then opt-in), or that a customer-requested reminder counts as "the service itself" (then Mirantus-branded is possible); optician opt-outs above 5%; click rate below 20% after a wording rework.

## CP2 addendum 3: 2026-10-23, interactive
Options: test at 4 willing stores (about n=24 result e-mails [CSV]); all independent stores after an opt-out notice (about n=183); all stores, with chains also on opt-out via HQ (about n=330)
Decision: All stores. Opt-out notice to independent stores and to chain HQs; partner manager additionally calls each chain HQ. Mobile units excluded.
By: Simon
Reason: Maximum test size without much hassle; 4 stores are too few to read a click rate. HQ decides customer communication at chains [SURVEY-7], so the notice goes there.
Would change if: legal says an opt-out notice does not count as "on the optician's behalf" or chain contracts require opt-in (then opt-in, smaller test); opt-outs above 5% [TARGET].
