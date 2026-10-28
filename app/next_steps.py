"""Decides what to show: flagged markers, retest status and which tests to suggest."""
import operator
from datetime import timedelta
from decimal import Decimal

from app.cleaning import CleanRecord, Measurement
from app.config import BANDS, RETEST, TESTS, Test
from app.markers import MARKERS, Marker

_COMPARE = {"le": operator.le, "lt": operator.lt, "ge": operator.ge, "gt": operator.gt}
_STATUS_PRIORITY = {"needs_attention": 0, "moderate": 1}


def grade(marker: Marker, value: Decimal) -> str:
    """'optimal', 'moderate' or 'needs_attention'. LDL 2.9 isn't <= 2.6 but is <= 3.4: moderate."""
    for band in ("optimal", "moderate"):
        limits = BANDS[marker.key][band]
        if all(_COMPARE[op](value, limit) for op, limit in limits.items()):
            return band
    return "needs_attention"


def retest_status(record: CleanRecord) -> dict:
    today = record.member.today
    due = record.member.membership.retest_due
    window_opens = due - timedelta(days=RETEST.early_retest_days)

    if any(r.counts_as_retest and r.date >= window_opens for r in record.member.reports):
        return {"status": "done", "due": due}
    if today > due:
        return {"status": "overdue", "due": due, "days_overdue": (today - due).days}
    if (due - today).days <= RETEST.due_soon_days:
        return {"status": "due_soon", "due": due, "days_until_due": (due - today).days}
    return {"status": "not_due", "due": due}


def suggest_tests(flagged: list[str], retest: dict) -> list[dict]:
    """The retest first if it's due, then one test for each flagged marker it doesn't cover."""
    suggestions = []
    if retest["status"] in ("overdue", "due_soon"):
        suggestions.append(_suggestion(TESTS[RETEST.test], f"retest_{retest['status']}", flagged))
    covered = {key for s in suggestions for key in s["markers"]}
    for key in flagged:
        if key not in covered:
            suggestions.append(_suggestion(_follow_up_test(key), "flagged", flagged))
    return suggestions


def build_next_steps(record: CleanRecord, preferred_name: str) -> dict:
    flags, not_assessed = [], []
    for marker in MARKERS.values():
        latest = record.latest(marker)
        if latest is None:
            continue
        if not latest.usable:
            not_assessed.append({"marker": marker.key, "name": marker.name, "reason": latest.problem})
            continue
        status = grade(marker, latest.value)
        if status != "optimal":
            flags.append(_flag(record, marker, latest, status))
    flags.sort(key=lambda f: _STATUS_PRIORITY[f["status"]])  # sort is stable, so marker order holds

    retest = retest_status(record)
    suggestions = suggest_tests([f["marker"] for f in flags], retest)
    for flag in flags:
        flag["suggested_test"] = next(s["test"] for s in suggestions if flag["marker"] in s["markers"])

    return {
        "member": {"preferred_name": preferred_name},
        "as_of": record.member.today,
        "retest": retest,
        "flags": flags,
        "not_assessed": not_assessed,
        "suggestions": suggestions,
        "total_sgd": sum(s["price_sgd"] for s in suggestions),
        "unverified": _unverified_uploads(record),
    }


def _flag(record: CleanRecord, marker: Marker, latest: Measurement, status: str) -> dict:
    return {
        "marker": marker.key,
        "name": marker.name,
        "value": _number(marker.round(latest.value)),
        "unit": marker.display_unit,
        "status": status,
        "report": latest.report.id,
        "date": latest.report.date,
        "trend": [
            {"report": m.report.id, "date": m.report.date, "value": _number(marker.round(m.value))}
            for m in record.history(marker) if m.usable
        ],
    }


def _follow_up_test(marker_key: str) -> Test:
    return next(t for t in TESTS.values() if t.key != RETEST.test and marker_key in t.covers)


def _suggestion(test: Test, reason: str, flagged: list[str]) -> dict:
    return {
        "test": test.key,
        "name": test.name,
        "price_sgd": test.price_sgd,
        "reason": reason,
        "markers": [key for key in flagged if key in test.covers],
        "action": {"type": "add_to_cart", "test": test.key},
    }


def _unverified_uploads(record: CleanRecord) -> list[dict]:
    """Uploads still under review. Shown on their own, never mixed into flags or trends."""
    uploads = []
    for report in record.member.reports:
        if report.is_verified:
            continue
        results = []
        for m in record.from_report(report):
            results.append({
                "marker": m.marker.key if m.marker else None,
                "name": m.marker.name if m.marker else m.original.marker,
                "value": _number(m.marker.round(m.value) if m.usable else m.original.value),
                "unit": m.marker.display_unit if m.usable else None,
                "original": {"value": _number(m.original.value), "unit": m.original.unit},
                "note": m.problem,
            })
        uploads.append({"report": report.id, "date": report.date, "lab": report.lab,
                        "review": report.review, "results": results})
    return uploads


def _number(value: Decimal) -> int | float:
    """JSON has no Decimal type. Values with no decimal places go out as ints (205), the rest as floats (68.0, 2.7)."""
    return int(value) if value.as_tuple().exponent >= 0 else float(value)
