# 05 — Prototype and mail flow spec: "Erinnern Sie mich" in the result e-mail

Run: interactive, 2026-10-23. Builds the version Simon chose after CP2 (`outputs/CHECKPOINTS.md`):
the doctor enters a recommended timeframe → the report shows the recommended date → the existing
result e-mail gets an "Erinnern Sie mich" [remind me] button → the click is the customer's
consent → at the date, Mirantus sends one reminder in the optician's name. `data/constraints.md`
was read fresh for this step and is unchanged; no changed rule.

**Deviation from `CLAUDE.md`, by Simon's decision:** no non-German example. German first; one
step at a time.

Names in curly braces are **placeholders**. The prototype shows them as "Optik Muster",
"Dr. med. A. Beispiel", "Frau Muster", "Herr Beispiel". Sample domains use the reserved
`.example` domain.

Constraint sections: **Consent**, **Medical advice**, **Relationship** (= "The optician owns the
relationship"), **Capacity**.

---

## 1. The flow

| # | Screen / message | New or changed |
|---|---|---|
| D1 | Doctor's evaluation form: required timeframe field | New field |
| M1 | Existing result e-mail "Ihr Ergebnis ist da" [your result is ready], with button | Changed |
| S1 | Report PDF, page 1: one line with the recommended date | Changed |
| S2 | "Erinnerung gespeichert" [reminder saved] page after the click | New |
| M2 | The reminder mail at the date | New |
| S3 | Booking page, store pre-selected | Existing |
| S4 | Unsubscribe page | New |

**With and without marketing consent: the same flow.** Every customer with a numeric interval
gets the same M1 with the button, whether or not they ticked "I'd like reminders and offers" at
booking. Only the click counts as consent for this reminder. Reasons: it keeps one flow, and the
booking checkbox may not cover a reminder timed from the doctor's interval (health data), which
legal checks in week 0.
- **Customer clicks:** M1 → S2 → (at the date) M2 → S3.
- **Customer doesn't click:** M1 only. **No further message**, with or without booking consent.
- **Referral result** ("Gemäß Facharztpraxis") or **holdout** (20% [TARGET], memo item 6): M1
  as today, without the button.

---

## 2. Screens and messages

### D1 — Doctor's evaluation form

> **Nächstes Screening empfohlen in** ( ) 12 Monaten ( ) 24 Monaten ( ) 36 Monaten
> ( ) Gemäß Facharztpraxis (Überweisung)
> [Next screening recommended in 12 / 24 / 36 months / as set by the referral practice]

Required, no default. Mirantus computes the date: screening date + timeframe, shown as month and
year.

- *Checked against:* Medical advice (timeframe is the doctor's choice; the date is only
  arithmetic on it); Capacity ([ASSUMPTION] the form can change; fallback: a fixed line in the
  assessment text). Not customer-facing.

### M1 — Result e-mail with the button

- **From:** {Optiker} <befund@versand.mirantus.example>
- **Subject:** Ihr Ergebnis ist da – Ihr Augen-Screening bei {Optiker}
  [Your result is here – your eye screening at {optician}]

> Guten Tag {Anrede} {Nachname},
>
> Ihr Befund zu Ihrem Augen-Screening vom {Datum} ist fertig:
>
> [Befund ansehen]
>
> Im Befund finden Sie auch die Empfehlung Ihrer Augenärztin bzw. Ihres Augenarztes, wann Sie
> zum nächsten Screening kommen sollten.
>
> **Sollen wir Sie daran erinnern?** Dann schicken wir Ihnen zu dem Zeitpunkt, den Ihr Befund
> empfiehlt, eine E-Mail. Nur diese eine, keine Werbung, jederzeit abbestellbar.
>
> [Erinnern Sie mich]
>
> mira ist ein Screening und ersetzt keine augenärztliche Untersuchung.
>
> Herzliche Grüße
> Ihr Team von {Optiker}

[Hello {title} {surname}, the report on your eye screening of {date} is ready: [View report]. In
the report you'll also find your ophthalmologist's recommendation for when to come for your next
screening. **Shall we remind you?** Then we'll send you an e-mail at the time your report recommends.
Just that one, no advertising, cancel any time. [Remind me]. mira is a screening and does not replace an eye
examination by an ophthalmologist. Kind regards, your team at {optician}.]

Footer:

> Diese E-Mail wurde im Auftrag von {Optiker}, {Adresse}, von der Mirantus GmbH versendet.
> [Impressum] [Datenschutz]

- Stores that opted out (directly or via their chain HQ) and mobile units keep today's result e-mail, Mirantus-branded, without the button.
- *Checked against:* Consent (the result e-mail is a service message the customer already
  receives; asking for consent in it is allowed; scope stated: one mail, no advertising);
  Medical advice (says a recommendation exists, does not state the interval; non-replacement
  note; no fear); Relationship (optician's name as sender and sign-off, on-behalf footer; stores
  that opted out are excluded); Capacity (e-mail may change).

### S1 — Report PDF, page 1

One line, boxed, at the top of page 1:

> **Ihr nächstes Screening:** empfohlen in 12 Monaten, also ab {Monat Jahr} – Empfehlung von
> {Dr. med. Name} (Augenheilkunde).
> [**Your next screening:** recommended in 12 months, i.e. from {month year} – recommendation by
> {Dr. Name} (ophthalmology).]

Referral variant: "**Ihr nächstes Screening:** bitte mit der Augenarztpraxis besprechen, an die
Sie überwiesen wurden." [**Your next screening:** please agree it with the ophthalmology practice
you were referred to.]

- Calm layout, no red. The existing report already carries the non-replacement note.
- Template approved by the doctors and legal in week 0.
- *Checked against:* Medical advice (doctor's recommendation, in the report, doctor named; no
  fear); Relationship (no change); Capacity (report PDF may change).

### S2 — "Erinnerung gespeichert" [reminder saved]

Opens in the browser after the click. No login.

> **Erinnerung gespeichert** ✓
> Wir schicken Ihnen eine E-Mail an {E-Mail-Adresse}, wenn der Zeitpunkt erreicht ist, den Ihre
> Augenärztin bzw. Ihr Augenarzt im Befund empfohlen hat. Sie können die Erinnerung jederzeit
> abbestellen.
> [Rückgängig machen]
> [**Reminder saved.** We'll send you an e-mail at {address} when the time your ophthalmologist
> recommended in the report has come. You can cancel the reminder at any time. / Undo]

- *Checked against:* Consent (confirms what was agreed and the use of the report's date; undo
  link); Medical advice (no interval stated); Relationship (optician's name and logo in the page
  header if provided); Capacity.

### M2 — The reminder mail

Sent once, at the start of the recommended month, if: the customer clicked, the store has not
opted out, and no screening has been recorded since that report.

- **From:** {Optiker} <erinnerung@versand.mirantus.example>
- **Subject:** Ihr nächstes Augen-Screening bei {Optiker}
  [Your next eye screening at {optician}]

> Guten Tag {Anrede} {Nachname},
>
> Sie hatten uns gebeten, Sie zu erinnern: Bei Ihrem Augen-Screening am {Datum} hat Ihre
> Augenärztin bzw. Ihr Augenarzt im Befund einen Zeitpunkt für Ihr nächstes Screening
> empfohlen. Dieser Zeitpunkt ist jetzt erreicht.
>
> Die Empfehlung finden Sie in Ihrem Befund: [Befund ansehen]
>
> Einen Termin bei uns können Sie hier buchen:
>
> [Termin buchen]
>
> mira ist ein Screening und ersetzt keine augenärztliche Untersuchung.
>
> Wir freuen uns auf Sie!
> Ihr Team von {Optiker}
>
> [Erinnerung abbestellen]

[Hello {title} {surname}, you asked us to remind you: at your eye screening on {date}, your
ophthalmologist recommended a time for your next screening in the report. That time has now
come. The recommendation is in your report: [View report]. You can book an appointment with us here: [Book appointment]. mira is a screening and does
not replace an eye examination. We look forward to seeing you! Your team at {optician}.
[Unsubscribe]]

Footer as M1. One-click unsubscribe headers (RFC 8058).

- One mail, no chaser, never with offers.
- *Checked against:* Consent (only after the customer's click; unsubscribe); Medical advice
  (relays the doctor's recommendation from the report, attributed to the doctor, without stating
  an interval; [ASSUMPTION] allowed, legal confirms in week 0; non-replacement note; no fear);
  Relationship (optician's name, booking at their store, on-behalf footer; [ASSUMPTION] that the
  opt-out notice in §3 counts as "on the optician's behalf", legal confirms in week 0); Capacity
  (e-mail only).

### S3 — Booking page (existing)

Store pre-selected, next free slots, price as today. No new copy.

- *Checked against:* Relationship (booking at the customer's own store); Capacity.

### S4 — Unsubscribe

> Sie erhalten keine Erinnerung mehr. Ihr Befund bleibt in Ihrem Konto abrufbar.
> [You will no longer receive a reminder. Your report remains in your account.]

- *Checked against:* Consent (withdrawal as easy as consent); Capacity.

---

## 3. The optician side: notice and opt-out

**Independent stores:** one notice to every independent partner, before launch. No signature needed; opting
out takes one click. A store that opts out keeps today's result e-mail.

- **From:** mira Partnerbetreuung <partner@versand.mirantus.example>
- **Subject:** Neu: Erinnerung an das nächste Screening – in Ihrem Namen
  [New: reminder for the next screening – in your name]

> Guten Tag {Anrede} {Nachname},
>
> ab {Datum} kommt die Befund-E-Mail an Ihre Kundinnen und Kunden mit Ihrem Namen als Absender.
> Neu darin: Kundinnen und Kunden können auf „Erinnern Sie mich" tippen. Zum Zeitpunkt, den die Augenärztin bzw. der Augenarzt im Befund empfiehlt, erhalten
> sie dann eine E-Mail mit Ihrem Namen als Absender und einem Link, um bei Ihnen einen Termin zu
> buchen.
>
> Für Ihr Team entsteht keine Arbeit. Antworten Ihrer Kundinnen und Kunden auf diese E-Mails
> beantworten wir automatisch mit Ihrer Telefonnummer und dem Buchungslink. Um die Wirkung zu
> messen, sehen zufällig ausgewählte Kundinnen und Kunden (etwa jede fünfte) den Knopf nicht.
>
> Wenn Sie das nicht möchten: [Für mein Geschäft abbestellen]
>
> Ihr mira-Partnerteam

[Hello {title} {surname}, from {date} the result e-mail reaches your customers with your name as
sender. New in it: customers can tap "Remind me".
At the time the ophthalmologist recommends in the report, they then get an e-mail with your name
as sender and a link to book an appointment with you. No work for your team. Your customers' replies to these e-mails get an
automatic answer with your phone number and the booking link. To measure the effect, randomly
chosen customers (about one in five) don't see the button. If you don't want this: [Opt out
for my store]. Your mira partner team.]

- *Checked against:* Relationship (informs the optician and lets them refuse before anything is
  sent in their name; no required work); Capacity (no optician systems). Optician-facing.

**Chain stores:** the notice goes to chain HQ, not to the stores, because HQ decides customer
communication [SURVEY-7]. Same opt-out construction as for independent stores. In addition, the
partner manager calls each HQ before launch to walk them through it, because one HQ opt-out or
complaint affects many stores at once.

- **From:** mira Partnerbetreuung <partner@versand.mirantus.example>
- **Subject:** Neu: Erinnerung an das nächste Screening – im Namen Ihrer Filialen
  [New: reminder for the next screening – in your stores' name]

> Guten Tag {Anrede} {Nachname},
>
> ab {Datum} kommt die Befund-E-Mail an die mira-Kundinnen und -Kunden Ihrer Filialen mit dem
> Namen der jeweiligen Filiale als Absender. Neu darin: ein Knopf „Erinnern Sie mich". Zum
> Zeitpunkt, den die Augenärztin bzw. der Augenarzt im Befund empfiehlt, erhalten Kundinnen und
> Kunden, die darauf getippt haben, eine E-Mail mit einem Link, um in ihrer Filiale einen Termin
> zu buchen.
>
> Für Ihre Filialen entsteht keine Arbeit. Antworten beantworten wir automatisch mit
> Telefonnummer und Buchungslink der Filiale. Etwa jede fünfte Kundin bzw. jeder fünfte Kunde
> sieht den Knopf zufällig nicht, damit wir die Wirkung messen können.
>
> Wenn Sie das für Ihre Filialen nicht möchten: [Für alle unsere Filialen abbestellen]
>
> Ihr mira-Partnerteam

[Hello {title} {surname}, from {date} the result e-mail to your stores' mira customers carries
the store's name as sender. New in it: a "Remind me" button. Customers who tap it get an e-mail at
the time the ophthalmologist recommends in the report, with a link to book at their store. No work
for your stores. Replies get an automatic answer with the store's phone number and booking link.
About one in five customers randomly don't see the button, so we can measure the effect. If you
don't want this for your stores: [Opt out for all our stores]. Your mira partner team.]

- *Checked against:* Relationship (HQ, which decides customer communication, is informed and can
  refuse before anything is sent in the stores' name; no required work); Capacity.
  Optician-facing.

**Technical:** Mirantus sends from its own domain (SPF, DKIM, DMARC set up once by Mirantus); the
optician's name is the sender name. Nothing for the optician to configure. Reply-To is a Mirantus
address with an automatic answer. Sending from opticians' own domains is not pursued.

**Open for legal in week 0:** does an opt-out notice count as "on the optician's behalf"
[CONSTRAINTS]; who is controller or processor for M2 (Art. 26 / 28 GDPR); whether chain contracts allow an opt-out construction; whether the click
covers timing a mail from the doctor's interval (Art. 9 GDPR); whether relaying the doctor's
recommendation in M2 is allowed.

---

## 4. What the 2-week test measures

The v0 (D1, S1, M1, S2, click storage) is built before the two weeks start. Four stores would
give about n=24 result e-mails in 14 days [CSV], too few to read a click rate. So the test runs at
every store (independent and chain) that did not opt out after the week-0 notice: about n=330
result e-mails if none opt out [CSV]. Mobile units are excluded. German only. Measured:
- opt-outs after the notice, independent stores and chain HQs separately;
- share of evaluations with a timeframe (D1);
- result e-mails sent and opened, "Erinnern Sie mich" clicked, undo clicks; by age band and
  booking consent (directional at this n).

M2 is not needed during the two weeks (it fires 12+ months later) and is built after the test.
Everyone who clicks during the test gets M2, even if we stop.

---

## 5. Prompt for Claude Design

Paste this whole file into Claude Design, with this block first:

```
Build a clickable prototype of the reminder flow for "mira", an eye-screening service at
opticians, from the spec below. Use ONLY the German copy in sections 2 and 3, verbatim. Do not write any
other customer-facing text; where a label is missing, leave a grey placeholder box. The optician
notices in section 3 are the only optician-facing copy.

E-mails show the OPTICIAN's name as sender ("Optik Muster <befund@versand.mirantus.example>")
and the on-behalf footer from M1. Use only fictional placeholder values: "Optik Muster,
Musterstraße 1, Musterstadt", "Dr. med. A. Beispiel", "Frau Muster".

Tone: calm, neutral, trustworthy. No red, no alarm icons. Large readable type for older readers.
Render e-mails as phone mail-app views; S1 as a PDF page.

Start screen with three entries:
- "Kundin klickt (mit oder ohne Einwilligung bei Buchung – gleicher Ablauf)": M1 → tap "Befund ansehen" → S1 → back → tap "Erinnern Sie mich" → S2 →
  M2 (label "12 Monate später") → tap "Termin buchen" → S3
- "Kundin klickt nicht (mit oder ohne Einwilligung bei Buchung)": M1 → note "Keine weitere Nachricht."
- "Hinter den Kulissen": D1 (desktop doctor form) and both optician notices from section 3
```
