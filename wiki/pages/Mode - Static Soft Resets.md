🏠 [`realbot-g3` Wiki Home](../README.md)

# ♻ Static Soft Resets

This mode is for hunting legendary Pokémon (like Mewtwo, Rayquaza, or Snorlax) using soft-resets. The bot will talk to the Pokémon, check if it's shiny, and then reset if it isn't.

The bot tracks the game's internal timer (RNG) to make sure you're hitting a different "frame" every time. This prevents you from seeing the same Pokémon over and over. Because of this, resets will get slightly longer as you do more of them.

**Tip**: If resets are taking too long, consider starting a new save to change your Trainer ID, or look at the `random_soft_reset_rng` option in [Cheats](Configuration%20-%20Cheats.md).

## How to use it
In most cases, just stand facing the Pokémon and start the bot. Make sure you **save your game** (in-game, not a save state) first.

### Specific Locations
- **Kyogre (Sapphire Only)**: Stand in the Cave of Origin, facing the tile *just before* the fight starts.
- **Groudon (Ruby Only)**: Stand in the Cave of Origin, facing the tile *just before* the fight starts.
- **Latias/Latios (Southern Island)**: Stand in front of the egg on the island.

## Game Support
|          | 🟥 Ruby | 🔷 Sapphire | 🟢 Emerald | 🔥 FireRed | 🌿 LeafGreen |
|:---------|:-------:|:-----------:|:----------:|:----------:|:------------:|
| English  |    ✅    |      ✅      |     ✅      |     ✅      |      ✅       |
| Japanese |    ✅    |      ✅      |     ✅      |     ✅      |      ✅       |
| German   |    ✅    |      ✅      |     ✅      |     ✅      |      ✅       |
| Spanish  |    ✅    |      ✅      |     ✅      |     ✅      |      ✅       |
| French   |    ✅    |      ✅      |     ✅      |     ✅      |      ✅       |
| Italian  |    ✅    |      ✅      |     ✅      |     ✅      |      ✅       |

✅ Tested and working.
