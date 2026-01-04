# RealBot G3
[![Wiki](wiki/images/badge_wiki.svg)](wiki/Readme.md) [![Python 3.12](wiki/images/badge_python.svg)](https://www.python.org/downloads/release/python-3132/) [![Code Formatting](wiki/images/badge_black.svg)](https://github.com/psf/black)

**RealBot G3** is a shiny hunting bot, written in Python that runs `libmgba` + mGBA Python bindings under the hood. Pokémon Ruby, Sapphire, Emerald, FireRed and LeafGreen are supported.

# ❓ Getting Started

Visit the [wiki](wiki/Readme.md) for information:
- ❓ [Getting Started](wiki/pages/Getting%20Started.md)
- 🎮 [Emulator Input Mapping](wiki/pages/Configuration%20-%20Key%20Mappings.md)
- 🔎 [Pokémon by Bot Mode](wiki/pages/Pokemon%20By%20Bot%20Mode.md)

# 😎 Showcase

|              Main interface              |              Load save state              |              Debug mode              |
|:----------------------------------------:|:-----------------------------------------:|:------------------------------------:|
| ![image](wiki/images/main_interface.png) | ![image](wiki/images/load_save_state.png) | ![image](wiki/images/debug_mode.png) |

| Shiny encounter GIFs            | 
|---------------------------------|
| ![image](wiki/images/shiny.gif) |

|             Discord shiny notifications              |              Discord phase stats              |              Discord milestones              |
|:----------------------------------------------------:|:---------------------------------------------:|:--------------------------------------------:|
| ![image](wiki/images/discord_shiny_notification.png) | ![image](wiki/images/discord_phase_stats.png) | ![image](wiki/images/discord_milestones.png) |

| Automatically saves PKHeX .pk3 file | HTTP API                           |
|-------------------------------------|------------------------------------|
| ![image](wiki/images/pk3_files.png) | ![image](wiki/images/http_api.png) |

# ❤ Attributions

Based on:

- [PokéBot Gen3](https://github.com/40Cakes/pokebot-gen3) by 40_Cakes

Core functionality:

- [mGBA](https://github.com/mgba-emu/mgba)
- [libmgba-py](https://github.com/hanzi/libmgba-py/)

Other awesome PokéBot projects:

- [PokéBot NDS](https://github.com/wyanido/pokebot-nds/)

Decompiled symbol tables and other various data from the following projects:

- [Pokémon Emerald decompilation](https://github.com/pret/pokeemerald) ([symbols](https://github.com/pret/pokeemerald/tree/symbols))
- [Pokémon Ruby and Sapphire decompilation](https://github.com/pret/pokeruby) ([symbols](https://github.com/pret/pokeruby/tree/symbols))
- [Pokémon FireRed and LeafGreen decompilation](https://github.com/pret/pokefirered) ([symbols](https://github.com/pret/pokefirered/tree/symbols))