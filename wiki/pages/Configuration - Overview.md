🏠 [`realbot-g3` Wiki Home](../README.md)

# 🛠 Configuration

Everything specific to your bot—like save games, screenshots, and stats—lives in its own folder under `./profiles/<profile name>/`. The bot creates this folder for you when you make a new profile.

You can find your encounter stats in `./profiles/<profile name>/stats/totals.json`.

## How Settings Work

If you want to change how a specific profile works, just copy the config file into that profile's folder. If a file isn't in your profile folder, the bot just uses the default one from the main `profiles` folder.

Most settings use `yml` files. The bot checks these when it starts up to make sure everything looks right. If you change a file while the bot is running, you'll need to reload it (the default key is `Ctrl + C`).

Each config page in this wiki goes into detail about what every setting does and what the defaults are.

### Example Folder Structure:

```text
├── /profiles
    │
    ├── /emerald-profile
    │     current_save.sav
    │     current_state.ss1
    │     discord.yml          <-- Settings just for 'emerald-profile'
    │     logging.yml          <-- Settings just for 'emerald-profile'
    │
    ├── /firered-profile
    │     current_save.sav
    │     current_state.ss1
    │     logging.yml          <-- Settings just for 'firered-profile'
    │
    │ catch_block.yml          <-- Settings used by everyone
    │ cheats.yml               <-- Settings used by everyone
    │ customcatchfilters.py    <-- Settings used by everyone
    │ discord.yml              <-- Settings used by everyone except 'emerald-profile'
    │ logging.yml              <-- Settings used by everyone except 'emerald' and 'firered'
```
