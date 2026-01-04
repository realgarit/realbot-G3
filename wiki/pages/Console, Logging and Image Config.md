🏠 [`realbot-g3` Wiki Home](../README.md)

# 📄 Console, Logging, and Images

Edit these settings in [`profiles/logging.yml`](../../modules/config/templates/logging.yml).

Use this file to turn features on or off. This includes things like data logging, saving Pokémon files (.pk3), or making shiny GIFs.

## Logging

### Options

`log_encounters` - Set this to `true` to log *every* encounter to the stats database, not just shinies.
- It doesn't really slow the bot down, but the database file (`profiles/<profile name>/stats.db`) will get big fast.
- Every encounter adds about 200 bytes. After a million encounters, the file will be around 190 MB.

`desktop_notifications` - Shows a pop-up on your desktop when the bot finds a shiny, a roamer, or something that matches your custom filters. It also pings you if the bot switches to manual mode.

`log_encounters_to_console` - Shows info about wild encounters and your current stats in the console window.

## Saving Pokémon Data (.pk3)

The bot can save individual Pokémon files in `.pk3` format. You can use these with the [PKHeX save editor](https://github.com/kwsch/PKHeX) to move them between games.

These files are saved in `./profile/<profile_name>/stats/pokemon/`. Here's what the filename looks like:
`273 ★ - SEEDOT - Modest [180] - C88CF14B19C6.pk3`

### Options

`save_pk3` - Set these to `true` or `false`:
- `shiny` - Save a file for every shiny you find.
- `custom` - Save a file for anything that matches your custom catch filters.
- `roamer` - Save a file for roaming Pokémon (like Latios or Entei) the first time you see them.

Feel free to share your cool finds in the [#pkhexchange](https://discord.com/channels/1057088810950860850/1123523909745135616) Discord channel!

## Shiny GIFs

The bot can record a short GIF of every shiny encounter. If you have [Discord webhooks](Configuration%20-%20Discord%20Integration.md) set up, it'll post the GIF there too.

GIFs are saved in `./profile/<profile_name>/screenshots/gif/`.

`shiny_gifs` - Turn this on or off.

![image](../images/shiny.gif)

## TCG Cards

This creates a fun (fake) TCG card for every shiny encounter or evolution.

Cards are saved in `./profile/<profile_name>/screenshots/cards/`.

- The card's color matches the Pokémon's main type.
- You'll see stars in the top right for shinies.
- The shape in the top right tells you which game it came from:
  - Blue/Red/Green square: S/R/E.
  - Orange/Green circle: FR/LG.
- The National Dex number is at the bottom right of the picture.
- The blue bar shows how good the Pokémon's stats are (IVs).

`tcg_cards` - Turn this on or off.

![image](../images/tcg_example.png)
