# `screenings.csv` — data dictionary

Synthetic export. One row per customer whose **first** screening took place in 2025.
Export date: **30.09.2026**. Second screenings are only visible up to that date.

| Column | Meaning |
|---|---|
| `customer_id` | Pseudonymous customer ID |
| `location_id` | Where the first screening took place |
| `location_type` | `optician_chain`, `independent_optician` or `mobile_unit` (a screening bus visiting companies and town squares) |
| `city` | City of the location |
| `optician_follow_up` | What the location does after a screening on its own initiative: `none`, `email`, `phone`. Self-reported by the optician in a partner survey |
| `first_screening_date` | Date of the first screening (YYYY-MM-DD) |
| `age_band` | `18-39`, `40-59`, `60+` |
| `preferred_language` | Language chosen at booking (`de`, `en`, `tr`, `ru`, `ar`, `pl`). The report is currently German only |
| `result_category` | Ophthalmologist's evaluation: `unremarkable`, `minor_findings` (no referral, but worth watching), `referral_recommended` |
| `report_opened` | Whether the customer opened the result report at least once |
| `report_opened_days_after` | Days between report available and first open; empty if never opened |
| `marketing_consent` | Whether the customer agreed at booking to be contacted for reminders and offers |
| `referral_booked` | Only for `referral_recommended`: whether an appointment at a partner practice was booked. Empty otherwise |
| `second_screening_date` | Date of the next screening at any mira location; empty if none yet |
