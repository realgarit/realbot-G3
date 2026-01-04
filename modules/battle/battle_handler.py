# Copyright (c) 2026 realgarit
from typing import Generator, TYPE_CHECKING

from modules.battle.battle_action_selection import handle_battle_action_selection
from modules.pokemon.battle_evolution_scene import handle_evolution_scene
from modules.battle.battle_move_replacing import handle_move_replacement_dialogue
from modules.battle.battle_state import (
    battle_is_active,
    get_main_battle_callback,
    get_current_battle_script_instruction,
    BattlePokemon,
    get_battle_state,
)
from modules.battle.battle_strategies import BattleStrategy
from modules.core.context import context
from modules.core.debug import debug
from modules.game.keyboard import handle_naming_screen
from modules.game.memory import get_game_state, GameState
from modules.menus.menuing import scroll_to_party_menu_index
from modules.core.plugins import plugin_should_nickname_pokemon
from modules.pokemon.pokemon_party import get_party, get_party_size
from modules.core.tasks import task_is_active

if TYPE_CHECKING:
    from modules.pokemon.encounter import EncounterInfo


@debug.track
def handle_battle(strategy: BattleStrategy) -> Generator:
    """
    This is the main loop for handling battles. It keeps the battle moving and
    asks the battle strategy what to do whenever a decision comes up.

    :param strategy: The set of rules for making battle decisions.
    """
    while battle_is_active() and context.bot_mode != "Manual":
        instruction = get_current_battle_script_instruction()
        if get_main_battle_callback() in ("HandleTurnActionSelectionState", "sub_8012324"):
            yield from handle_battle_action_selection(strategy)
        elif instruction == "BattleScript_AskToLearnMove":
            yield from handle_move_replacement_dialogue(strategy)
        elif task_is_active("Task_EvolutionScene"):
            yield from handle_evolution_scene(strategy)
        elif (
            (instruction == "BattleScript_HandleFaintedMon" or task_is_active("Task_HandleChooseMonInput"))
            and get_battle_state().own_side.is_fainted
            and len(get_party().non_fainted_pokemon) > 0
        ):
            yield from handle_fainted_pokemon(strategy)
        elif instruction in ("BattleScript_TryNicknameCaughtMon", "BattleScript_CaughtPokemonSkipNewDex"):
            yield from handle_nickname_caught_pokemon(context.stats.last_encounter)
        else:
            context.emulator.press_button("B")
            yield


@debug.track
def handle_fainted_pokemon(strategy: BattleStrategy):
    fainted_pokemon: BattlePokemon | None = None
    battle_state = get_battle_state()
    if battle_state.own_side.left_battler is None or battle_state.own_side.left_battler.current_hp == 0:
        fainted_pokemon = battle_state.own_side.left_battler
    elif battle_state.is_double_battle and (
        battle_state.own_side.right_battler is None or battle_state.own_side.right_battler.current_hp == 0
    ):
        fainted_pokemon = battle_state.own_side.right_battler

    if fainted_pokemon is None:
        # I'm not sure if this can actually happen, but I'm keeping the check just in case.
        context.message = "fainted_pokemon was None"
        context.debug_stepping_mode()
        # context.emulator.press_button("B")
        # for _ in range(180):
        #     yield
        return

    if not battle_state.is_trainer_battle:
        if strategy.should_flee_after_faint(battle_state):
            if context.bot_mode != "Manual":
                while (
                    battle_is_active()
                    and get_current_battle_script_instruction() != "BattleScript_FaintedMonEnd"
                    and get_game_state() != GameState.PARTY_MENU
                    and get_main_battle_callback() != "HandleEndTurn_FinishBattle"
                ):
                    context.emulator.press_button("B")
                    yield

                if battle_is_active() and get_main_battle_callback() == "HandleEndTurn_FinishBattle":
                    while get_main_battle_callback() == "HandleEndTurn_FinishBattle":
                        context.emulator.press_button("B")
                        yield
                    return

    new_lead_index = strategy.choose_new_lead_after_faint(battle_state)

    # If we're not in the party menu yet, the game is still using the normal overworld party order.
    # We'll need to map the new index to the in-battle order later. If we're already in the menu,
    # then `get_party()` is already using the correct in-battle order.
    #
    # Usually, we're outside the menu if the strategy just picked the next Pokémon during the dialogue.
    # We're inside the menu if we tried to run away but failed, since the game forces the menu open then.
    index_needs_mapping = get_game_state() != GameState.PARTY_MENU

    if context.bot_mode == "Manual":
        yield
        return

    if new_lead_index < 0 or new_lead_index >= get_party_size():
        raise RuntimeError(f"Cannot send out party index #{new_lead_index} because that does not exist.")

    new_lead = get_party()[new_lead_index]
    if new_lead.is_egg:
        raise RuntimeError(f"Cannot send out party index #{new_lead_index} because it is an egg.")
    if new_lead.current_hp <= 0:
        raise RuntimeError(f"Cannot send out {new_lead.name} (#{new_lead_index}) because it has 0 HP.")

    while (
        battle_is_active()
        and get_current_battle_script_instruction() != "BattleScript_FaintedMonEnd"
        and not task_is_active("Task_HandleChooseMonInput")
        and not task_is_active("HandleBattlePartyMenu")
    ):
        context.emulator.press_button("A")
        yield

    # This happens if the battle ends right as your Pokémon faints—like from using Explosion
    # or taking too much recoil damage on a winning hit. The game just ends the battle
    # instead of asking for a new Pokémon.
    if get_current_battle_script_instruction() == "BattleScript_FaintedMonEnd":
        return

    if index_needs_mapping:
        new_lead_index = battle_state.map_battle_party_index(new_lead_index)

    yield from scroll_to_party_menu_index(new_lead_index)
    while get_game_state() == GameState.PARTY_MENU:
        context.emulator.press_button("A")
        yield


@debug.track
def handle_nickname_caught_pokemon(encounter: "EncounterInfo"):
    nickname_choice = plugin_should_nickname_pokemon(encounter)
    if nickname_choice:
        yield from handle_naming_screen(nickname_choice)

    # Skip the nicknaming dialogue.
    while get_current_battle_script_instruction() in (
        "BattleScript_TryNicknameCaughtMon",
        "BattleScript_CaughtPokemonSkipNewDex",
    ):
        context.emulator.press_button("B")
        yield
