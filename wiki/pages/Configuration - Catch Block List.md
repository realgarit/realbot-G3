🏠 [`realbot-g3` Wiki Home](../README.md)

# ❌ Catch Block List

Edit these settings in [`profiles/catch_block.yml`](../../modules/config/templates/catch_block.yml).

The block list lets you skip certain shinies. This is helpful if you don't want to fill your PC with common shinies you've already caught a dozen times.

### A few things to know:

- Even if you skip a shiny, the bot still resets your phase stats.
- You can update this list while the bot is running. It reloads the file every time it runs into a shiny, so your changes take effect immediately.
- To add Nidoran, use `Nidoran♀` or `Nidoran♂`.
- For Unown, you can block specific forms like `Unown (F)` or `Unown (?)`. If you want to skip all Unowns, just use `Unown`.

`block_list` - List the Pokémon you want to skip here (one per line).

Example:

```yaml
block_list:
  - Poochyena
  - Pidgey
  - Rattata
  - Nidoran♀
  - Unown (F)
```
