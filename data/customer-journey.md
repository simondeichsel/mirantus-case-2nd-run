# The customer journey today

Simplified for this case. Some details differ from the live product.

## 1. Booking

- The customer books online (on the optician's website or our booking page) or at the store
  counter. Most bookings at independent opticians happen at the counter.
- Online booking asks for name, e-mail, date of birth, preferred language, and two checkboxes:
  terms (required) and "I'd like reminders and offers" (optional, unticked by default).
- **E-mail 1 — booking confirmation:** date, time, address, what to expect, "please don't wear
  contact lenses on the day".
- **E-mail 2 — reminder:** 24 hours before the appointment.

## 2. Screening at the optician (15 min)

- An examiner (usually optician staff trained by us) runs the screening on the mira devices:
  vision test, lens assessment, retinal images, eye-pressure measurement, slit-lamp photos.
- At the end the examiner says the results will arrive by e-mail within 48 hours. Some opticians
  use the moment to show frames or contact lenses; most don't.
- The customer pays 69 € at the counter.

## 3. Evaluation and report

- An ophthalmologist evaluates the images remotely within 48 hours.
- **E-mail 3 — "Your result is ready":** a link to log in and download the report (PDF). The
  e-mail itself contains no result.
- The report is 4 pages, in German: images, measured values, the ophthalmologist's assessment in
  medical language, and — if relevant — a recommendation to see an ophthalmologist.
- The report has **no** recommendation for when to come back for the next screening.

## 4. After the report

- If a referral is recommended, the report lists partner practices nearby. The customer books
  there themselves.
- If the result is unremarkable or has minor findings: **no further contact** from Mirantus.
- Whether the optician gets in touch depends entirely on the optician (see
  `optician_follow_up` in the CSV).
