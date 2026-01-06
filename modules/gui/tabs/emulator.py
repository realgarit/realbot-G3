# Copyright (c) 2026 realgarit
from tkinter import ttk
from typing import TYPE_CHECKING

from modules.gui.emulator_controls import DebugTab
from modules.gui.tabs.utils import FancyTreeview

if TYPE_CHECKING:
    from modules.game.libmgba import LibmgbaEmulator


class EmulatorTab(DebugTab):
    _tv: FancyTreeview

    def draw(self, root: ttk.Notebook):
        frame = ttk.Frame(root, padding=10)
        self._tv = FancyTreeview(frame)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        root.add(frame, text="Emulator")

    def update(self, emulator: "LibmgbaEmulator"):
        self._tv.update_data(self._get_data(emulator))

    def _get_data(self, emulator: "LibmgbaEmulator"):
        core = emulator._core

        return {
            "Core": {
                "Audio Buffer Size": core.audio_buffer_size,
                "Frame Counter": core.frame_counter,
                "CPU Frequency": core.frequency,
            }
        }
