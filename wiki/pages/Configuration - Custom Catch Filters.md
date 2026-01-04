🏠 [`realbot-g3` Wiki Home](../README.md)

# 🥅 Custom Catch Filters

Edit these settings in [`profiles/customcatchfilters.py`](../../modules/config/templates/customcatchfilters.py).

The bot checks every Pokémon you run into against these filters. Use this file if you're looking for something very specific. I've included a few examples in the file to get you started.

Most examples are turned off (they have a `#` at the start) so you don't waste Poké Balls. However, I left a few rare ones on by default, like Pokémon with perfect IVs, all zero IVs, or six identical IVs.

These filters run *after* the catch block list. So, if you block Wurmple but have a filter for a specific Wurmple evolution, the bot will still check it.

- ✅ `return "your message"` - Tell the bot to catch the Pokémon. If you use Discord, this message will show up in the webhook.
- 💾 `save_pk3(pokemon)` - This [saves a .pk3 file](Console,%20Logging%20and%20Image%20Config.md) of the Pokémon.

If you don't know Python, I'd suggest using [VS Code](https://code.visualstudio.com/) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python). It'll help you spot mistakes and even suggest what you can filter for.

If you *do* know Python, you can see all the settings you can check in the [pokemon.py](../../modules/pokemon.py) file.

### Examples

Here's how to catch a shiny Wurmple that evolves into Silcoon/Beautifly, while ignoring the ones that become Cascoon:

```python
# Shiny Wurmple that will evolve into Silcoon
if pokemon.is_shiny and pokemon.species.name == "Wurmple":
    if pokemon.wurmple_evolution == "silcoon":
        return "Shiny Wurmple evolving into Silcoon/Beautifly"
```

And here's how to catch anything with perfect IVs:

```python
# Pokémon with perfect IVs
if pokemon.ivs.sum() == (6 * 31):
    return "Pokémon with perfect IVs"
```

- **Note**: You **must** restart the bot for any changes here to work! Unlike other settings, just hitting `Ctrl + C` to reload won't update `.py` files.
