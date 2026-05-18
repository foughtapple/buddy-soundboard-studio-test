"""Activity log helper for the soundboard."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ActivityLog:
    """Fixed-size newest-first activity log."""

    limit: int = 10
    _entries: deque[str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.limit < 1:
            raise ValueError("ActivityLog limit must be at least 1")
        self._entries = deque(maxlen=self.limit)

    def record(self, pad_name: str, when: datetime | None = None) -> None:
        clean_name = pad_name.strip()
        if not clean_name:
            raise ValueError("pad_name must not be blank")
        timestamp = (when or datetime.now()).strftime("%H:%M:%S")
        self._entries.appendleft(f"{timestamp}  {clean_name}")

    def entries(self) -> list[str]:
        return list(self._entries)

    def as_text(self) -> str:
        if not self._entries:
            return "No pads played yet."
        return "\n".join(self._entries)
