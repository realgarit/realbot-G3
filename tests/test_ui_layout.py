import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import ttkbootstrap as ttk
from modules.gui.emulator_screen import EmulatorScreen
from modules.gui.select_profile_screen import SelectProfileScreen
from modules.gui.emulator_controls import EmulatorControls

class TestUILayout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Share one root window for the entire test suite to avoid Tcl "application destroyed" errors
        # with ttkbootstrap's global style cache.
        cls.root = ttk.Window(themename="cosmo")
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()
        
    def setUp(self):
        # Clean up any widgets attached to root from previous tests
        for widget in self.root.winfo_children():
            widget.destroy()


    def test_emulator_screen_layout_structure(self):
        """Verify EmulatorScreen uses grid and has correct resizing weights."""
        # Patch BOTH locations because they imported 'context' separately at module level
        with patch('modules.gui.emulator_screen.context') as mock_ctx_screen, \
             patch('modules.gui.emulator_controls.context') as mock_ctx_controls:
             
             # Setup mock for screen
             mock_ctx_screen.profile.path.name = "TestProfile"
             mock_ctx_screen.debug = False
             
             # Setup mock for controls (it needs stats, emulator, etc)
             mock_ctx_controls.emulator = MagicMock()
             mock_ctx_controls.profile.path = MagicMock()
             mock_ctx_controls.bot_mode = "Manual"
             mock_ctx_controls.emulation_speed = 1
             mock_ctx_controls.rom.is_emerald = False
             mock_ctx_controls.debug = False # explicitly False to avoid debug menu access
             
             screen = EmulatorScreen(self.root)
             screen.enable()
             
             # Check main frame

        self.assertIsInstance(screen.frame, ttk.Frame)
        # Verify grid usage (info return dict if managed by grid)
        self.assertTrue(screen.frame.grid_info(), "Main frame should be managed by grid")
        
        # Verify row weights for responsiveness
        # Row 0 is canvas, should extend
        self.assertEqual(int(screen.frame.rowconfigure(0)['weight']), 1, "Canvas row should expand")
        
        # Check control bar placement
        self.assertTrue(screen.control_bar.grid_info(), "Control bar should be managed by grid")
        self.assertEqual(int(screen.control_bar.grid_info()['row']), 1, "Control bar should be on row 1")
        
        screen.disable()

    def test_select_profile_screen_padding(self):
        """Verify SelectProfileScreen has consistent padding."""
        mock_cb = MagicMock()
        screen = SelectProfileScreen(self.root, mock_cb, mock_cb)
        
        # We need to mock list_available_profiles or it might fail/empty
        with patch('modules.gui.select_profile_screen.list_available_profiles', return_value=[]):
            # If empty it goes to creation screen, so we mock non-empty for layout test
            # Also mock sorting logic if needed, but return value is mock object
             with patch('modules.gui.select_profile_screen.list_available_profiles', return_value=[MagicMock()]):
                # Create screen again inside patch context if list is called in init?? No, it's called in enable.
                screen.enable()
                
                # Check main padding
                # Tkinter returns padding as string "10" or tuple ("10",)
                padding = str(screen.frame.cget('padding'))
                self.assertTrue("10" in padding, f"Main frame padding should be 10, got {padding}")
                
                # Verify search frame structure
                self.assertIsNotNone(screen.search_frame, "Search frame should exist")
                # It is successfully initialized as a Frame
                self.assertIsInstance(screen.search_frame, ttk.Frame)
                
                screen.disable()

    def test_emulator_controls_alignment(self):
        """Verify EmulatorControls widgets align correctly."""
        controls = EmulatorControls(self.root)
        controls.frames = MagicMock() # Mock frames if needed? No, logic is in add_to_window
        
        # We need to mock context because controls uses it
        with patch('modules.gui.emulator_controls.context') as mock_ctx:
             mock_ctx.bot_mode = "Manual"
             mock_ctx.emulation_speed = 1
             mock_ctx.rom.is_emerald = False
             mock_ctx.debug = False
             mock_ctx.emulator = MagicMock()
             mock_ctx.profile.path = MagicMock() # For 'Open Profile Folder'
             
             controls.add_to_window()
             
             # Check grid padding instead of frame internal padding for symmetry
             padding = controls.frame.grid_info().get('padx', 0)
             self.assertEqual(padding, 5, f"Controls frame should have grid padx 5, got {padding}")
             
             # Check alignment of bot mode button
             info = controls.bot_mode_button.grid_info()
             self.assertEqual(info['sticky'], 'w', "Bot mode should left align (w)")
             
             controls.remove_from_window()

if __name__ == '__main__':
    unittest.main()
