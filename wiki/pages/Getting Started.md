🏠 [`realbot-g3` Wiki Home](../README.md)

# ❓ Getting Started

## What You'll Need

### Windows
- [Python 3.13](https://www.python.org/downloads/windows/) (Download the **64-bit installer**).
- **Important**: Make sure you check the box that says `Add Python to PATH` when you install it.

### macOS
- [Python 3.13](https://www.python.org/downloads/macos/) (Download the **universal2 installer**) or run `brew install python@3.13`.
- mGBA 0.10.x. You can install it with `brew install mgba`. 
- For more details, see the [macOS Installation guide](/wiki/pages/MacOS%20Installation.md).

### Linux (Ubuntu/Debian/Arch)
- Python 3.13. Run `sudo apt install python3.13` (or use your package manager).
- You'll also need these packages: `sudo apt install python3-distutils python3-tk libmgba0.10 portaudio19-dev`.
- If your distro doesn't have `libmgba0.10`, you can download the `.deb` file from [mgba.io](https://mgba.io/downloads.html).

---

## Download the Bot

### Stable Version (Recommended)
Go to the [releases page](https://github.com/realgar/realbot-g3/releases) and download the **realbot-DATE.zip** file. The bot has an auto-updater, so it'll check for new versions once a day.

### Dev Version (Latest Features)
If you want the absolute latest code, you can download the ZIP from the main [GitHub page](https://github.com/realgar/realbot-g3). 

If you know how to use Git, you can also clone the repo:
`git clone https://github.com/realgar/realbot-g3.git`

---

## How to Run It

1. Put your **official** Pokémon GBA ROMs into the `roms/` folder.
2. Double-click `realbot.py` or run `python realbot.py` in your terminal.
3. The bot will automatically check and install any missing requirements the first time you run it.
4. Follow the steps on the screen to create your profile.

### Tips
- **Key Mappings**: The bot uses default mGBA keys. You can see them [here](pages/Configuration%20-%20Key%20Mappings.md).
- **Running Away**: Make sure your lead Pokémon can escape from battles 100% of the time, or the bot might get stuck. Using a Smoke Ball or a fast Pokémon is a good idea.
- **Backups**: We're still working on the bot, so things might change. Always back up your `profiles/` folder before you update!

---

## Importing a Save

If you already have a save file from mGBA:
1. Open the game in mGBA and load your save.
2. Go to **File** > **Save State File...** and save it somewhere.
3. Run the bot (`realbot.py`), type a name for your profile, and click **Load Existing Save**.
4. Pick the save state file you just made. The bot will create a new profile and start running.

---

## Advanced Options

If you want to run the bot with specific settings from the terminal:

```text
python realbot.py [profile_name] [options]
```

### Common Options:
- `-d` or `--debug`: Opens a debug menu with extra info.
- `-m [MODE]`: Starts the bot in a specific mode (like `Spin` or `Fishing`).
- `-s [SPEED]`: Sets the initial speed (1x, 2x, etc.). Use `0` for unthrottled speed.
- `-nv`: Starts with video turned off.
- `-na`: Starts with audio turned off.
