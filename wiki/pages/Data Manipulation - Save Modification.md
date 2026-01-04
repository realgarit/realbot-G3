# 💾 Save Modification

> ⚠️ **Warning**: You can only use this feature in debug mode. Start the bot with the `--debug` option to see it.

Save modification lets you export and import your "event flags" and "variables." These are a way to keep track of your progress in the game.

---

## Why Use This?

This is really handy if you need to move your progress between different save files. For example:
- If you're switching from a US save to a Japanese ROM, you can't just copy the save file. Instead, you can:
    - Export your progress flags and variables from the US save.
    - Start a new game on the Japanese ROM.
    - Import your flags and variables to jump back to where you were.

### Things to Watch Out For

1. **It Doesn't Copy Everything**:
    - This only copies your **game progress**. It won't move your Pokémon, items, TM/HMs, or Poké Balls. You'll need to use a save editor like PKHeX for those.

2. **Soft Lock Risk**:
    - If you import endgame progress into a brand new save, you might get stuck (a "soft lock"). For example, if the game thinks you've finished the story but you don't have a Pokémon or any HMs, you won't be able to go anywhere.

3. **Editing the Files**:
    - You can manually edit the exported `event_flags.txt` and `event_vars.txt` files if you need to fine-tune things or fix a soft lock.

---

## How to Use It

### Exporting Your Progress
1. Open the **Data Manipulation** menu in the bot.
2. Choose **Export events and vars**.
3. Your progress will be saved into text files in your profile folder.

### Importing Your Progress
1. Open the **Data Manipulation** menu.
2. Choose **Import events and vars**.
3. The bot will load the data into the current game.
4. **Save your game** in the menu.
5. Reset the game or restart the bot to make sure everything updates.

---

## The Files

When you export your progress, the bot creates these files:

1. **event_flags.txt** (`profiles/event_flags.txt`)
    - These are simple "on/off" switches for things you've done in the game (like beating a gym).
2. **event_vars.txt** (`profiles/event_vars.txt`)
    - These are numbers that track things like how many times you've talked to someone or where you are in a specific quest.