🏠 [`realbot-g3` Wiki Home](../README.md)

# ❓ General FAQ

Here are the most common questions about the bot, how it works, and basic game terms.

## Glossary

### Phase
Shiny hunters use this term to describe how many Pokémon they've seen since their last shiny. If you found a shiny Wurmple after 8,000 encounters, you "phased," and your counter starts over at zero.

### SV (Shiny Value)
This is a number between `0` and `65,535`. In Gen 3, if this number is **8 or lower**, the Pokémon is shiny.

### TID and SID (Trainer ID and Secret ID)
These are your hidden IDs. The game uses them along with a Pokémon's data to decide if it's shiny.

### PID (Personality ID)
Every Pokémon has a unique PID. It determines everything from its gender and nature to whether it's shiny.

---

## Bot Mechanics

### Why does the bot use specific Pokémon in the lead?
- **Speed**: Pokémon with short cries (like Lotad) save a tiny bit of time on every encounter.
- **Running Away**: In caves, the bot can run faster if your lead Pokémon is a lower level than the wild one. For example, using a low-level Pokémon with a Smoke Ball to make sure we never get stuck.

### What are 'Illuminate' and 'White Flute'?
- **Illuminate**: This ability doubles how many Pokémon you run into.
- **White Flute**: An item that does the same thing.
Using both together means you find Pokémon much faster.

### Does the bot catch every shiny?
**Yes.** The bot is built to catch every shiny it sees.

### Will the bot use the Repel Trick?
**Yes.** If you have a lead Pokémon at a certain level and use a Repel, the game will only spawn Pokémon at that level or higher. This is a great way to target specific rare spawns. It works in both `spin` and `bunny hop` modes.

---

## Random Odds

- **Shiny Odds**: 1 in 8,192. (There’s no Shiny Charm in Gen 3!)
- **Pokérus**: 1 in 21,845.
- **6 Perfect IVs**: 1 in 1,073,741,824.
- **Shiny with 6 Perfect IVs**: 1 in 8,796,093,000,000.

---

## Seedot Facts

People ask about this all the time.

### How rare is it?
Seedot is a **1% encounter**. Your chance of finding a shiny one is **1 in 819,200**. It's just as rare everywhere it spawns, so there's no way to make it easier.

### What about the in-game trade?
The Seedot you get in the trade is called DOTS. He is **never shiny**. His stats and PID are locked by the game, so he will always be the exact same non-shiny Pokémon.
