from datetime import datetime

import pytest

from buddy_soundboard_studio_test.activity_log import ActivityLog


def test_activity_log_keeps_last_10_newest_first() -> None:
    log = ActivityLog(limit=10)

    for index in range(12):
        log.record(f"Pad {index}", when=datetime(2026, 1, 1, 12, 0, index))

    entries = log.entries()
    assert len(entries) == 10
    assert entries[0].endswith("Pad 11")
    assert entries[-1].endswith("Pad 2")


def test_activity_log_rejects_blank_pad_name() -> None:
    log = ActivityLog()

    with pytest.raises(ValueError, match="pad_name"):
        log.record("   ")


def test_activity_log_empty_text() -> None:
    assert ActivityLog().as_text() == "No pads played yet."
