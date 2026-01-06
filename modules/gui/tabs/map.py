# Copyright (c) 2026 realgarit
import contextlib
import tkinter
from tkinter import Canvas, ttk
from typing import TYPE_CHECKING

from PIL import ImageTk

from modules.core.context import context
from modules.gui.emulator_controls import DebugTab
from modules.gui.tabs.utils import FancyTreeview, MapViewer
from modules.map.map import (
    EffectiveWildEncounter,
    WildEncounter,
    get_effective_encounter_rates_for_current_map,
    get_map_data,
    get_map_objects,
    get_wild_encounters_for_map,
)
from modules.map.map_data import MapFRLG, MapGroupFRLG, MapGroupRSE, MapRSE, get_map_enum
from modules.map.map_path import Direction, _find_tile_by_local_coordinates
from modules.game.memory import game_has_started
from modules.player.player import TileTransitionState, get_player_avatar

if TYPE_CHECKING:
    from modules.game.libmgba import LibmgbaEmulator


class MapTab(DebugTab):
    _tv: FancyTreeview
    _map: MapViewer

    def __init__(self, canvas: Canvas):
        self._canvas = canvas
        self._map: MapViewer | None = None
        self._tv: FancyTreeview | None = None
        self._selected_tile: tuple[int, int] | None = None

    def draw(self, root: ttk.Notebook):
        frame = ttk.Frame(root, padding=10)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self._map = MapViewer(frame, row=0, column=0)
        self._tv = FancyTreeview(frame, row=0, column=1, on_highlight=self._handle_selection)
        root.add(frame, text="Map")

    def update(self, emulator: "LibmgbaEmulator"):
        if not game_has_started():
            with contextlib.suppress(tkinter.TclError, RuntimeError):
                self._tv.update_data({"": "Game has not been started yet."})
            return

        self._map.update()

        try:
            player_location = get_player_avatar().local_coordinates
            show_different_tile = False
            # If the user is hovering over the map component, we want to show the tile being hovered over.
            if self._map._map == self._map._root.nametowidget(self._map._root.winfo_pointerxy()[1]):
                x = self._map._map.winfo_pointerx() - self._map._map.winfo_rootx()
                y = self._map._map.winfo_pointery() - self._map._map.winfo_rooty()
                # The map is 150x150, but the internal bitmap is (width * 8) x (height * 8).
                # The map is drawn with AspectRatio.retain, so we need to figure out which tile the user is hovering over.
                # Since the map is centered, we can figure out the offset.
                map_width = self._map._map.image.width()
                map_height = self._map._map.image.height()
                offset_x = (150 - map_width) // 2
                offset_y = (150 - map_height) // 2
                # If the user clicks within the map
                if offset_x <= x < offset_x + map_width and offset_y <= y < offset_y + map_height:
                    relative_x = x - offset_x
                    relative_y = y - offset_y
                    scale_x = map_width / (self._map.image.width() / MapViewer.TILE_SIZE)
                    scale_y = map_height / (self._map.image.height() / MapViewer.TILE_SIZE)
                    col = int(relative_x / scale_x)
                    row = int(relative_y / scale_y)
                    self._selected_tile = (col, row)
                    show_different_tile = True
        except Exception:
            pass

        if not show_different_tile and self._selected_tile is not None:
            # If the user is NOT hovering over the map, but previously selected a tile (by clicking on the video output)
            # then show that tile.
            player_location = self._selected_tile
            show_different_tile = True

        self._tv.update_data(self._get_data(show_different_tile))
        if show_different_tile:
            # Revert the selected tile to the player location so that the next update shows the player location again.
            self._selected_tile = None

    def on_video_output_click(self, click_location: tuple[int, int], scale: int):
        canvas_width = int(self._canvas["width"])
        canvas_height = int(self._canvas["height"])

        x, y = click_location
        # 240x160 is the GBA resolution
        x_scaling = canvas_width / 240
        y_scaling = canvas_height / 160

        x = int(x / x_scaling)
        y = int(y / y_scaling)

        # The player is always at the center of the screen (approx 120, 80)
        # The tiles are 16x16 pixels
        x_offset = (x - 120) // 16
        y_offset = (y - 88) // 16  # 80 + 8 (player is 16x24, center is slightly lower)

        player_location = get_player_avatar().local_coordinates
        self._selected_tile = (player_location[0] + x_offset, player_location[1] + y_offset)
        # Select the 'Map' tab
        self._tv._tv.nametowidget(self._tv._tv.winfo_parent()).master.master.select(3)  # 3 is the index of the Map tab

    def _get_data(self, show_different_tile: bool):
        player_avatar = get_player_avatar()
        player_location = player_avatar.local_coordinates
        if show_different_tile and self._selected_tile:
            player_location = self._selected_tile

        # get_map_data returns a MapLocation for the specific tile at player_location
        current_map = get_map_data(player_avatar.map_group_and_number, player_location)
        if current_map is None:
            return {"Error": "Map data not found"}

        map_objects_data = {}
        all_objects = get_map_objects()
        matching_objects = [obj for obj in all_objects if obj.current_coords == player_location]
        
        for i, obj in enumerate(matching_objects):
            # Try to get template info for more details
            template = None
            with contextlib.suppress(Exception):
                template = obj.object_event_template

            map_objects_data[f"Object #{i + 1}"] = {
                "__value": f"ID {obj.local_id} at ({obj.current_coords[0]}, {obj.current_coords[1]})",
                "Type": f"Graphics ID {obj.graphics_id}",
                "Coordinates": self.format_coordinates(obj.current_coords),
                "Movement Type": obj.movement_type,
                "Trainer Type": obj.trainer_type,
                "Local ID": obj.local_id,
            }
            if template:
                map_objects_data[f"Object #{i + 1}"].update({
                    "Script": template.script_symbol,
                    "Flag ID": template.flag_id,
                    "Trainer Range": template.trainer_range if template.trainer_type != "None" else "N/A",
                })

        # Filter encounters to only show those relevant to the current tile
        map_group, map_num = player_avatar.map_group_and_number
        encounters = get_wild_encounters_for_map(map_group, map_num)
        
        def list_encounters(encounter_list: list[WildEncounter], rate: int):
            if not encounter_list or rate == 0:
                return {"__value": "None"}
            
            result = {"__value": f"{rate}%"}
            for encounter in encounter_list:
                label = f"{encounter.species.name} (Lv. {encounter.min_level}"
                if encounter.min_level != encounter.max_level:
                    label += f"-{encounter.max_level}"
                label += ")"
                result[label] = f"{encounter.encounter_rate}%"
            return result
        
        def list_effective_encounters(label: str, encounters_list: list[EffectiveWildEncounter]):
             if not encounters_list:
                 return {label: {"__value": "None"}}
             
             total_rate = sum(e.encounter_rate for e in encounters_list)
             data = {"__value": f"{total_rate:.2f}%"}
             for e in encounters_list:
                 label_text = f"{e.species.name} (Lv. {e.min_level}"
                 if e.min_level != e.max_level:
                     label_text += f"-{e.max_level}"
                 label_text += ")"
                 data[label_text] = f"{e.encounter_rate:.2f}%"
             return {label: data}

        land_encounters = list_encounters(encounters.land_encounters, encounters.land_encounter_rate) if encounters else {"__value": "None"}
        water_encounters = list_encounters(encounters.surf_encounters, encounters.surf_encounter_rate) if encounters else {"__value": "None"}
        rock_smash_encounters = list_encounters(encounters.rock_smash_encounters, encounters.rock_smash_encounter_rate) if encounters else {"__value": "None"}
        
        fishing_data = {"__value": f"{encounters.fishing_encounter_rate}%" if encounters else "None"}
        if encounters:
            fishing_data.update({
                "Old Rod": list_encounters(encounters.old_rod_encounters, encounters.fishing_encounter_rate),
                "Good Rod": list_encounters(encounters.good_rod_encounters, encounters.fishing_encounter_rate),
                "Super Rod": list_encounters(encounters.super_rod_encounters, encounters.fishing_encounter_rate),
            })

        map_enum = get_map_enum((map_group, map_num))
        map_name = map_enum.name if map_enum else "Unknown"

        # Use dict_for_tile() as a base but augment it
        tile_info = current_map.dict_for_tile()
        
        data = {
            "Map": {
                "__value": f"{map_name} ({map_group}, {map_num})",
                "Group": map_group,
                "Number": map_num,
                "Name": map_name,
                "Width": current_map.map_size[0],
                "Height": current_map.map_size[1],
            },
            "Tile": {
                 "__value": f"({player_location[0]}, {player_location[1]})",
                 "X": player_location[0],
                 "Y": player_location[1],
                 "Elevation": tile_info["elevation"],
                 "Type": tile_info["type"],
                 "Collision": bool(tile_info["collision"]),
                 "Encounter Type": {"__value": "Yes" if tile_info["has_encounters"] else "No"},
                 "Is Surfable": "Yes" if tile_info["is_surfing_possible"] else "No",
            },
            "Objects": {"__value": f"{len(matching_objects)} Objects", **map_objects_data},
            "Encounters": {
                "__value": "Rates",
                "Land": land_encounters,
                "Water": water_encounters,
                "Fishing": fishing_data,
                "Rock Smash": rock_smash_encounters,
            },
        }
        
        if show_different_tile:
            data["Tile"]["__value"] += " (Selected)"

        if not show_different_tile:
             effective = get_effective_encounter_rates_for_current_map()
             if effective:
                 data["Effective Encounters"] = {
                     "__value": f"Repel Lv. {effective.repel_level}",
                     **list_effective_encounters("Land", effective.land_encounters),
                     **list_effective_encounters("Surfing", effective.surf_encounters),
                     **list_effective_encounters("Old Rod", effective.old_rod_encounters),
                     **list_effective_encounters("Good Rod", effective.good_rod_encounters),
                     **list_effective_encounters("Super Rod", effective.super_rod_encounters),
                     **list_effective_encounters("Rock Smash", effective.rock_smash_encounters),
                 }
        
        return data

    def format_coordinates(self, coordinates: tuple[int, int]):
        return f"({coordinates[0]}, {coordinates[1]})"

    def _handle_selection(self, selected_label: str):
        pass
