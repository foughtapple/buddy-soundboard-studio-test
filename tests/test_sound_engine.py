from buddy_soundboard_studio_test.sound_engine import PAD_SOUNDS, clamp_frequency, scaled_duration_ms


def test_all_required_pad_sounds_exist() -> None:
    expected = {
        "Airhorn",
        "Applause",
        "Laser",
        "Drum Hit",
        "Bell",
        "Error Buzz",
        "Magic",
        "Victory",
    }

    assert set(PAD_SOUNDS) == expected
    assert all(spec.tones for spec in PAD_SOUNDS.values())


def test_scaled_duration_clamps_volume_range() -> None:
    assert scaled_duration_ms(100, -1.0) == 35
    assert scaled_duration_ms(100, 0.5) == 67
    assert scaled_duration_ms(100, 2.0) == 100
    assert scaled_duration_ms(1, 1.0) == 20


def test_clamp_frequency_matches_windows_beep_range() -> None:
    assert clamp_frequency(1) == 37
    assert clamp_frequency(440) == 440
    assert clamp_frequency(50000) == 32767
