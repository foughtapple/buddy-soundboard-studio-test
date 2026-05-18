"""Tkinter GUI for Buddy Soundboard Studio."""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk

from .activity_log import ActivityLog
from .sound_engine import PAD_SOUNDS, SoundEngine, SoundSpec

APP_TITLE = "Soundboard Studio"
PAD_NAMES = [
    "Airhorn",
    "Applause",
    "Laser",
    "Drum Hit",
    "Bell",
    "Error Buzz",
    "Magic",
    "Victory",
]


class SoundboardApp(tk.Tk):
    """Small polished soundboard/sample-pad GUI."""

    def __init__(self, sound_engine: SoundEngine | None = None) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("920x620")
        self.minsize(820, 560)
        self.configure(bg="#10141f")

        self.sound_engine = sound_engine or SoundEngine()
        self.activity_log = ActivityLog(limit=10)
        self.volume_var = tk.IntVar(value=65)
        self.now_playing_var = tk.StringVar(value="Now playing: Ready")
        self.log_var = tk.StringVar(value="No pads played yet.")

        self._configure_styles()
        self._build_layout()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Root.TFrame", background="#10141f")
        style.configure("Panel.TFrame", background="#171d2b", borderwidth=0)
        style.configure(
            "Title.TLabel",
            background="#10141f",
            foreground="#f8fafc",
            font=("Segoe UI", 30, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#10141f",
            foreground="#94a3b8",
            font=("Segoe UI", 11),
        )
        style.configure(
            "Now.TLabel",
            background="#172033",
            foreground="#7dd3fc",
            font=("Segoe UI", 15, "bold"),
            padding=14,
        )
        style.configure(
            "Pad.TButton",
            font=("Segoe UI", 15, "bold"),
            padding=20,
            background="#243044",
            foreground="#f8fafc",
            borderwidth=1,
            focusthickness=3,
            focuscolor="#38bdf8",
        )
        style.map(
            "Pad.TButton",
            background=[("active", "#334155"), ("pressed", "#0ea5e9")],
            foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
        )
        style.configure(
            "Danger.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10,
            background="#7f1d1d",
            foreground="#ffffff",
        )
        style.map("Danger.TButton", background=[("active", "#991b1b")])
        style.configure(
            "Control.TLabel",
            background="#171d2b",
            foreground="#cbd5e1",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "Log.TLabel",
            background="#0f172a",
            foreground="#cbd5e1",
            font=("Consolas", 10),
            padding=12,
        )
        style.configure(
            "Horizontal.TScale",
            background="#171d2b",
            troughcolor="#334155",
        )

    def _build_layout(self) -> None:
        root = ttk.Frame(self, style="Root.TFrame", padding=24)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)

        ttk.Label(root, text=APP_TITLE, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            root,
            text="Eight generated sample pads. No external audio files required.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(0, 18))

        content = ttk.Frame(root, style="Root.TFrame")
        content.grid(row=2, column=0, sticky="nsew")
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        pad_panel = ttk.Frame(content, style="Panel.TFrame", padding=18)
        pad_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        for row in range(2):
            pad_panel.rowconfigure(row, weight=1, uniform="pad_rows")
        for column in range(4):
            pad_panel.columnconfigure(column, weight=1, uniform="pad_cols")

        for index, pad_name in enumerate(PAD_NAMES):
            row, column = divmod(index, 4)
            button = ttk.Button(
                pad_panel,
                text=pad_name,
                style="Pad.TButton",
                command=lambda name=pad_name: self.play_pad(name),
            )
            button.grid(row=row, column=column, sticky="nsew", padx=9, pady=9)

        side = ttk.Frame(content, style="Panel.TFrame", padding=18)
        side.grid(row=0, column=1, sticky="nsew")
        side.columnconfigure(0, weight=1)
        side.rowconfigure(5, weight=1)

        ttk.Label(side, textvariable=self.now_playing_var, style="Now.TLabel").grid(
            row=0, column=0, sticky="ew", pady=(0, 18)
        )
        ttk.Label(side, text="Volume", style="Control.TLabel").grid(row=1, column=0, sticky="w")
        ttk.Scale(
            side,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.volume_var,
        ).grid(row=2, column=0, sticky="ew", pady=(6, 18))
        ttk.Button(side, text="Stop Sound", style="Danger.TButton", command=self.stop_sound).grid(
            row=3, column=0, sticky="ew", pady=(0, 24)
        )
        ttk.Label(side, text="Activity Log", style="Control.TLabel").grid(row=4, column=0, sticky="w")
        ttk.Label(side, textvariable=self.log_var, style="Log.TLabel", anchor="nw", justify="left").grid(
            row=5, column=0, sticky="nsew", pady=(6, 0)
        )

    def play_pad(self, pad_name: str) -> None:
        spec = PAD_SOUNDS[pad_name]
        volume = max(0, min(100, int(self.volume_var.get()))) / 100
        self.now_playing_var.set(f"Now playing: {pad_name}")
        self.activity_log.record(pad_name)
        self.log_var.set(self.activity_log.as_text())

        thread = threading.Thread(
            target=self.sound_engine.play,
            args=(spec, volume),
            daemon=True,
        )
        thread.start()

    def stop_sound(self) -> None:
        self.sound_engine.stop()
        self.now_playing_var.set("Now playing: Stopped")


def app_title() -> str:
    return APP_TITLE


def main() -> None:
    app = SoundboardApp()
    app.mainloop()
