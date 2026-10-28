"""Turns the raw result rows into measurements we can trust (or know not to).

The rule throughout: never guess and never drop anything silently. A row we can't use
keeps a `problem`, and every change is written to `notes` for the team.
"""
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal

from app.markers import Marker, match_marker, normalise_unit
from app.records import MemberFile, Report, ResultRow


@dataclass
class Measurement:
    report: Report
    marker: Marker | None          # None if we don't recognise the name
    original: ResultRow            # the row exactly as it came in
    value: Decimal | None = None   # in the display unit, full precision
    problem: str | None = None     # why it can't be used, if it can't

    @property
    def usable(self) -> bool:
        return self.problem is None


@dataclass
class CleanRecord:
    member: MemberFile
    measurements: list[Measurement]
    notes: list[str]  # for the team; never sent to the member

    def history(self, marker: Marker) -> list[Measurement]:
        """Every verified measurement of a marker, oldest first."""
        found = [m for m in self.measurements if m.marker == marker and m.report.is_verified]
        return sorted(found, key=lambda m: m.report.date)

    def latest(self, marker: Marker) -> Measurement | None:
        """The newest verified measurement, even if it's unusable. We never fall back to an older one."""
        history = self.history(marker)
        return history[-1] if history else None

    def from_report(self, report: Report) -> list[Measurement]:
        return [m for m in self.measurements if m.report is report]


def clean(member: MemberFile) -> CleanRecord:
    notes: list[str] = []
    measurements = _match_and_dedupe(member, notes)
    _mark_conflicts(measurements)
    for m in measurements:
        if m.usable:
            _convert(m, notes)
        if not m.usable:
            notes.append(f"{m.report.id} {_label(m)}: {m.problem}")
    for report in member.reports:
        if not report.is_verified:
            notes.append(f"{report.id}: not verified, kept out of flags, trends and suggestions")
    return CleanRecord(member, measurements, notes)


def _match_and_dedupe(member: MemberFile, notes: list[str]) -> list[Measurement]:
    """Match each row to a marker and drop exact duplicates, compared as given (before conversion)."""
    reports = {r.id: r for r in member.reports}
    seen, kept = set(), []
    for row in member.results:
        marker = match_marker(row.marker)
        identity = (row.report, marker.key if marker else row.marker, row.value, normalise_unit(row.unit))
        if identity in seen:
            notes.append(f"{row.report} {identity[1]}: duplicate row dropped")
            continue
        seen.add(identity)
        problem = None if marker else "unknown_marker"
        kept.append(Measurement(reports[row.report], marker, row, problem=problem))
    return kept


def _mark_conflicts(measurements: list[Measurement]) -> None:
    """Two different values for one marker in one report: we can't pick, so neither is used."""
    counts = Counter((m.report.id, m.marker.key) for m in measurements if m.marker)
    for m in measurements:
        if m.marker and counts[(m.report.id, m.marker.key)] > 1:
            m.problem = "conflicting_values"


def _convert(m: Measurement, notes: list[str]) -> None:
    unit = m.original.unit
    if not unit.strip():
        m.problem = "unit_missing"
    elif not m.marker.accepts(unit):
        m.problem = "unit_unrecognised"
    else:
        m.value = m.marker.to_display_unit(m.original.value, unit)
        if normalise_unit(unit) != normalise_unit(m.marker.display_unit):
            notes.append(f"{m.report.id} {m.marker.key}: converted from {m.original.value} {unit}")


def _label(m: Measurement) -> str:
    return m.marker.key if m.marker else m.original.marker
