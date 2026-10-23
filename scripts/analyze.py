#!/usr/bin/env python3
"""Mirantus return-rate analysis. Standard library only.

    python3 scripts/analyze.py

Reads data/screenings.csv, writes outputs/01-data-analysis.md. Every number used later in the
case must come from that file. All data is synthetic.
"""
import csv
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "screenings.csv"
OUT = ROOT / "outputs" / "01-data-analysis.md"

EXPORT = date(2026, 9, 30)
WINDOW_DAYS = 457            # primary observation window: 15 months after first screening
                             # (cohort = first screening on or before 2025-06-30)
SENSITIVITY_WINDOWS = [274, 365, 457, 548]   # 9, 12, 15, 18 months
SMALL_N = 100
MONTH = 30.4375              # average days per month, for month bucketing

lines = []


def w(s=""):
    lines.append(s)


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "n/a"


def flag(n):
    return " (directional, n<100)" if n < SMALL_N else ""


def parse_date(s):
    if not s:
        return None
    try:
        y, m, d = s.split("-")
        return date(int(y), int(m), int(d))
    except ValueError:
        return "INVALID"


# --------------------------------------------------------------------------- load
with DATA.open(encoding="utf-8") as f:
    reader = csv.DictReader(f)
    columns = reader.fieldnames
    raw = list(reader)

# --------------------------------------------------------------------------- data quality
dq = []  # (check, count, handling)
missing = {c: sum(1 for r in raw if r[c] == "") for c in columns}

ids = Counter(r["customer_id"] for r in raw)
dup_ids = sum(c - 1 for c in ids.values() if c > 1)
full_dups = len(raw) - len({tuple(r[c] for c in columns) for r in raw})

bad_first = [r for r in raw if parse_date(r["first_screening_date"]) in (None, "INVALID")]
bad_second = [r for r in raw if parse_date(r["second_screening_date"]) == "INVALID"]
first_not_2025 = [r for r in raw if isinstance(parse_date(r["first_screening_date"]), date)
                  and parse_date(r["first_screening_date"]).year != 2025]
second_before_first = []
second_same_day = []
second_after_export = []
for r in raw:
    f1, f2 = parse_date(r["first_screening_date"]), parse_date(r["second_screening_date"])
    if isinstance(f1, date) and isinstance(f2, date):
        if f2 < f1:
            second_before_first.append(r)
        elif f2 == f1:
            second_same_day.append(r)
        if f2 > EXPORT:
            second_after_export.append(r)

opened_false_with_delay = [r for r in raw if r["report_opened"] == "false"
                           and r["report_opened_days_after"] != ""]
opened_true_no_delay = [r for r in raw if r["report_opened"] == "true"
                        and r["report_opened_days_after"] == ""]
negative_delay = [r for r in raw if r["report_opened_days_after"] not in ("",)
                  and r["report_opened_days_after"].lstrip("-").isdigit()
                  and int(r["report_opened_days_after"]) < 0]
referral_field_wrong = [r for r in raw if (r["result_category"] == "referral_recommended")
                        != (r["referral_booked"] != "")]

ALLOWED = {
    "location_type": {"optician_chain", "independent_optician", "mobile_unit"},
    "optician_follow_up": {"none", "email", "phone"},
    "age_band": {"18-39", "40-59", "60+"},
    "preferred_language": {"de", "en", "tr", "ru", "ar", "pl"},
    "result_category": {"unremarkable", "minor_findings", "referral_recommended"},
    "report_opened": {"true", "false"},
    "marketing_consent": {"true", "false"},
}
bad_domain = {c: sum(1 for r in raw if r[c] not in vals) for c, vals in ALLOWED.items()}

# a location should have one type and one follow-up value
loc_types = defaultdict(set)
loc_follow = defaultdict(set)
for r in raw:
    loc_types[r["location_id"]].add(r["location_type"])
    loc_follow[r["location_id"]].add(r["optician_follow_up"])
loc_inconsistent_type = sum(1 for v in loc_types.values() if len(v) > 1)
loc_inconsistent_follow = sum(1 for v in loc_follow.values() if len(v) > 1)

# exclusion rule: drop rows whose dates make the return status unknowable
excluded_ids = {r["customer_id"] for r in bad_first + bad_second + second_before_first
                + second_after_export + first_not_2025}
seen = set()
rows = []
for r in raw:
    if r["customer_id"] in excluded_ids or r["customer_id"] in seen:
        continue
    seen.add(r["customer_id"])
    rows.append(r)

for r in rows:
    r["_f1"] = parse_date(r["first_screening_date"])
    r["_f2"] = parse_date(r["second_screening_date"])
    r["_days"] = (r["_f2"] - r["_f1"]).days if r["_f2"] else None
    r["_followup_days"] = (EXPORT - r["_f1"]).days
    r["_lang_group"] = "de" if r["preferred_language"] == "de" else "non-de"
    # report opened field is cleaned: a delay without opened=true is treated as opened=false
    r["_opened"] = r["report_opened"] == "true"
    d = r["report_opened_days_after"]
    r["_open_speed"] = ("not opened" if not r["_opened"] else
                        "opened, delay unknown" if d == "" else
                        "opened day 0-1" if int(d) <= 1 else
                        "opened day 2-3" if int(d) <= 3 else "opened day 4+")
    r["_quarter"] = f"2025-Q{(r['_f1'].month - 1) // 3 + 1}"

# --------------------------------------------------------------------------- header
w("# 01 — Data analysis (generated by `scripts/analyze.py`)")
w()
w("Generated output. Do not edit by hand; rerun `python3 scripts/analyze.py`. "
  "All data is synthetic and must not be presented as real Mirantus figures. Source for every "
  "number in this file: [CSV].")
w()
w(f"- Export date: {EXPORT.isoformat()}")
w(f"- Primary observation window: {WINDOW_DAYS} days (15 months) after the first screening")
w(f"- Small-cell threshold: cells with n<{SMALL_N} are marked directional")
w()

# --------------------------------------------------------------------------- 1 data quality
w("## 1. Data quality")
w()
f1s = [parse_date(r["first_screening_date"]) for r in raw
       if isinstance(parse_date(r["first_screening_date"]), date)]
f2s = [parse_date(r["second_screening_date"]) for r in raw
       if isinstance(parse_date(r["second_screening_date"]), date)]
w(f"- Rows in file: n={len(raw)}; columns: {len(columns)}")
w(f"- Distinct customer_id: n={len(ids)}; duplicate customer_id rows: n={dup_ids}; "
  f"fully duplicated rows: n={full_dups}")
w(f"- first_screening_date range: {min(f1s).isoformat()} to {max(f1s).isoformat()}")
if f2s:
    w(f"- second_screening_date range: {min(f2s).isoformat()} to {max(f2s).isoformat()}")
w(f"- Distinct locations: n={len(loc_types)}; locations with more than one location_type: "
  f"n={loc_inconsistent_type}; with more than one optician_follow_up value: "
  f"n={loc_inconsistent_follow}")
w()
w("### Missing values per column")
w()
w("| Column | Empty cells | Expected empty? |")
w("|---|---|---|")
expected_empty = {
    "report_opened_days_after": "yes, when report_opened = false",
    "referral_booked": "yes, unless result_category = referral_recommended",
    "second_screening_date": "yes, when no second screening yet",
}
for c in columns:
    w(f"| {c} | n={missing[c]} | {expected_empty.get(c, 'no')} |")
w()
w("### Impossible or inconsistent values")
w()
w("| Check | Rows | Handling |")
w("|---|---|---|")
checks = [
    ("Unparseable or missing first_screening_date", len(bad_first), "excluded"),
    ("Unparseable second_screening_date", len(bad_second), "excluded"),
    ("first_screening_date outside 2025", len(first_not_2025), "excluded (cohort is 2025)"),
    ("second_screening_date before first", len(second_before_first), "excluded"),
    ("second_screening_date on the same day as first", len(second_same_day),
     "kept, reported (counts as return)"),
    ("second_screening_date after export date", len(second_after_export), "excluded"),
    ("report_opened = false but a delay is given", len(opened_false_with_delay),
     "kept; treated as not opened (the flag is the primary field)"),
    ("report_opened = true but no delay", len(opened_true_no_delay),
     "kept; treated as opened, delay unknown"),
    ("Negative report_opened_days_after", len(negative_delay), "kept, reported"),
    ("referral_booked filled iff referral_recommended violated", len(referral_field_wrong),
     "kept, reported"),
]
for c, vals in bad_domain.items():
    checks.append((f"Value outside allowed set in {c}", vals, "kept, reported"))
for name, n, how in checks:
    w(f"| {name} | n={n} | {how} |")
w()
w(f"- Rows excluded in total: n={len(raw) - len(rows)}; rows kept for analysis: n={len(rows)}")
delays = Counter(r["report_opened_days_after"] for r in rows if r["report_opened_days_after"])
w(f"- Distinct values of report_opened_days_after: "
  f"{', '.join(sorted(delays, key=lambda x: int(x)))} (only these values occur)")
w()

# --------------------------------------------------------------------------- 2 cohort & window
w("## 2. Cohort, follow-up time and observation window")
w()
min_fu = min(r["_followup_days"] for r in rows)
max_fu = max(r["_followup_days"] for r in rows)
w(f"- Follow-up time from first screening to export: min {min_fu} days, max {max_fu} days")
w(f"- Every customer has had at least {min_fu} days (about {min_fu / MONTH:.1f} months) of "
  "follow-up; only customers screened early in 2025 have had 12 months or more.")
w()
by_q = Counter(r["_quarter"] for r in rows)
w("| First-screening quarter | n | Min follow-up to export (days) |")
w("|---|---|---|")
for q in sorted(by_q):
    fu = min(r["_followup_days"] for r in rows if r["_quarter"] == q)
    w(f"| {q} | n={by_q[q]} | {fu} |")
w()


def window_cohort(days):
    cutoff = EXPORT - timedelta(days=days)
    return [r for r in rows if r["_f1"] <= cutoff], cutoff


def returned_within(r, days):
    return r["_days"] is not None and r["_days"] <= days


cohort, cutoff = window_cohort(WINDOW_DAYS)
naive_ret = sum(1 for r in rows if r["_f2"])
w("### Window choice")
w()
w(f"- **Primary window: return within {WINDOW_DAYS} days of the first screening.** Cohort: "
  f"customers first screened on or before {cutoff.isoformat()}, so every included customer "
  f"has fully had {WINDOW_DAYS} days before the export. Cohort size n={len(cohort)} "
  f"(of n={len(rows)}).")
w(f"- Excluded from the primary cohort (less than {WINDOW_DAYS} days observed): "
  f"n={len(rows) - len(cohort)}")
w()
w("| Definition | Cohort | Returned | Rate |")
w("|---|---|---|---|")
w(f"| Naive: any second screening by export, all customers (NOT USED, unequal follow-up) "
  f"| n={len(rows)} | n={naive_ret} | {pct(naive_ret, len(rows))} |")
for days in SENSITIVITY_WINDOWS:
    c, cut = window_cohort(days)
    k = sum(1 for r in c if returned_within(r, days))
    tag = " (primary)" if days == WINDOW_DAYS else ""
    w(f"| Return within {days} days{tag}; first screening on or before {cut.isoformat()} "
      f"| n={len(c)} | n={k} | {pct(k, len(c))} |")
w()
prim_k = sum(1 for r in cohort if returned_within(r, WINDOW_DAYS))
prim_rate = prim_k / len(cohort)
ret_after = sum(1 for r in cohort if r["_f2"] and not returned_within(r, WINDOW_DAYS))
w(f"- Primary-cohort customers who returned after day {WINDOW_DAYS} (but before export): "
  f"n={ret_after}")
c12, _ = window_cohort(365)
k12_in = sum(1 for r in c12 if returned_within(r, 365))
k12_after = sum(1 for r in c12 if r["_f2"] and not returned_within(r, 365))
w(f"- For comparison, a 365-day window: within-window returns n={k12_in}, returns of the same "
  f"cohort after day 365 but before export n={k12_after}. A 12-month window cuts through the "
  "return peak (section 3), which is why the primary window is 15 months.")
w()

# --------------------------------------------------------------------------- 3 timing
w("## 3. Timing of returns")
w()
returners = [r for r in rows if r["_days"] is not None]
w(f"All returners by export, n={len(returners)}. Months since first screening "
  f"(days / {MONTH}, floored). Later months are only observable for early customers, so the "
  "raw histogram under-counts late returns; the censoring-aware curve below corrects for that.")
w()
hist = Counter(int(r["_days"] // MONTH) for r in returners)
w("| Month after first screening | Returns | Share of returners | Cumulative share |")
w("|---|---|---|---|")
cum = 0
for m in range(0, max(hist) + 1):
    cum += hist.get(m, 0)
    w(f"| {m}-{m + 1} | n={hist.get(m, 0)} | {pct(hist.get(m, 0), len(returners))} | "
      f"{pct(cum, len(returners))} |")
w()
q1 = [r for r in rows if r["_quarter"] == "2025-Q1"]
q1r = [r for r in q1 if r["_days"] is not None]
w(f"Same histogram for the 2025-Q1 cohort only (n={len(q1)}, every customer observed at "
  f"least {min(r['_followup_days'] for r in q1)} days, so months 0-18 are fully visible); "
  f"returners n={len(q1r)}.")
w()
w("| Month after first screening | Returns (Q1 cohort) | Share of Q1 returners |")
w("|---|---|---|")
hq = Counter(int(r["_days"] // MONTH) for r in q1r)
for m in range(0, max(hq) + 1):
    w(f"| {m}-{m + 1} | n={hq.get(m, 0)} | {pct(hq.get(m, 0), len(q1r))} |")
w()
w("Median days to return among returners, by segment (all returners by export; "
  "segments with fewer than 30 returners are marked directional):")
w()
w("| Variable | Level | Returners | Median days to return |")
w("|---|---|---|---|")
for var, key in [("result_category", lambda r: r["result_category"]),
                 ("age_band", lambda r: r["age_band"]),
                 ("marketing_consent", lambda r: r["marketing_consent"]),
                 ("optician_follow_up", lambda r: r["optician_follow_up"])]:
    g = defaultdict(list)
    for r in returners:
        g[key(r)].append(r["_days"])
    for lvl in sorted(g):
        v = sorted(g[lvl])
        mark = " (directional, fewer than 30 returners)" if len(v) < 30 else ""
        w(f"| {var} | {lvl}{mark} | n={len(v)} | {v[len(v) // 2]} |")
w()
days_sorted = sorted(r["_days"] for r in returners)
med = days_sorted[len(days_sorted) // 2]
w(f"- Median days to return among returners: {med}")
in_band = sum(1 for d in days_sorted if 335 <= d <= 395)
w(f"- Returns between day 335 and day 395 (12 months +/- about one month): n={in_band} "
  f"({pct(in_band, len(returners))} of returners)")
early = sum(1 for d in days_sorted if d < 90)
w(f"- Returns before day 90: n={early} ({pct(early, len(returners))} of returners)")
w()

# Kaplan-Meier cumulative return (1 - S(t)), censoring at export
w("### Censoring-aware cumulative return (Kaplan-Meier), all customers")
w()
events = Counter(r["_days"] for r in rows if r["_days"] is not None)
censor = Counter(r["_followup_days"] for r in rows if r["_days"] is None)
times = sorted(set(events) | set(censor))
at_risk = len(rows)
surv = 1.0
km = {}
for t in times:
    e = events.get(t, 0)
    if at_risk > 0 and e:
        surv *= (1 - e / at_risk)
    km[t] = surv
    at_risk -= e + censor.get(t, 0)


def km_at(day):
    s = 1.0
    for t in times:
        if t > day:
            break
        s = km[t]
    return 1 - s


def at_risk_at(day):
    return sum(1 for r in rows if (r["_days"] if r["_days"] is not None
                                   else r["_followup_days"]) >= day)


w("| Months after first screening | Day | Cumulative return | Customers still at risk |")
w("|---|---|---|---|")
for m in (3, 6, 9, 12, 15, 18, 21):
    d = round(m * MONTH)
    if d > max_fu:
        break
    w(f"| {m} | {d} | {100 * km_at(d):.1f}% | n={at_risk_at(d)} |")
w()

# --------------------------------------------------------------------------- 4 segments
w("## 4. Segments (primary window and cohort)")
w()
w(f"Return within {WINDOW_DAYS} days (15 months), cohort first screened on or before {cutoff.isoformat()} "
  f"(n={len(cohort)}, overall {pct(prim_k, len(cohort))}). "
  "\"Non-returners\" = customers in the cell without a return in the window. "
  "\"Gap to best level\" = returns the cell would have gained at the best level's rate "
  "within the same variable (rounded); it sizes where the gap is biggest in absolute terms. "
  "It is descriptive, not an achievable target.")
w()


def seg_table(key, label, data=None, order=None):
    data = cohort if data is None else data
    groups = defaultdict(list)
    for r in data:
        groups[key(r)].append(r)
    stats = {g: (len(v), sum(1 for r in v if returned_within(r, WINDOW_DAYS)))
             for g, v in groups.items()}
    best = max(k / n for n, k in stats.values() if n >= SMALL_N) if any(
        n >= SMALL_N for n, _ in stats.values()) else max(k / n for n, k in stats.values())
    w(f"### {label}")
    w()
    w("| Level | n | Returned | Rate | Non-returners | Gap to best level |")
    w("|---|---|---|---|---|---|")
    keys = order if order else sorted(stats)
    for g in keys:
        if g not in stats:
            continue
        n, k = stats[g]
        gap = round(n * best - k)
        w(f"| {g}{flag(n)} | n={n} | n={k} | {pct(k, n)} | n={n - k} | "
          f"{gap if gap > 0 else 0} |")
    w()
    return stats


seg_stats = {}
seg_stats["age"] = seg_table(lambda r: r["age_band"], "Age band", order=["18-39", "40-59", "60+"])
seg_stats["loc"] = seg_table(lambda r: r["location_type"], "Location type")
seg_stats["fu"] = seg_table(lambda r: r["optician_follow_up"],
                            "Optician follow-up (self-reported)",
                            order=["none", "email", "phone"])
seg_stats["consent"] = seg_table(lambda r: r["marketing_consent"], "Marketing consent")
seg_stats["result"] = seg_table(lambda r: r["result_category"], "Result category",
                                order=["unremarkable", "minor_findings",
                                       "referral_recommended"])
seg_stats["opened"] = seg_table(lambda r: "opened" if r["_opened"] else "not opened",
                                "Report opened")
seg_table(lambda r: r["_open_speed"], "Report opening speed",
          order=["opened day 0-1", "opened day 2-3", "opened day 4+",
                 "opened, delay unknown", "not opened"])
seg_stats["lang"] = seg_table(lambda r: r["preferred_language"], "Preferred language",
                              order=["de", "en", "tr", "ru", "pl", "ar"])
seg_table(lambda r: r["_lang_group"], "Preferred language (grouped)")
seg_table(lambda r: r["referral_booked"] or "(not a referral)",
          "Referral booked (referral_recommended only)",
          data=[r for r in cohort if r["result_category"] == "referral_recommended"])
seg_table(lambda r: r["_quarter"], "First-screening quarter")
seg_table(lambda r: r["city"], "City")

# robustness: key segment rates across windows
w("### Robustness: segment rates across observation windows")
w()
w("Each column uses its own cohort (customers who fully had that window). If a segment "
  "ranking holds across windows, it is less likely to be an artefact of the window choice.")
w()
w("| Variable | Level | " + " | ".join(f"{d} days" for d in SENSITIVITY_WINDOWS) + " |")
w("|---|---|" + "---|" * len(SENSITIVITY_WINDOWS))
for var, key in [("age_band", lambda r: r["age_band"]),
                 ("location_type", lambda r: r["location_type"]),
                 ("optician_follow_up", lambda r: r["optician_follow_up"]),
                 ("marketing_consent", lambda r: r["marketing_consent"]),
                 ("result_category", lambda r: r["result_category"]),
                 ("report_opened", lambda r: "opened" if r["_opened"] else "not opened"),
                 ("language", lambda r: r["_lang_group"])]:
    levels = sorted({key(r) for r in rows})
    for lvl in levels:
        cells = []
        for d in SENSITIVITY_WINDOWS:
            c, _ = window_cohort(d)
            sub = [r for r in c if key(r) == lvl]
            k = sum(1 for r in sub if returned_within(r, d))
            cells.append(f"{pct(k, len(sub))} (n={len(sub)}){flag(len(sub))}")
        w(f"| {var} | {lvl} | " + " | ".join(cells) + " |")
w()

# --------------------------------------------------------------------------- 5 confounding
w("## 5. Confounding: cross-tabulations (primary cohort)")
w()


def crosstab(rk, ck, rlabel, clabel, rorder=None, corder=None, data=None):
    data = cohort if data is None else data
    cells = defaultdict(list)
    for r in data:
        cells[(rk(r), ck(r))].append(r)
    rvals = rorder or sorted({k[0] for k in cells})
    cvals = corder or sorted({k[1] for k in cells})
    w(f"### {rlabel} x {clabel}")
    w()
    w("Cell = return rate within the window (n customers). Row share = share of the row's "
      "customers in that column.")
    w()
    w(f"| {rlabel} \\ {clabel} | " + " | ".join(cvals) + " | Row total |")
    w("|---|" + "---|" * (len(cvals) + 1))
    for rv in rvals:
        row_n = sum(len(cells.get((rv, cv), [])) for cv in cvals)
        out = []
        for cv in cvals:
            c = cells.get((rv, cv), [])
            n = len(c)
            k = sum(1 for r in c if returned_within(r, WINDOW_DAYS))
            out.append(f"{pct(k, n)} (n={n}; row share {pct(n, row_n)}){flag(n) if n else ''}")
        row_k = sum(1 for cv in cvals for r in cells.get((rv, cv), [])
                    if returned_within(r, WINDOW_DAYS))
        w(f"| {rv} | " + " | ".join(out) + f" | {pct(row_k, row_n)} (n={row_n}) |")
    w()


LOC = ["optician_chain", "independent_optician", "mobile_unit"]
FU = ["none", "email", "phone"]
crosstab(lambda r: r["optician_follow_up"], lambda r: r["location_type"],
         "follow-up", "location type", FU, LOC)
crosstab(lambda r: r["marketing_consent"], lambda r: r["location_type"],
         "consent", "location type", ["false", "true"], LOC)
crosstab(lambda r: r["optician_follow_up"], lambda r: r["marketing_consent"],
         "follow-up", "consent", FU, ["false", "true"])
crosstab(lambda r: r["_lang_group"], lambda r: "opened" if r["_opened"] else "not opened",
         "language", "report opened", ["de", "non-de"], ["opened", "not opened"])
crosstab(lambda r: r["age_band"], lambda r: r["result_category"],
         "age band", "result", ["18-39", "40-59", "60+"],
         ["unremarkable", "minor_findings", "referral_recommended"])
crosstab(lambda r: r["age_band"], lambda r: r["location_type"],
         "age band", "location type", ["18-39", "40-59", "60+"], LOC)
crosstab(lambda r: r["marketing_consent"], lambda r: "opened" if r["_opened"] else "not opened",
         "consent", "report opened", ["false", "true"], ["opened", "not opened"])
crosstab(lambda r: r["_lang_group"], lambda r: r["location_type"],
         "language", "location type", ["de", "non-de"], LOC)

# follow-up effect within location type, stratified (Mantel-Haenszel style standardisation)
w("### Follow-up association standardised to the cohort's location-type mix")
w()
w("Rate per follow-up level if each level had the overall location-type mix of the cohort "
  "(direct standardisation over location type; strata with zero customers are skipped).")
w()
loc_mix = Counter(r["location_type"] for r in cohort)
w("| Follow-up | Crude rate | Location-standardised rate | n |")
w("|---|---|---|---|")
for fu in FU:
    sub = [r for r in cohort if r["optician_follow_up"] == fu]
    crude = sum(1 for r in sub if returned_within(r, WINDOW_DAYS)) / len(sub) if sub else 0
    num = den = 0
    for loc, wgt in loc_mix.items():
        s = [r for r in sub if r["location_type"] == loc]
        if s:
            num += wgt * sum(1 for r in s if returned_within(r, WINDOW_DAYS)) / len(s)
            den += wgt
    w(f"| {fu} | {100 * crude:.1f}% | {100 * num / den:.1f}% | n={len(sub)} |")
w()

# follow-up is a location-level attribute: how many locations stand behind each cell?
w("### Locations behind each follow-up x location-type cell")
w()
w("optician_follow_up is reported per location, so the number of independent units behind a "
  "follow-up comparison is the number of locations, not customers. Cells with few locations "
  "can reflect a handful of stores. Primary cohort; per-location return rates shown as range.")
w()
w("| Follow-up | Location type | Locations | Customers | Lowest location rate | "
  "Highest location rate |")
w("|---|---|---|---|---|---|")
per_loc = defaultdict(list)
for r in cohort:
    per_loc[r["location_id"]].append(r)
for fu in FU:
    for loc in LOC:
        ids_ = [l for l, v in per_loc.items() if v[0]["optician_follow_up"] == fu
                and v[0]["location_type"] == loc]
        if not ids_:
            continue
        rates = [sum(1 for r in per_loc[l] if returned_within(r, WINDOW_DAYS)) / len(per_loc[l])
                 for l in ids_]
        nc = sum(len(per_loc[l]) for l in ids_)
        w(f"| {fu} | {loc} | {len(ids_)} | n={nc} | {100 * min(rates):.1f}% | "
          f"{100 * max(rates):.1f}% |")
w()

crosstab(lambda r: r["optician_follow_up"], lambda r: r["marketing_consent"],
         "follow-up (independent opticians only)", "consent", FU, ["false", "true"],
         data=[r for r in cohort if r["location_type"] == "independent_optician"])
crosstab(lambda r: r["result_category"], lambda r: r["marketing_consent"],
         "result", "consent", ["unremarkable", "minor_findings", "referral_recommended"],
         ["false", "true"])

# report open rate: not subject to the return window, so use all customers
w("## 5b. Report open rate by segment (all customers)")
w()
w("Opening happens within days of the screening (report_opened_days_after takes values up "
  "to 9), so all customers are used. Share of customers with report_opened = true.")
w()
w("| Variable | Level | n | Opened | Open rate |")
w("|---|---|---|---|---|")
for var, key in [("preferred_language", lambda r: r["preferred_language"]),
                 ("language group", lambda r: r["_lang_group"]),
                 ("age_band", lambda r: r["age_band"]),
                 ("location_type", lambda r: r["location_type"]),
                 ("marketing_consent", lambda r: r["marketing_consent"]),
                 ("result_category", lambda r: r["result_category"])]:
    g = defaultdict(list)
    for r in rows:
        g[key(r)].append(r)
    for lvl in sorted(g):
        n = len(g[lvl])
        k = sum(1 for r in g[lvl] if r["_opened"])
        w(f"| {var} | {lvl}{flag(n)} | n={n} | n={k} | {pct(k, n)} |")
w()
nd = [r for r in rows if r["_lang_group"] == "non-de"]
de = [r for r in rows if r["_lang_group"] == "de"]
de_open = sum(1 for r in de if r["_opened"]) / len(de)
nd_open_k = sum(1 for r in nd if r["_opened"])
w(f"- Non-German customers who would open at the German open rate: about "
  f"{round(len(nd) * de_open)} instead of {nd_open_k}, i.e. about "
  f"{round(len(nd) * de_open) - nd_open_k} more opened reports across the 2025 cohort "
  "(descriptive gap, not a forecast).")
w()

# --------------------------------------------------------------------------- 6 reach
w("## 6. Reach: who each lever could legally reach")
w()
w("Counts over all analysed customers (full 2025 cohort) and over the primary cohort. "
  "Reach is a ceiling, not an expected effect.")
w()


def reach_row(label, pred):
    a = sum(1 for r in rows if pred(r))
    b = sum(1 for r in cohort if pred(r))
    bk = sum(1 for r in cohort if pred(r) and returned_within(r, WINDOW_DAYS))
    w(f"| {label} | n={a} ({pct(a, len(rows))}) | n={b} ({pct(b, len(cohort))}) | "
      f"n={b - bk} |")


w("| Group | All 2025 customers | Primary cohort | Primary-cohort non-returners in window |")
w("|---|---|---|---|")
reach_row("All customers", lambda r: True)
reach_row("Marketing consent = true (reachable by Mirantus reminders)",
          lambda r: r["marketing_consent"] == "true")
reach_row("Marketing consent = false", lambda r: r["marketing_consent"] == "false")
reach_row("Report opened (reachable via report / in-report content)", lambda r: r["_opened"])
reach_row("Report not opened", lambda r: not r["_opened"])
reach_row("Consent and report opened", lambda r: r["marketing_consent"] == "true" and r["_opened"])
reach_row("Consent or report opened", lambda r: r["marketing_consent"] == "true" or r["_opened"])
reach_row("Neither consent nor report opened",
          lambda r: r["marketing_consent"] == "false" and not r["_opened"])
reach_row("Non-German preferred language", lambda r: r["_lang_group"] == "non-de")
reach_row("Non-German and consent", lambda r: r["_lang_group"] == "non-de"
          and r["marketing_consent"] == "true")
reach_row("Store customers (chain or independent)", lambda r: r["location_type"] != "mobile_unit")
reach_row("Store customers whose optician reports no follow-up",
          lambda r: r["location_type"] != "mobile_unit" and r["optician_follow_up"] == "none")
reach_row("Mobile-unit customers", lambda r: r["location_type"] == "mobile_unit")
reach_row("Referral recommended, referral not booked",
          lambda r: r["result_category"] == "referral_recommended"
          and r["referral_booked"] == "false")
w()

# --------------------------------------------------------------------------- 6b test sizing
w("## 6b. Test sizing: first screenings per location in 14 days")
w()
f1_all = [r["_f1"] for r in rows]
span_days = (max(f1_all) - min(f1_all)).days + 1
w(f"First screenings in 2025 spread over {span_days} days. Per location: first screenings in "
  "2025 scaled to 14 days. Customers who opened the report are the ones who can see an "
  "in-e-mail button; the open rate is the all-customer rate per location type (section 5b). "
  "Descriptive sizing for a test, not a forecast.")
w()
loc_type = {r["location_id"]: r["location_type"] for r in rows}
loc_n = Counter(r["location_id"] for r in rows)
w("| Location type | Locations | Mean first screenings per location in 14 days | "
  "Min-max per location | Report open rate |")
w("|---|---|---|---|---|")
for lt in ["independent_optician", "optician_chain", "mobile_unit"]:
    per = sorted(loc_n[l] * 14 / span_days for l in loc_n if loc_type[l] == lt)
    lt_rows = [r for r in rows if r["location_type"] == lt]
    opened = sum(1 for r in lt_rows if r["_opened"])
    w(f"| {lt} | {len(per)} | {sum(per) / len(per):.1f} | {per[0]:.1f}-{per[-1]:.1f} | "
      f"{pct(opened, len(lt_rows))} |")
w()
store_rows = [r for r in rows if r["location_type"] != "mobile_unit"]
store_locs = [l for l in loc_n if loc_type[l] != "mobile_unit"]
mean_store = len(store_rows) * 14 / span_days / len(store_locs)
store_open = sum(1 for r in store_rows if r["_opened"]) / len(store_rows)
w("Expected result e-mails and opened reports in a 14-day test, at the mean store rate "
  f"({mean_store:.1f} first screenings per store in 14 days, open rate "
  f"{pct(sum(1 for r in store_rows if r['_opened']), len(store_rows))}):")
w()
w("| Stores in test | Result e-mails (about) | Opened reports (about) |")
w("|---|---|---|")
n_indep = sum(1 for l in store_locs if loc_type[l] == "independent_optician")
for k in [4, 10, 20, n_indep, len(store_locs)]:
    label = {n_indep: f"{k} (all independent stores)",
             len(store_locs): f"{k} (all stores)"}.get(k, str(k))
    w(f"| {label} | n={round(k * mean_store)} | n={round(k * mean_store * store_open)} |")
w()

# --------------------------------------------------------------------------- 7 limits
w("## 7. What the data cannot show")
w()
w("- The export has no column for the recommended re-screening interval. Columns present: "
  + ", ".join(columns) + ".")
w("- Therefore \"returned on time\" cannot be measured per customer. The window rate above "
  "measures return within a fixed calendar window, not return relative to each customer's "
  "interval. A customer whose interval is longer than the window is counted as a non-returner "
  "in the window rate without being late.")
w(f"- The longest follow-up in the export is {max_fu} days (about {max_fu / MONTH:.1f} months). "
  "Any interval longer than that cannot be judged from this export at all; customers with "
  "such intervals are not judgeable, not non-returners.")
w("- optician_follow_up is self-reported per location by the optician, not observed per "
  "customer; whether a given customer was actually contacted is unknown.")
w("- Returns are only seen at mira locations; screenings or eye exams elsewhere are invisible.")
w("- There is no data on reminders sent by Mirantus, on what the report says, or on why "
  "customers did not return.")
w()

OUT.parent.mkdir(exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {OUT.relative_to(ROOT)} ({len(lines)} lines)")
