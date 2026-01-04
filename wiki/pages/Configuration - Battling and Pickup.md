🏠 [`realbot-g3` Wiki Home](../README.md)

# ⚔ Battling and Pickup

Edit these settings in [`profiles/battle.yml`](../../modules/config/templates/battle.yml).

The bot can automatically fight any Pokémon that doesn't match your catch rules.

## Auto Catching

`auto_catch` - Turn this on to catch shinies or anything that matches your filters.

If your lead Pokémon has False Swipe, the bot will use it. It also tries to use moves that cause sleep or paralysis when it can.

The bot will throw the best ball you have (except for Master Balls) until the Pokémon is caught.

## Pickup

`pickup` - This makes the bot check if your Pokémon found any items using the [Pickup ability](https://bulbapedia.bulbagarden.net/wiki/Pickup_(Ability)). Check out this [item list](https://bulbapedia.bulbagarden.net/wiki/Pickup_(Ability)#Items_received) to see what they can find.

`pickup_threshold` - This is how many Pokémon in your party need to be holding an item before the bot stops to take them. If you have fewer Pokémon with the Pickup ability than this number, it'll just use that smaller count instead.

`pickup_check_frequency` - How many encounters to wait between checks for items.

- If you turned on `faster_pickup` in [💎 Cheats](Configuration%20-%20Cheats.md), the bot ignores the threshold and checks every time.

## Battling

`hp_threshold` - This is the minimum HP percentage your Pokémon needs to keep fighting.

`lead_cannot_battle_action` - What to do if your lead Pokémon is too beat up (fainted or below the HP limit).
- `stop` - Stops the bot so you can take over.
- `flee` - Runs away from the fight.
- `rotate` - Switches to the next Pokémon that's healthy and has moves left.

`faint_action` - What to do if a Pokémon faints during a fight.
- `stop` - Stops the bot.
- `flee` - Runs away (but will stop the bot if it's a trainer fight).
- `rotate` - Switches to the next healthy Pokémon.

`new_move` - What to do when a Pokémon tries to learn a new move.
- `stop` - Stops the bot.
- `cancel` - Skips the new move entirely.
- `learn_best`- The bot checks your current moves. If the new move is better than your weakest one, it'll swap them. It also tries to keep a good variety of move types.

`stop_evolution` - Set to `true` to stop Pokémon from evolving (the bot will mash B). Set to `false` to let them evolve.

`switch_strategy` - Choose `first_available` to just pick the next one in line, or `lowest_level` to help level up your weaker Pokémon.

`banned_moves` - A list of moves you never want the bot to use.

`avoided_pokemon` - A list of Pokémon you want to run away from.

`targeted_pokemon` - A list of Pokémon you actually want to fight. If it's not on this list, the bot will run.
