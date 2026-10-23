# 05 — Prototype link

Clickable prototype built in Claude Design from `outputs/05-prototype-spec.md`:

https://claude.ai/artifact/8wBLJEkrTmcss84XVczp83

## Check against the spec (2026-10-23)

The prototype's copy was extracted and compared with `outputs/05-prototype-spec.md`:

- All customer-facing copy (result e-mail M1, report line S1 incl. referral variant, "Erinnerung
  gespeichert" S2, reminder mail M2, unsubscribe S4) and both optician notices match the spec
  word for word, including sender names, `.example` addresses and the on-behalf footer.
- Doctor form D1: required, no option pre-selected; the date is computed from the doctor's choice.
- Referral results show no button; the "showButton" switch demonstrates the holdout.
- No fear wording; non-replacement note present in both e-mails.
- Click paths match the spec, labelled "mit oder ohne Einwilligung bei Buchung – gleicher Ablauf".

Minor, not blocking: the optician notice uses a sample date ("ab 1.12.2026"), and the opt-out
button in the notices does nothing (prototype only).
