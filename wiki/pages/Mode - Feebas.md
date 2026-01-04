🏠 [`realbot-g3` Wiki Home](../README.md)

# 🐟 Feebas

This mode hunts for the rare Feebas by fishing on every single water tile on Route 119. Once it finds one, it stays on that tile and keeps fishing until it finds a shiny.

In Gen 3, Feebas only appears on six specific tiles. These tiles change whenever the "trendy phrase" in Dewford Town changes or after a full real-world day.

## How to use it
1. Go to Route 119 and use Surf.
2. Make sure you have a fishing rod.
3. If you have the Rain Badge and know Waterfall, the bot will also check the tiles above the waterfall. If not, it'll just skip them.

## Tips for better hunting
- **Use the Old Rod**: It's faster because encounters start as soon as you get a bite. The bot will automatically register it to your `Select` button.
- **Sticky Hold / Suction Cups**: In Emerald, put a Pokémon with one of these abilities in your first slot (it's okay if it's fainted). This will make Pokémon bite much more often.

## How the bot works
The bot fishes on each tile 3 times. If it doesn't find a Feebas after 3 bites, there's an 87.5% chance that tile isn't one of the special Feebas spots.

| Bites | Confidence |
|-------|------------|
| 1     | 50%        |
| 2     | 75%        |
| 3     | 87.5%      |
| 4     | 93.75%     |
| 5     | 96.875%    |

## Game Support
|          | 🟥 Ruby | 🔷 Sapphire | 🟢 Emerald |
|:---------|:-------:|:-----------:|:----------:|
| English  |    ✅    |      ✅      |     ✅      |
| Japanese |    ✅    |      ✅      |     ✅      |
| German   |    ✅    |      ✅      |     ✅      |
| Spanish  |    ✅    |      ✅      |     ✅      |
| French   |    ✅    |      ✅      |     ✅      |
| Italian  |    ✅    |      ✅      |     ✅      |

✅ Tested and working.
