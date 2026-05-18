"""Generated Windows sound effects for the soundboard."""

from __future__ import annotations

import math
import sys
import threading
import time
from dataclasses import dataclass

try:  # pragma: no cover - winsound is unavailable on non-Windows CI runners.
    import winsound
except ImportError:  # pragma: no cover
    winsound = None  # type: ignore[assignment]


@dataclass(frozen=True, slots=True)
class Tone:
    frequency_hz: int
    duration_ms: int
    gap_ms: int = 20


@dataclass(frozen=True, slots=True)
class SoundSpec:
    name: str
    tones: tuple[Tone, ...]


PAD_SOUNDS: dict[str, SoundSpec] = {
    "Airhorn": SoundSpec("Airhorn", (Tone(440, 180), Tone(520, 180), Tone(440, 220))),
    "Applause": SoundSpec("Applause", tuple(Tone(freq, 45, 10) for freq in (700, 900, 650, 1100, 800, 1000, 760, 950))),
    "Laser": SoundSpec("Laser", tuple(Tone(freq, 28, 3) for freq in range(1200, 320, -110))),
    "Drum Hit": SoundSpec("Drum Hit", (Tone(160, 70, 8), Tone(105, 110, 8), Tone(75, 160, 0))),
    "Bell": SoundSpec("Bell", (Tone(988, 180, 30), Tone(1319, 220, 20), Tone(988, 280, 0))),
    "Error Buzz": SoundSpec("Error Buzz", (Tone(220, 160, 30), Tone(180, 180, 30), Tone(140, 220, 0))),
    "Magic": SoundSpec("Magic", tuple(Tone(freq, 55, 10) for freq in (523, 659, 784, 1047, 1319, 1568))),
    "Victory": SoundSpec("Victory", (Tone(523, 120), Tone(659, 120), Tone(784, 120), Tone(1047, 360, 0))),
}


def scaled_duration_ms(duration_ms: int, volume: float) -> int:
    """Return a practical duration that makes low volume feel softer.

    winsound.Beep does not support amplitude control, so the first version uses
    duration scaling as a standard-library-only approximation.
    """

    clamped = max(0.0, min(1.0, volume))
    return max(20, int(duration_ms * (0.35 + (0.65 * clamped))))


def clamp_frequency(frequency_hz: int) -> int:
    """Clamp to the Windows Beep supported range."""

    return max(37, min(32767, int(frequency_hz)))


class SoundEngine:
    """Simple interruptible generated-tone sound engine."""

    def __init__(self) -> None:
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

    def play(self, spec: SoundSpec, volume: float = 1.0) -> None:
        with self._lock:
            self._stop_event.clear()
            for tone in spec.tones:
                if self._stop_event.is_set():
                    break
                self._play_tone(tone, volume)

    def stop(self) -> None:
        self._stop_event.set()

    def _play_tone(self, tone: Tone, volume: float) -> None:
        if volume <= 0:
            time.sleep(tone.duration_ms / 1000)
            return

        duration = scaled_duration_ms(tone.duration_ms, volume)
        frequency = clamp_frequency(tone.frequency_hz)

        if winsound is not None and sys.platform.startswith("win"):
            winsound.Beep(frequency, duration)  # type: ignore[union-attr]
        else:  # Non-Windows fallback keeps tests/dev runs harmless.
            time.sleep(duration / 1000)

        if tone.gap_ms > 0:
            time.sleep(tone.gap_ms / 1000)
