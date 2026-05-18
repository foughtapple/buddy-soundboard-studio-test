from buddy_soundboard_studio_test.app import app_title


def test_app_title():
    assert app_title() == 'Buddy Soundboard Studio Test'
