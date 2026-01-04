🏠 [`realbot-g3` Wiki Home](../README.md)

# 💎 Cheats

Edit these settings in [`profiles/cheats.yml`](../../modules/config/templates/cheats.yml).

These settings let the bot do things a human can't. This includes things like peeking inside eggs to see if they're shiny, knowing exactly where a roaming Pokémon is, or finding Feebas tiles instantly.

> We're planning to add even more cheats later, like injecting healing at a Pokémon Center. By default, everything is turned off. We might even add more sophisticated RNG manipulation options in the future.

`random_soft_reset_rng` - This helps the bot find unique Pokémon when soft-resetting.
- It stops the bot from getting slower over time by removing the wait for new frames.
- In Gen 3, the way the game picks random numbers is very predictable. Without this setting, you might keep running into the exact same Pokémon every time you reset. If you want the technical details, you can read more [here](https://blisy.net/g3/frlg-starter.html) and [here](https://www.smogon.com/forums/threads/rng-manipulation-in-firered-leafgreen-wild-pok%C3%A9mon-supported-in-rng-reporter-9-93.62357/).

`faster_pickup` - If you're using Pickup mode, this lets the bot check your party's items instantly by reading the game's memory. This is much faster than opening the menu every time.
