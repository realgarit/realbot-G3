import unittest
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as bttk
from unittest.mock import MagicMock, patch
from modules.gui.emulator_screen import EmulatorScreen
from modules.gui.emulator_controls import EmulatorControls

class TestUISymmetry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = bttk.Window(themename="darkly")
        # Ensure the window is drawn so winfo values are updated
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_canvas_border_symmetry(self):
        """Mathematically verify the gap from canvas to window edges."""
        with patch('modules.core.context.context') as mock_ctx_screen, \
             patch('modules.gui.emulator_screen.context') as mock_ctx_screen_alt, \
             patch('modules.gui.emulator_controls.context') as mock_ctx_controls:
             
             mock_ctx_screen.profile.path.name = "Test"
             mock_ctx_screen.debug = False
             mock_ctx_screen.rom.short_game_name = "Emerald"
             mock_ctx_screen.rom.game_name = "Pokemon Emerald"
             
             # Also fix the alternate patch location
             mock_ctx_screen_alt.debug = False
             
             mock_ctx_controls.emulator = MagicMock()
             mock_ctx_controls.profile.path = MagicMock()
             mock_ctx_controls.bot_mode = "Manual"
             mock_ctx_controls.emulation_speed = 1
             mock_ctx_controls.rom.is_emerald = False
             mock_ctx_controls.rom.short_game_name = "Emerald" # Fix mock
             mock_ctx_controls.rom.game_name = "Pokemon Emerald" # Fix mock
             mock_ctx_controls.debug = False
             
             # Simulate RealbotGui master container
             content_frame = bttk.Frame(self.root, padding=0)
             content_frame.pack(padx=5, pady=5, fill="both", expand=True)

             screen = EmulatorScreen(self.root, content_frame)
             screen.enable()
             
             # Force update to calculate geometry
             self.root.update_idletasks()
             self.root.update()
             
             # Get geometries
             window_rootx = self.root.winfo_rootx()
             window_width = self.root.winfo_width()
             
             canvas = screen.canvas
             canvas_x = canvas.winfo_rootx()
             canvas_w = canvas.winfo_width()
             
             total_left = canvas_x - window_rootx
             total_right = window_width - (total_left + canvas_w)
             
             self.assertEqual(total_left, total_right, f"Symmetry broken! Left={total_left}px, Right={total_right}px")

if __name__ == "__main__":
    unittest.main()
