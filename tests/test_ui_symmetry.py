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

    def test_ev_selection_window_symmetry(self):
        """Verify runtime symmetry of EV selection window widgets."""
        import modules.gui.ev_selection_window
        from modules.gui.ev_selection_window import ask_for_ev_targets
        
        with patch('modules.gui.ev_selection_window.context') as mock_ctx, \
             patch('modules.gui.ev_selection_window.get_party') as mock_get_party:
            
            mock_ctx.gui.window = self.root
            mock_ctx.gui.is_headless = False
            
            mock_mon = MagicMock()
            mock_mon.name = "TestMon"
            mock_mon.evs = {"hp":0, "attack":0, "defence":0, "speed":0, "special_attack":0, "special_defence":0}
            mock_get_party.return_value = [mock_mon]

            # Helper to traverse and check
            def verify():
                top_levels = [w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel)]
                if not top_levels:
                    self.fail("EV Window did not open")
                window = top_levels[0]

                # Check Main Frame Padding (should be 15)
                frames = [c for c in window.winfo_children() if isinstance(c, ttk.Frame)]
                found_main = False
                for f in frames:
                    try:
                        pad = str(f.cget('padding'))
                        # Tcl/Tk can return padding as "15", "(15,)", "15 15 15 15"
                        if "15" in pad:
                            found_main = True
                            break
                    except:
                        pass
                
                if not found_main:
                    self.fail("Could not find Main Frame with padding=15 in EV Window")

                # Check buttons padding (pady=15)
                # Need to find the main frame first (assuming first one found is main or contains buttons)
                main_frame = frames[0]
                
                children = main_frame.winfo_children()
                buttons = [c for c in children if isinstance(c, ttk.Button)]
                
                for btn in buttons:
                    info = btn.grid_info()
                    pady = str(info.get('pady', 0))
                    if pady != "15":
                         self.fail(f"EV Button has asymmetric or wrong pady: {pady} (expected 15)")

                # Use event to trigger closing mechanism which updates logic variables
                window.event_generate("<Escape>")

            self.root.after(200, verify)
            
            try:
                ask_for_ev_targets(mock_mon)
            except tk.TclError:
                pass
            except Exception as e:
                # If window is destroyed during the loop, generic Exception or TclError might be raised
                if "application has been destroyed" not in str(e):
                    raise e
    
    def test_multi_select_window_symmetry(self):
        """Verify runtime symmetry of multi-select window widgets."""
        import modules.gui.multi_select_window
        from modules.gui.multi_select_window import ask_for_confirmation
        
        with patch('modules.gui.multi_select_window.context') as mock_ctx:
            mock_ctx.gui.window = self.root
            mock_ctx.gui.is_headless = False
            
            def verify():
                top_levels = [w for w in self.root.winfo_children() if isinstance(w, tk.Toplevel)]
                if not top_levels:
                    self.fail("Confirmation Window did not open")
                window = top_levels[0]
                
                # Check frame padding=20
                frames = [c for c in window.winfo_children() if isinstance(c, ttk.Frame)]
                if not frames:
                    self.fail("No frame found in confirmation window")
                    
                padding = str(frames[0].cget('padding'))
                
                if "20" not in padding:
                    self.fail(f"Confirmation Frame padding is {padding}, expected 20")
                    
                # Check label pady=20
                labels = [c for c in frames[0].winfo_children() if isinstance(c, ttk.Label)]
                if not labels:
                     self.fail("No label found in confirmation window")
                
                pady = str(labels[0].grid_info().get('pady', 0))
                if "20" not in pady:
                    self.fail(f"Confirmation Label pady is {pady}, expected 20")

                if "20" not in pady:
                    self.fail(f"Confirmation Label pady is {pady}, expected 20")

                window.event_generate("<Escape>")

            self.root.after(200, verify)
            ask_for_confirmation("Test Message")

    def test_main_controls_alignment(self):
        """Verify that the 3 main control groups are vertically aligned (same Y coordinate)."""
        import modules.gui.emulator_controls
        from modules.gui.emulator_controls import EmulatorControls
        
        with patch('modules.gui.emulator_controls.context') as mock_ctx, \
             patch('modules.gui.debug_menu.context', new=mock_ctx): # Share the same mock
            mock_ctx.gui.window = self.root
            mock_ctx.gui.is_headless = False
            mock_ctx.bot_mode = "Manual"
            mock_ctx.emulation_speed = 1
            mock_ctx.video = True
            mock_ctx.audio = True
            mock_ctx.config.keys.emulator = MagicMock()
            mock_ctx.rom = MagicMock()
            mock_ctx.rom.game_name = "Pokemon Emerald"
            mock_ctx.rom.is_emerald = True
            mock_ctx.rom.is_firered = False
            mock_ctx.rom.get_game_id.return_value = "BPEE"
            mock_ctx.debug = True # Force debug menu to init so we test it too
            
            # Create a container for the controls
            container = ttk.Frame(self.root)
            container.pack()
            
            controls = EmulatorControls(self.root, container)
            controls.add_to_window()
            
            # Force layout
            self.root.update_idletasks()
            
            # Find the 3 groups
            # They are children of controls.frame, created as ttk.Frame
            children = controls.frame.winfo_children()
            frames = [c for c in children if isinstance(c, ttk.Frame)]
            
            # We expect at least 3 frames (Bot Mode, Speed, Settings)
            # plus maybe others depending on implementation, but these 3 should be in row 0
            row_0_frames = []
            for f in frames:
                info = f.grid_info()
                if str(info.get('row')) == '0':
                    row_0_frames.append(f)
            
            self.assertGreaterEqual(len(row_0_frames), 3, "Could not find the 3 main control groups in row 0")
            
            # Check Y alignment check
            # Since they are in the same grid row, they should have the same Y coordinate relative to parent
            # IF they have the same sticky and padding instructions.
            # We can check their grid_info options for 'pady' and 'sticky' equality
            
            # Verify column weights (should all be 1)
            for col in range(3):
                col_weight = controls.frame.columnconfigure(col)['weight']
                self.assertEqual(col_weight, 1, f"Column {col} weight should be 1, got {col_weight}")

            # Sort frames by column index to ensure we check the right ones
            # (row_0_frames might not be in column order depending on winfo_children order)
            row_0_frames.sort(key=lambda x: int(x.grid_info()['column']))

            # Expected sticky values for [Bot Mode, Speed, Settings]
            expected_stickies = ["nw", "n", "ne"]
            
            for i, f in enumerate(row_0_frames):
                if i >= 3: break # Ignore extra frames if any (shouldn't be)
                
                info = f.grid_info()
                pady = str(info.get('pady', '0'))
                sticky = str(info.get('sticky', '')).lower()
                
                # Check vertical alignment (pady should be 10 for all)
                self.assertEqual(pady, "10", f"Group {i} (col {i}) pady mismatch: {pady} != 10")
                
                # Check horizontal alignment strategy
                self.assertEqual(sticky, expected_stickies[i], 
                                 f"Group {i} (col {i}) sticky mismatch: {sticky} != {expected_stickies[i]}")

            controls.remove_from_window()
            container.destroy()

if __name__ == "__main__":
    unittest.main()
