# Copyright (c) 2026 realgarit
import time
from tkinter import Toplevel
import ttkbootstrap as ttk

from rich.prompt import IntPrompt

from modules.core.context import context
from modules.pokemon.pokemon import Pokemon
from modules.pokemon.pokemon import StatsValues
from modules.pokemon.pokemon_party import get_party


def ask_for_ev_targets(pokemon: "Pokemon") -> StatsValues:
    if context.gui.is_headless:
        return StatsValues(
            hp=IntPrompt.ask("Choose target HP EVs", default=pokemon.evs.hp),
            attack=IntPrompt.ask("Choose target Attack EVs", default=pokemon.evs.attack),
            defence=IntPrompt.ask("Choose target Defence EVs", default=pokemon.evs.defence),
            speed=IntPrompt.ask("Choose target Speed EVs", default=pokemon.evs.speed),
            special_attack=IntPrompt.ask("Choose target Special Attack EVs", default=pokemon.evs.special_attack),
            special_defence=IntPrompt.ask("Choose target Special Defence EVs", default=pokemon.evs.special_defence),
        )

    spinboxes: list[ttk.Spinbox] = []
    selected_ev_targets: StatsValues | None = None

    def remove_window(event=None):
        nonlocal window
        window.destroy()
        window = None

    def return_selection():
        nonlocal spinboxes, selected_ev_targets
        selected_ev_targets = StatsValues(
            hp=int(spinboxes[0].get()),
            attack=int(spinboxes[1].get()),
            defence=int(spinboxes[2].get()),
            speed=int(spinboxes[5].get()),
            special_attack=int(spinboxes[3].get()),
            special_defence=int(spinboxes[4].get()),
        )
        window.after(50, remove_window)

    window = Toplevel(context.gui.window)
    window.title("EV Goals")
    window.protocol("WM_DELETE_WINDOW", remove_window)
    window.bind("<Escape>", remove_window)

    # Main container with padding
    frame = ttk.Frame(window, padding=15)
    frame.grid(sticky="NSWE")
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    # Pokemon name label
    pokemon_label = ttk.Label(frame, text=get_party()[0].name, font=("TkDefaultFont", 11, "bold"))
    pokemon_label.grid(row=0, column=0, pady=10, sticky="W")

    # Stats frame
    stats_frame = ttk.Frame(frame)
    stats_frame.grid(row=1, column=0, sticky="EW")

    # Stat labels - symmetric padding
    stat_names = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
    stat_keys = ["hp", "attack", "defence", "special_attack", "special_defence", "speed"]

    for i, name in enumerate(stat_names):
        ttk.Label(stats_frame, text=name, anchor="center").grid(row=0, column=i, padx=10, pady=5)

    # Spinboxes - symmetric padding
    for i, key in enumerate(stat_keys):
        spinbox = ttk.Spinbox(stats_frame, from_=0, to=252, increment=4, wrap=True, width=6)
        spinbox.delete(0, "end")
        spinbox.insert(0, str(pokemon.evs[key]))
        spinbox.grid(row=1, column=i, padx=10, pady=5)
        spinboxes.append(spinbox)

    # Button - centered with symmetric padding
    button = ttk.Button(
        frame,
        text="Start EV Training",
        command=return_selection,
        bootstyle="success",
        cursor="hand2",
    )
    button.grid(row=2, column=0, pady=15)

    while window is not None:
        window.update_idletasks()
        window.update()
        time.sleep(1 / 60)

    return selected_ev_targets

