# Buddy Soundboard Studio Test

A polished Windows desktop mini soundboard studio built as an AI Code Buddy test project.

The app uses a standard-library Tkinter GUI and generated Windows beep patterns, so the first version does not need external audio files or private data storage.

## Features

- Dark themed desktop GUI.
- Title: **Soundboard Studio**.
- Eight large sound pads in a 2 x 4 grid.
- Pads: Airhorn, Applause, Laser, Drum Hit, Bell, Error Buzz, Magic, Victory.
- Generated sound effects using standard Python/Windows capabilities where practical.
- Now Playing label.
- Volume slider.
- Stop Sound button.
- Activity log showing the last 10 played pads.

## Setup

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

This creates `.venv` if missing, upgrades pip, and installs the project with development extras.

## Run

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run.ps1
```

Or run the stable entry point directly after setup:

```powershell
.\.venv\Scripts\python.exe run_app.py
```

## Test

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\test.ps1
```

## Package

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\package.ps1
```

The packaged app is written to:

```text
dist\BuddySoundboardStudioTest
```

## Notes

- No external audio files are required.
- `winsound.Beep` does not support true amplitude control, so the first version approximates volume by changing generated tone duration.
- On non-Windows systems, sound playback falls back to short sleeps so tests and imports remain safe.
