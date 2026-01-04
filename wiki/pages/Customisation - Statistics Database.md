🏠 [`realbot-g3` Wiki Home](../README.md)

# 📊 Statistics Database

The bot keeps all its stats in a file called `stats.db`. You can find it in your profile folder: `profiles/<profile name>/stats.db`. It's a regular SQLite database with four main tables:

- **encounters**: Info on Pokémon you've run into. If you turned on `log_encounters` (see the [logging page](Console,%20Logging%20and%20Image%20Config.md)), it lists *everything*. Otherwise, it only shows shinies, roamers, and custom filter matches.
- **shiny_phases**: Details on your "phases"—the time between two shiny encounters.
- **encounter_summaries**: A total count for every species you've seen. This is where the bot looks to answer things like "How many Seedot have I found?"
- **pickup_items**: A list of items your Pokémon have found using the Pickup ability.

## How to View or Change Stats

Since this is a standard SQLite file, you can open it with any database tool. If you've never done this before, here's how to get started.

**Important: Always back up your `stats.db` file first!** If you mess something up, the bot might crash or lose your stats. If that happens, just restore your backup.

### Opening the Database

A good tool to use is [DB Browser for SQLite](https://sqlitebrowser.org/). It works on most computers.

1. **Close the bot.** Only one program can use the database file at a time.
2. Open DB Browser and click **Open Database** (or press `Ctrl + O`). Find the `stats.db` file in your profile folder.
3. Make your changes (see below for examples).
4. If you changed anything, click **Write Changes** (or press `Ctrl + S`).
5. **Close the database** in the tool. If you leave it open, the bot will give you a "Database is locked" error.

### Exporting to CSV or JSON

If you'd rather work with spreadsheets or JSON, you can export your data.
1. Go to **File** > **Export**.
2. Choose **Table(s) as CSV file...** or **Table(s) as JSON...**.
3. Pick the tables you want and save them.

### Changing Encounter Counts

If you want to manually fix your counts:
1. Right-click the `encounter_summaries` table and pick **Browse Table**.
2. Find the Pokémon you want to change and edit the numbers.
3. Don't forget to click **Write Changes** before you close the tool.
