
import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.built_in_plugins.generate_encounter_media import GenerateEncounterMediaPlugin
from modules.pokemon.encounter import EncounterValue, EncounterInfo

class TestTCGPlugin(unittest.TestCase):
    def setUp(self):
        # Mock context
        self.mock_context_patcher = patch('modules.built_in_plugins.generate_encounter_media.context')
        self.mock_context = self.mock_context_patcher.start()
        
        # Setup config
        self.mock_context.config.logging.tcg_cards = True
        self.mock_context.profile.path = Path("/tmp/test_profile")

        self.plugin = GenerateEncounterMediaPlugin()

    def tearDown(self):
        self.mock_context_patcher.stop()



    @patch('modules.built_in_plugins.generate_encounter_media.generate_tcg_card')
    @patch('modules.built_in_plugins.generate_encounter_media.Thread')
    def test_on_logging_encounter_triggers_tcg_card(self, mock_thread, mock_generate):
        """Verify that on_logging_encounter triggers TCG card generation for shinies."""
        
        # Create a mock shiny encounter
        mock_encounter = MagicMock(spec=EncounterInfo)
        mock_encounter.value = EncounterValue.Shiny
        mock_encounter.map = MagicMock(pretty_name="Test Map") # Fix AttributeError for map
        
        # Setup nested pokemon object
        mock_pokemon = MagicMock()
        mock_pokemon.data = b'some_data'
        mock_pokemon.species_name_for_stats = "TORCHIC"
        
        # Create explicit species mock
        mock_species = MagicMock()
        mock_species.name = "Torchic"
        mock_species.national_dex_number = 255
        mock_pokemon.species = mock_species
        
        mock_encounter.pokemon = mock_pokemon
        
        # Run the hook
        self.plugin.on_logging_encounter(mock_encounter)
        
        # Verify Thread was started
        mock_thread.assert_called_once()
        
        # Verify args passed to thread
        args, kwargs = mock_thread.call_args
        # The target should be generate_tcg_card (the mock object itself)
        # Instead of checking name, check identity
        self.assertIs(kwargs['target'], mock_generate)
        
    @patch('modules.built_in_plugins.generate_encounter_media.generate_tcg_card')
    def test_on_logging_encounter_ignores_non_shiny(self, mock_generate):
        """Verify that non-shiny encounters do NOT trigger TCG card generation."""
        
        mock_encounter = MagicMock(spec=EncounterInfo)
        mock_encounter.value = EncounterValue.Trash # Not shiny
        
        self.plugin.on_logging_encounter(mock_encounter)
        
        mock_generate.assert_not_called()


    @patch('modules.items.tcg_card.Image.open')
    @patch('modules.items.tcg_card.get_sprites_path')
    @patch('modules.items.tcg_card.Pokemon')
    @patch('modules.core.context.context') # Mock context for rom checks
    def test_tcg_card_uses_proper_case_filename(self, mock_context, mock_pokemon_class, mock_get_path, mock_image_open):
        """Verify that TCG card generation uses species.name (proper case) not nickname."""
        
        # Import the function to test
        from modules.items.tcg_card import generate_tcg_card
        
        # Mock path to return a dummy path
        mock_get_path.return_value = Path("/mock/sprites")
        
        # Mock context.rom.is_rse
        mock_context.rom.is_rse = True
        
        # Define simple fake classes to avoid MagicMock formatting hell
        class FakeSpecies:
            name = "Torchic"
            national_dex_number = 255
            types = ["Fire"]
            

        class FakeIVs:
            hp = 31
            attack = 31
            defence = 31
            special_attack = 31
            special_defence = 31
            speed = 31
            def sum(self): return 186
            
        class FakeNature:
            name = "Jolly"
            
        class FakeAbility:
            name = "Blaze"
            
        class FakeMoveData:
            def __init__(self, name):
                self.name = name
                self.type = MagicMock()
                self.type.name = "Normal"
                self.base_power = 40
                self.accuracy = 100
                self.pp = 35
                self.description = "A standard move."
        
        class FakeLearnedMove:
            def __init__(self, name):
                self.move = FakeMoveData(name)

        class FakeOriginalTrainer:
            name = "Ash"
            gender = "male"
            id = 12345
            secret_id = 54321

        class FakePokemon:
            species = FakeSpecies()
            is_shiny = True
            species_name_for_stats = "TORCHIC" # Uppercase
            game_of_origin = "Ruby"
            dex_number = 255
            level = 5
            gender = "male"
            trainer_memo = "Met at level 5."
            met_location = "Route 101"
            ot_name = "Ash"
            ot_id = 12345
            name = "Torchic"
            personality_value = 0x12345678
            original_trainer = FakeOriginalTrainer()
            
            def __init__(self):
                self.nature = FakeNature()
                self.ability = FakeAbility()
                self.ivs = FakeIVs()
                self.held_item = None
                self.origin_info = {"level_met": 5}
                self.moves = [FakeLearnedMove("Scratch"), FakeLearnedMove("Growl"), None, None]
                
        fake_pokemon = FakePokemon()
        mock_pokemon_class.return_value = fake_pokemon
            
        # Mock Image.new to return a mock image
        with patch('modules.items.tcg_card.Image.new') as mock_new:
            mock_card_image = MagicMock()
            mock_new.return_value = mock_card_image
            
            # Mock ImageDraw and Font
            with patch('modules.items.tcg_card.ImageDraw.Draw') as MockDraw:
                mock_draw = MockDraw.return_value
                mock_draw.textlength.return_value = 10
                
                with patch('modules.items.tcg_card.ImageFont.truetype'):
                    with patch('os.replace'):
                            mock_card_image.save = MagicMock()
                            
                            try:
                                generate_tcg_card(b'dummy_data', "Location")
                            except Exception as e:
                                print(f"DEBUG EXCEPTION: {e}")
                                pass

        # Verify Image.open was called with the correct path
        sprite_load_found = False
        for call in mock_image_open.call_args_list:
            args, _ = call
            path_str = str(args[0])
            if "pokemon/shiny" in path_str:
                if "Torchic.png" in path_str:
                    sprite_load_found = True
                if "TORCHIC.png" in path_str:
                    self.fail("Found uppercase filename 'TORCHIC.png' - Regression detected!")
                    
        self.assertTrue(sprite_load_found, "Did not find load call for 'Torchic.png'. Only found: " + 
                        str([str(c[0][0]) for c in mock_image_open.call_args_list]))


if __name__ == '__main__':
    unittest.main()
