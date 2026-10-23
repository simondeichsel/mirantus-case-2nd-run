# 03 — Insight synthesis and framings

Run: interactive, 2026-10-23, fresh run. Inputs: `outputs/01-data-analysis.md`,
`outputs/01-data-interpretation.md`, `outputs/02-qual-evidence.md`, `data/constraints.md` (read
fresh this run; no earlier run to compare against, so no changed rule). All data is synthetic.
Every rate is "return within 457 days (15 months) of the first screening", cohort first screened
on or before 2025-06-30 (n=3511), unless stated otherwise. Rates are associations, not effects.

## Insight 1: Nobody records or tells the customer a next-screening interval, so "return on time" cannot be measured or acted on today

**Quantitative.** Within 15 months, 4.7% of the cohort return (n=3511) [CSV]. No return happens
before month 6. The censoring-aware (Kaplan-Meier) cumulative return is 1.8% at month 12, 4.9% at
month 15 and 6.0% at month 18 (at risk n=1472) [CSV]: returns are still accumulating after month
15. In the fully observed Q1 cohort (n=1574, returners n=105), months 14-15 hold the most returns
(n=26) and returns continue through months 15-20 [CSV]. The export has **no interval column**:
we cannot tell a late customer from one who is not yet due, and nothing longer than 637 days of
follow-up is observable [CSV].

**Qualitative.** "The report has **no** recommendation for when to come back for the next
screening." [JOURNEY] The ophthalmologist's evaluation form has no interval field; she says "I
would fill it in if it were there. It takes five seconds." [INT-04] Intervals "depend on the
person", from yearly to every 2-3 years [INT-04]. Opticians would trust a date in the report:
"Wenn im Befund steht "Nächstes Screening in 12 Monaten", dann glauben die Leute das auch." [If the
report says "Next screening in 12 months", people will believe it.] [SURVEY-6]

**For the decision.** Leadership's metric ("returned at the recommended interval") does not
exist until the interval is captured per customer. Any reminder needs a date, and that date is a
medical statement that may only come from the ophthalmologist's evaluation [CONSTRAINTS, Medical
advice]. So whatever we build first must either capture the interval or depend on it.

**Confidence: high** that no interval exists anywhere in the journey: the journey description
[JOURNEY] and the evaluating doctor [INT-04] both say so; the CSV only shows that none is
exported. **Low** on how much of the non-return is "late" versus
"not yet due".

## Insight 2: After the report, nothing prompts a return, even for customers who asked to be reminded

**Quantitative.** Customers with marketing consent return at 5.7% (n=1975) vs 3.5% without
(n=1536); the gap holds within chain and independent stores and within every result category
[CSV]. Where opticians report phoning customers, return is 8.2% (n=452) vs 4.0% with no
follow-up (n=1939); the phone association appears only among consenting customers: 11.7%
(n=273) vs 2.8% (n=179) without consent [CSV].

**Qualitative.** For unremarkable or minor results, "**no further contact** from Mirantus."
[JOURNEY] The Berlin customer ticked "I'd like reminders and offers" and "has received nothing
since the report" (note); "Honestly I'd love a reminder. Just WhatsApp me in a year. I will forget
otherwise." [INT-02] The optician could call, "aber wer soll sich das merken?" [but who is supposed
to remember that?] [INT-03]

**For the decision.** A prompt at the right time is missing, and for 54.2% of customers (n=4880)
we already have consent to send one [CSV]. The consent box promises a reminder the journey never
sends.

**Confidence: medium.** The absence of any prompt is certain [JOURNEY]. That a prompt would
*cause* returns is not shown: consenting customers self-select, and phone follow-up is
self-reported per location and rests on six independent stores and one chain store (chain cell
n=33, directional) [CSV].

## Insight 3: An unremarkable result is read as "done", and it is the largest pool of non-returners, but it may also be the group with the longest intervals

**Quantitative.** Unremarkable 3.4% (n=2428) vs minor findings 9.4% (n=742) vs referral 3.5%
(n=341) [CSV]. Unremarkable is the largest absolute gap to the best level (about 146 returns)
[CSV]. The age gradient holds within it: 60+ with an unremarkable result return at 4.9% (n=878),
18-39 at 1.8% (n=560) [CSV]. Minor findings return at nearly three times the unremarkable rate,
which fits shorter intervals; but among all returners by export (not the window cohort), their
median time to return is not shorter (384 days, n=130, vs 372 days, n=150) [CSV].

**Qualitative.** "Warum? War doch alles in Ordnung." [Why? Everything was fine.] [INT-01] "An
unremarkable result is a snapshot, not a guarantee. Patients read it as 'I'm healthy'." [INT-04]
The 67-year-old's sister has glaucoma and nobody asked (note) [INT-01]; risk factors are not asked
at the screening, so the doctor "often can't tell who should come back sooner" (note) [INT-04].
The doctor also says "It's the 'unremarkable' 60-year-olds who disappear." [INT-04] The data does
not show that: within unremarkable results, 60+ return *more* than younger customers (see above
and Contradiction 7).

**For the decision.** The biggest gap sits with customers who leave the journey believing they
are finished. The fix has to change what an unremarkable report tells them about the future,
without fear [CONSTRAINTS, Medical advice] ("If you scare people, the ones who come are the
anxious ones, not the ones at risk." [INT-04]).

**Confidence: medium** on the mechanism (doctor and customer agree). **Low** on sizing: under-40s
without risk factors may correctly be on a 2-3-year interval [INT-04], so part of this gap may be
correct behaviour.

## Insight 4: The report loses non-German speakers at the opening step, not afterwards

**Quantitative.** Non-German speakers open the report at 37.8% (n=1633) vs 71.8% for German
speakers (n=7367), across all 2025 customers [CSV]. They return at 3.3% (n=634) vs 5.0% (n=2877).
Among those who open it, the gap nearly closes: 5.3% (n=228) vs 6.1% (n=2053); among non-openers
both are 2.2% [CSV]. Non-German speakers are 18.1% of customers (n=1633) [CSV]. The absolute
return gap for the group is small (about 11 returns in the cohort) [CSV].

**Qualitative.** The report is "4 pages, in German ... in medical language" [JOURNEY]. The Berlin
customer used Google Translate and "half of it made no sense" (note); she wants it "in English and
in normal words" (note) [INT-02]. Preferred language is asked at booking and then not used
[JOURNEY]. "They are written for colleagues, honestly. Not for patients." [INT-04]

**For the decision.** Whatever we put in the report (an interval, a next date) will not reach
most non-German speakers unless the result e-mail and that part of the report speak their
language. Language belongs inside the first build, not as a separate project.

**Confidence: medium-high** on the open-rate gap; **low** that translation alone would raise
returns (no variation in report language exists in the data) [CSV].

## Insight 5: Who sends the message decides whether it is heard, and opticians will block anything that looks like Mirantus taking their customer

**Quantitative.** Independent-store customers return at 5.4% (n=1897), chain 4.2% (n=1415),
mobile units 1.5% (n=199, only n=3 returns) [CSV]. 50.2% of all 2025 customers (n=4515) are
store customers whose optician reports no follow-up at all [CSV].

**Qualitative.** The 67-year-old does not know the name Mirantus; it is "der Augen-Check bei
Herrn K." [the eye check at Mr K.'s] (note), and "Wenn Herr K. sagt, ich soll wieder kommen, dann
komm ich wieder." [If Mr K. says I should come again, then I'll come again.] [INT-01] Opticians:
"Bitte keine Mails von Mirantus an meine Kunden." [Please no e-mails from Mirantus to my
customers.] [SURVEY-4]; "The customers are mine. If someone writes to them, it's me."
(translated) [INT-03]; but "Eine automatische Erinnerung an den Kunden, aber mit unserem Logo."
[An automatic reminder to the customer, but with our logo.] [SURVEY-1] and "Wir haben keine Zeit,
Kunden anzurufen. Es muss automatisch gehen." [We don't have time to call customers. It has to be
automatic.] [SURVEY-9] "Die meisten Kunden wissen gar nicht mehr, dass sie bei uns waren, wenn der
Befund per Mail kommt. Der Befund sollte von uns kommen." [Most customers don't even remember they
were with us by the time the report comes by e-mail. The report should come from us.] [SURVEY-11]
Their motive is the glasses sale: "Interessant ist es nur, wenn danach eine Brille verkauft wird."
[It's only interesting if glasses are sold afterwards.] [SURVEY-13]

**For the decision.** Any reminder must go out in the optician's name and need no staff time
[CONSTRAINTS, The optician owns the relationship]. A Mirantus-branded reminder fails with
opticians; an optician-run phone list fails on staff time for some of them [SURVEY-9].

**Confidence: medium.** Optician positions are stated, not observed; store type is unknown for
most survey answers [SURVEY-1]-[SURVEY-15], and at chains HQ decides [SURVEY-7].

## Insight 6: The report may legally go to every customer but is opened by two in three; a reminder may go only to those with consent

**Quantitative.** Consent: 54.2% (n=4880). Report opened: 65.6% (n=5905). Consent or report
opened: 84.0% (n=7559). Neither: 16.0% (n=1441) [CSV].

**Qualitative / rules.** "Without consent, the only messages allowed are those needed to deliver
the service already bought (booking confirmation, appointment reminder, "your result is ready")."
"Consent can be asked for again later, but only in a message the customer already receives
legitimately, or in person." [CONSTRAINTS, Consent] The report PDF and e-mails can be changed this
quarter; optician CRMs cannot be integrated [CONSTRAINTS, Capacity].

**For the decision.** Legal reach and actual reach differ. The report is the one place a
doctor's next-screening recommendation can legally reach a customer without consent, but it only
reaches those who open it. A reminder at the due date can only go to consenting customers. 16.0%
(n=1441) have neither consent nor an opened report and are not reached by either [CSV]. Consent
can be asked for again in service messages (e.g. the "result ready" e-mail) or in person at the
optician's counter [CONSTRAINTS, Consent].

**Confidence: high** on reach counts and on the rules; reach is a ceiling, not an effect.

## Contradictions

1. **Who should send the reminder.** The chain customer wants it "not from the optician ... from
   whoever has my results" [INT-02]; the independent customer listens to "Herr K." [INT-01].
   Opticians reject Mirantus mail [SURVEY-4] [INT-03] but one asks for an automatic reminder "mit
   unserem Logo" [with our logo] [SURVEY-1]. Nobody was asked about the form the rules allow:
   Mirantus sends it, in the optician's name [CONSTRAINTS].
2. **One interval for everyone vs. a personal one.** One optician wants a till poster "dass man
   jährlich kommen sollte" [that you should come yearly] [SURVEY-8]; another a "Jahres-Check"
   [annual check] bundle [SURVEY-10]. The doctor says intervals depend on the person, yearly to
   every 2-3 years [INT-04]; the rules say only the doctor may set it [CONSTRAINTS, Medical
   advice]. Returns peak around months 10-15 and continue after [CSV], consistent with many
   annual intervals but unable to confirm any.
3. **Will opticians do the follow-up?** "Wir rufen dann selbst an." [We'll call them ourselves.]
   [SURVEY-3] and "A list ... Then my people can call." [INT-03] vs "Wir haben keine Zeit"
   [We don't have time] [SURVEY-9]. Phone follow-up is associated with higher return [CSV] but is
   reported by only seven locations.
4. **Do customers want reminders?** "Older customers find it pushy if you call them for
   something they didn't ask for." (translated) [INT-03] vs the 67-year-old who would return if
   her optician asked [INT-01] and the 44-year-old who wants one [INT-02]. The qualifier narrows
   the conflict: a customer who ticked the reminder box did ask.
5. **Referral customers.** The doctor worries about them less, "they're in the medical system
   now" [INT-04]; yet referral customers without consent return at 0.6% (n=154) [CSV], and the
   referred Berlin customer expects to forget the year the practice gave her [INT-02].
6. **Is there a problem?** "Our customers come back for glasses anyway" [SURVEY-2] vs 4.7%
   screening return [CSV]; a glasses visit is not a screening.
7. **Who disappears.** The doctor: "It's the 'unremarkable' 60-year-olds who disappear." [INT-04]
   The data: unremarkable 60+ return at 4.9% (n=878), above 40-59 at 3.0% (n=990) and 18-39 at
   1.8% (n=560) [CSV]. Possible reconciliation: her own guidance gives 40+ an interval of 1-2
   years [INT-04], which a 15-month window cannot judge; she may be seeing 60+ who are late on a
   yearly interval while younger ones are not yet due. Unresolved.
8. **Which channel reaches customers.** "SMS statt E-Mail. Unsere Kunden lesen keine E-Mails."
   [SMS instead of e-mail. Our customers don't read e-mails.] [SURVEY-14]; the 67-year-old reads
   e-mail "ab und zu" [now and then] (note) [INT-01]; "Just WhatsApp me" [INT-02]. Yet the
   report and e-mails are what can change this quarter [CONSTRAINTS, Capacity], and 65.6%
   (n=5905) do open the report from the e-mail [CSV].

## Open questions

1. Will evaluating ophthalmologists fill an interval field for every customer? Only one was
   heard [INT-04]. *Answerable in the 2-week test.*
2. What intervals will they give? If most are 2-3 years, the 15-month window metric undercounts
   success and the baseline must be re-cut by interval. [ASSUMPTION]
3. Would opticians who reject Mirantus mail [SURVEY-4] [INT-03] accept a reminder in their own
   name and logo that Mirantus sends? Untested.
4. Do counter bookings (most bookings at independents [JOURNEY]) capture consent and language at
   all? The CSV has both fields for every customer, so how they are filled at the counter is
   unknown.
5. Is price a barrier to repeating? Raised for pensioners [SURVEY-5] [INT-01], not for the
   younger customer [INT-02]; no data on it.
6. Mobile units: who owns the customer, and can they screen again at the right time? No source
   speaks for them [CSV shows only n=3 returns].
7. Does a reminder bring back the customers at risk, or only the engaged ones who would have
   come anyway? Needs a holdout, not this export.
8. Can the ophthalmologist's evaluation form be changed this quarter? [CONSTRAINTS, Capacity]
   names only the report PDF and e-mails as changeable. [ASSUMPTION] that the form, as Mirantus
   software feeding the report, can be.
9. Whose consent is the booking checkbox: the optician's or Mirantus's? Booking runs on "the
   optician's website or our booking page" [JOURNEY]. It decides who may send a reminder.
10. Without risk-factor questions (family history, diabetes, myopia) the doctor can rarely
    personalise an interval [INT-04]. Does the interval field need a risk question at booking?

## Framings

All three were checked against `data/constraints.md` sections Consent, Medical advice, The
optician owns the relationship, Capacity.

### Framing A (recommended): "Nobody tells the customer when to come back"

- **Problem statement:** Customers leave the screening with no next-screening date from their
  doctor, so even willing customers have nothing to act on and we have nothing to remind them of.
- **Rests on:** Insights 1, 2, 3, 6 (and 4, 5 as design requirements).
- **Would build:** an interval field in the ophthalmologist's evaluation form
  ([ASSUMPTION] that the form can change this quarter, see Open question 8); the doctor's
  recommended next screening shown on page 1 of the report only, since medical statements may only
  come from the doctor "in the report" [CONSTRAINTS, Medical advice]. The interval is a
  structured value rendered through pre-approved templates in the customer's preferred language,
  so no free medical text is translated. The "result ready" e-mail (a service message) says that
  the report contains the doctor's recommendation for the next screening, without stating it, and
  carries the optician's name; it may also ask for reminder consent again [CONSTRAINTS, Consent].
  For customers with consent, a reminder in the optician's name when the interval is due, offered
  to opticians as an opt-in tool needing no staff work [CONSTRAINTS, The optician owns the
  relationship]; stores that decline still get the in-report date, which is part of the service.
  The interval is stored per customer, which makes the core metric measurable.
- **Leaves out:** a due-list and phone tooling for opticians; full report translation and plain-
  language rewrite; SMS/WhatsApp channels; price; mobile units' specific problems.
- **Main risk:** doctors do not fill the field consistently, or give a default interval because
  risk factors are not asked [INT-04]; a date on a PDF does not move behaviour for customers
  without consent; e-mail may not reach some customers [SURVEY-14]; opticians who reject Mirantus
  mail [SURVEY-4] [INT-03] may also decline the optician-named version. The reminder half cannot
  show an effect within the quarter: the shortest interval the doctor names is yearly [INT-04].

### Framing B: "Opticians don't know who is due"

- **Problem statement:** Opticians have the relationship and a channel but no list of who is due,
  so follow-up depends on memory and spare time.
- **Rests on:** Insights 2, 5.
- **Would build:** a monthly "due for re-screening" list in the optician dashboard, optionally an
  export; opticians contact customers themselves.
- **Leaves out:** customers whose optician does nothing with the list (50.2% of all 2025
  customers, n=4515, are store customers whose optician reports no follow-up today [CSV]); mobile units; chain stores where HQ
  decides [SURVEY-7].
- **Main risk:** it relies on optician staff time, which some say they lack [SURVEY-9], and
  opticians cannot be required to do it [CONSTRAINTS]. Without a doctor's interval, "who is due"
  would be a Mirantus guess, which is a medical statement [CONSTRAINTS]. Its evidence, phone
  follow-up, rests on seven locations [CSV].

### Framing C: "The report doesn't speak the customer's language"

- **Problem statement:** The report is German medical prose behind a login, so many customers,
  above all non-German speakers, never take anything from it.
- **Rests on:** Insights 4, 3.
- **Would build:** the result e-mail and a plain-language first page in the customer's preferred
  language, with the doctor's assessment summarised.
- **Leaves out:** any trigger at the time a return is due; the interval gap; consent.
- **Main risk:** it fixes opening, not returning. Openers among non-German speakers still return
  at only 5.3% (n=228) [CSV], and the absolute gap is small (about 11 returns in the cohort) [CSV].
  Translating medical assessments also needs doctor sign-off [CONSTRAINTS, Medical advice].
