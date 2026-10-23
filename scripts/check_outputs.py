#!/usr/bin/env python3
"""Deterministic checks on the Mirantus case outputs, and staleness tracking.

    python3 scripts/check_outputs.py            check every output that exists
    python3 scripts/check_outputs.py --stale    list steps whose inputs changed since last run
    python3 scripts/check_outputs.py --record N record step N's inputs as the current state

Exit code 1 if any check fails.
"""
import glob
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
MANIFEST = OUT / ".manifest.json"

EXPECTATIONS = OUT / "01-expectations.md"
ANALYSIS = OUT / "01-data-analysis.md"
INTERPRETATION = OUT / "01-data-interpretation.md"
QUAL = OUT / "02-qual-evidence.md"
INSIGHTS = OUT / "03-insights.md"
MEMO = OUT / "04-decision-memo.md"
PROTOTYPE = OUT / "05-prototype-spec.md"

# Inputs each step reads. Upstream outputs are inputs too, so a change propagates.
STEP_INPUTS = {
    1: ["data/screenings.csv", "data/README.md", "scripts/analyze.py"],
    2: ["data/interviews/*.md", "data/optician-survey.md", "data/customer-journey.md"],
    3: ["outputs/01-data-analysis.md", "outputs/01-data-interpretation.md",
        "outputs/02-qual-evidence.md", "data/constraints.md"],
    4: ["outputs/03-insights.md", "data/constraints.md"],
    5: ["outputs/04-decision-memo.md", "data/customer-journey.md", "data/constraints.md"],
}
DOWNSTREAM = {1: [3], 2: [3], 3: [4], 4: [5], 5: []}

MEMO_WORD_LIMIT = 600

# Fear phrases (EN/DE). Checked in the memo and in customer-facing copy.
FEAR = [r"\bgo(ing)? blind", r"\bblindness", r"lose your (sight|vision)", r"too late",
        r"erblind", r"zu spät", r"augenlicht verlieren", r"sehkraft verlieren"]

failures = []


def fail(msg):
    failures.append(msg)


def text(path):
    return path.read_text(encoding="utf-8") if path.exists() else None


# --- staleness -------------------------------------------------------------

def input_files(step):
    files = []
    for pattern in STEP_INPUTS[step]:
        files += sorted(glob.glob(str(ROOT / pattern)))
    return files


def fingerprint(step):
    return {str(Path(f).relative_to(ROOT)): hashlib.sha256(Path(f).read_bytes()).hexdigest()
            for f in input_files(step)}


def load_manifest():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def record(step):
    manifest = load_manifest()
    manifest[str(step)] = fingerprint(step)
    OUT.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    print(f"Recorded inputs of step {step}.")


def stale():
    manifest = load_manifest()
    direct = {}
    for step in STEP_INPUTS:
        recorded = manifest.get(str(step))
        if recorded is None:
            direct[step] = ["never recorded"]
            continue
        current = fingerprint(step)
        changed = [f for f in sorted(set(recorded) | set(current))
                   if recorded.get(f) != current.get(f)]
        if changed:
            direct[step] = changed
    out_of_date = set(direct)
    queue = list(direct)
    while queue:
        for nxt in DOWNSTREAM[queue.pop()]:
            if nxt not in out_of_date:
                out_of_date.add(nxt)
                queue.append(nxt)
    if not out_of_date:
        print("All steps up to date.")
        return
    for step in sorted(out_of_date):
        reason = ", ".join(direct[step]) if step in direct else "an upstream step is out of date"
        print(f"Step {step} out of date: {reason}")
    print(f"Rerun from step {min(out_of_date)}: /run-case {min(out_of_date)}")


# --- content checks --------------------------------------------------------

def valid_tag_pattern():
    interviews = len(glob.glob(str(ROOT / "data/interviews/*.md")))
    survey = text(ROOT / "data/optician-survey.md") or ""
    answers = len(re.findall(r"^\d+\.", survey, re.M))
    return interviews, answers


def check_tags(path, body):
    interviews, answers = valid_tag_pattern()
    for n in re.findall(r"\[INT-(\d+)\]", body):
        if not 1 <= int(n) <= interviews:
            fail(f"{path.name}: tag [INT-{n}] but there are {interviews} interviews")
    for n in re.findall(r"\[SURVEY-(\d+)\]", body):
        if not 1 <= int(n) <= answers:
            fail(f"{path.name}: tag [SURVEY-{n}] but the survey has {answers} answers")


def normalise(s):
    return s.replace(" ", " ").replace(" %", "%").replace(" pp", "pp")


NUMBER = re.compile(r"\d+(?:\.\d+)?(?:%|pp)|\bn\s?=\s?[\d,]+")
EXEMPT = re.compile(r"\[(TARGET|ASSUMPTION)\]")


def numbers(body):
    """Rates, percentage-point differences and n= counts: the numbers that must be sourced.

    A number is exempt only if [TARGET] or [ASSUMPTION] follows it before the next number.
    """
    found = []
    for line in normalise(body).splitlines():
        matches = list(NUMBER.finditer(line))
        for i, m in enumerate(matches):
            end = matches[i + 1].start() if i + 1 < len(matches) else len(line)
            if EXEMPT.search(line, m.end(), end):
                continue
            num = m.group()
            found.append("n=" + re.sub(r"\D", "", num) if num.startswith("n") else num)
    return found


def check_numbers(path, body, source):
    source_text = normalise(source).replace(",", "")
    source_text = re.sub(r"\bn\s?=\s?", "n=", source_text)
    for num in sorted(set(numbers(body))):
        if num.replace(",", "") not in source_text:
            fail(f"{path.name}: number {num} not found in 01-data-analysis.md")


def check_fear(path, body):
    for pattern in FEAR:
        if re.search(pattern, body, re.I):
            fail(f"{path.name}: fear phrase matching '{pattern}'")


def check():
    analysis = text(ANALYSIS)
    for path in [INTERPRETATION, QUAL, INSIGHTS, MEMO, PROTOTYPE]:
        body = text(path)
        if body is None:
            continue
        check_tags(path, body)
        if path != QUAL:
            if analysis is None:
                fail(f"{path.name}: exists but 01-data-analysis.md does not")
            else:
                check_numbers(path, body, analysis)

    interpretation = text(INTERPRETATION)
    if interpretation is not None:
        if not EXPECTATIONS.exists():
            fail("01-data-interpretation.md exists but 01-expectations.md does not")
        if "## Expectations vs. findings" not in interpretation:
            fail("01-data-interpretation.md: missing section '## Expectations vs. findings'")

    insights = text(INSIGHTS)
    if insights is not None:
        sections = re.split(r"^## ", insights, flags=re.M)
        found = [s for s in sections if s.startswith("Insight")]
        if not 4 <= len(found) <= 6:
            fail(f"03-insights.md: {len(found)} insights, expected 4-6")
        for s in found:
            if not re.search(r"\[(CSV|INT-\d+|SURVEY-\d+|JOURNEY|CONSTRAINTS)\]", s):
                fail(f"03-insights.md: '{s.splitlines()[0]}' has no source tag")
        for heading in ["Contradictions", "Open questions", "Framings"]:
            if f"## {heading}" not in insights:
                fail(f"03-insights.md: missing section '## {heading}'")

    memo = text(MEMO)
    if memo is not None:
        words = len(re.sub(r"<!--.*?-->", "", memo, flags=re.S).split())
        if words > MEMO_WORD_LIMIT:
            fail(f"04-decision-memo.md: {words} words, limit {MEMO_WORD_LIMIT}")
        for heading in ["Recommendation", "What ships first", "Cut", "Success metric",
                        "Guardrails", "2-week test"]:
            if not re.search(rf"^## {heading}", memo, re.M):
                fail(f"04-decision-memo.md: missing section '## {heading}'")
        check_fear(MEMO, memo)

    prototype = text(PROTOTYPE)
    if prototype is not None:
        check_fear(PROTOTYPE, prototype)

    if failures:
        print("FAIL")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("OK: all checks passed for the outputs that exist.")


if __name__ == "__main__":
    if "--record" in sys.argv:
        record(int(sys.argv[sys.argv.index("--record") + 1]))
    elif "--stale" in sys.argv:
        stale()
    else:
        check()
