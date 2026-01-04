# Copyright (c) 2026 realgarit
from typing import Generator

from modules.core.context import context
from modules.core.debug import debug
from modules.game.memory import read_symbol


def _select_in_menu(cursor_symbol: str, target_index: int, use_third_byte: bool = False) -> Generator:
    if target_index < 0 or target_index > 3:
        raise ValueError(f"Menu index must be a number between 0 and 3. '{target_index}' given.")

    first_iteration = True
    while True:
        current_index = read_symbol(cursor_symbol, size=4)

        # Double battles use the 3rd byte for the Pokémon on the right side.
        # Everything else uses the 1st byte.
        if use_third_byte:
            current_index = current_index[2]
        else:
            current_index = current_index[0]

        if current_index == target_index:
            # If the cursor is already where it needs to be, we might still need to wait a frame.
            # It's an edge case, but waiting makes sure the UI is ready for the next input.
            if first_iteration:
                yield
            break
        else:
            if current_index in (1, 3) and target_index in (0, 2):
                context.emulator.press_button("Left")
            elif current_index in (0, 2) and target_index in (1, 3):
                context.emulator.press_button("Right")
            elif current_index > 1 and target_index <= 1:
                context.emulator.press_button("Up")
            else:
                context.emulator.press_button("Down")
        yield
        yield
        first_iteration = False


@debug.track
def scroll_to_battle_action(action_index: int) -> Generator:
    yield from _select_in_menu("gActionSelectionCursor", action_index)


@debug.track
def scroll_to_move(move_index: int, is_right_side_pokemon: bool = False) -> Generator:
    yield from _select_in_menu("gMoveSelectionCursor", move_index, is_right_side_pokemon)
