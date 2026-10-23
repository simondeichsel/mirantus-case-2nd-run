# 01 — Expectations (written before seeing the data)

Run: interactive, 2026-10-23, fresh run. Written after reading only `data/README.md` and the
header line of `data/screenings.csv`. No data row had been read and no script had been run.
These are hypotheses, not findings; all are `[ASSUMPTION]`.

## Expectations

- **E1 — Return is low overall and mostly not yet due.** I expect only a minority of customers
  to have returned within any window the export can fully observe, because a typical
  recommended interval for an unremarkable screening is probably one to two years or longer, and
  the export only covers up to about 21 months after the earliest first screening.
- **E2 — Returns cluster around twelve months.** I expect months-to-return to peak around
  month 12, because annual check-ups are the cultural default for eye exams and many customers
  likely received a one-year interval or simply anchor on "once a year".
- **E3 — Older customers return more.** I expect the 60+ band to return at a higher rate than
  18-39, because older customers are more likely to have findings, shorter intervals and a
  stronger health motive, and are more used to regular check-ups.
- **E4 — Result category drives return.** I expect `minor_findings` to return more than
  `unremarkable`, because "worth watching" implies a shorter interval and a reason to come back;
  I expect `referral_recommended` customers to return to mira *less*, because their next contact
  is the partner ophthalmologist, not a screening.
- **E5 — Mobile units return least.** I expect `mobile_unit` customers to return at a clearly
  lower rate than store customers, because the bus is a one-off encounter with no store to walk
  back into and no optician who "owns" the customer.
- **E6 — Optician follow-up is associated with return, but confounded.** I expect `phone` >
  `email` > `none`, because active contact reminds customers; but I expect follow-up to be
  concentrated in stores (and absent in mobile units), so much of the raw gap will shrink once
  location type is held constant.
- **E7 — Marketing consent is associated with higher return.** I expect consenting customers to
  return more, because they are the ones who can receive reminders and they are self-selected as
  more engaged. This also caps the reach of any reminder lever to the consenting share.
- **E8 — Non-German speakers return less and open the report less.** I expect customers with
  `preferred_language` other than `de` to have lower report-open and return rates, because the
  report is German only (`data/README.md`), so the result and its implied interval may not be
  understood.
- **E9 — Opening the report is associated with return.** I expect customers who opened the report
  (and opened it quickly) to return more, because the report is where they learn their result
  and, presumably, when to come back.

## Questions I most want the data to answer

1. What share of customers return within a window that every customer has fully had, and how
   different is that from the naive rate?
2. When do returns happen — is there a peak, and at what month?
3. Does the data contain each customer's recommended interval? If not, how can "returned on
   time" be measured at all?
4. Where is the gap biggest in absolute missing returns (n times rate gap), not just in rate?
5. How much of the follow-up and consent association survives within location type?
6. How many customers could each lever legally reach (consent, opened report, language)?
7. Are there data-quality problems (duplicates, impossible dates, inconsistent report fields)
   that change any of the above?
