from datetime import date


def flags_by_marker(body):
    return {f["marker"]: f for f in body["flags"]}


def test_flags_alexs_markers_in_order(run):
    _, body = run()
    flags = flags_by_marker(body)
    assert list(flags) == ["ldl", "apob", "hscrp", "vitd", "ferritin"]
    assert {f["status"] for f in body["flags"]} == {"moderate"}
    assert "hba1c" not in flags  # 37.7 mmol/mol is optimal


def test_pending_upload_is_never_used(run):
    _, body = run()
    assert flags_by_marker(body)["ldl"]["value"] == 2.9  # R3, not the newer U1 value of 2.7
    assert all(f["report"] != "U1" for f in body["flags"])
    assert all(point["report"] != "U1" for f in body["flags"] for point in f["trend"])


def test_retest_is_overdue(run):
    _, body = run()
    assert body["retest"] == {"status": "overdue", "due": date(2026, 9, 14), "days_overdue": 42}


def test_suggests_retest_then_one_test_per_remaining_marker(run):
    _, body = run()
    assert [(s["test"], s["markers"]) for s in body["suggestions"]] == [
        ("retest_6m", ["ldl", "hscrp", "vitd"]),
        ("apob_addon", ["apob"]),
        ("iron_studies", ["ferritin"]),
    ]
    assert body["total_sgd"] == 285
