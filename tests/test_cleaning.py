from decimal import Decimal

from app.markers import MARKERS


def measurement(record, report, marker_key):
    (found,) = [m for m in record.measurements
                if m.report.id == report and m.marker and m.marker.key == marker_key]
    return found


def test_converts_to_display_units(run):
    record, _ = run()
    assert measurement(record, "R3", "hba1c").value == Decimal("37.70505")  # 5.6 %
    assert measurement(record, "U1", "ldl").value.quantize(Decimal("0.001")) == Decimal("2.689")  # 104 mg/dL
    assert measurement(record, "U1", "vitd").value == Decimal("77.376")  # 31 ng/mL
    assert measurement(record, "R1", "hba1c").value == 40  # already mmol/mol


def test_matches_different_names_for_one_marker(run):
    record, _ = run()
    assert [m.report.id for m in record.history(MARKERS["ldl"])] == ["R1", "R2", "R3"]  # R2 says LDL-C
    assert measurement(record, "U1", "vitd").original.marker == "25 OH Vitamin D"


def test_drops_exact_duplicate(run):
    record, _ = run()
    assert measurement(record, "R3", "hscrp").value == Decimal("1.1")  # one row left, not two
    assert "R3 hscrp: duplicate row dropped" in record.notes


def test_never_guesses_a_missing_unit(run):
    record, _ = run()
    glucose = measurement(record, "U1", "glucose")
    assert glucose.problem == "unit_missing" and glucose.value is None
