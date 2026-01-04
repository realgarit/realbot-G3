🏠 [`realbot-g3` Wiki Home](../README.md)

# 💀 Using Unsupported ROMs

> [!CAUTION]
> Even if you follow these steps, there is a very high chance that modified ROMs (like ROM hacks) **will not work at all**, or will have broken features.
>
> **Do not ask for help on GitHub or Discord if you are using an unsupported ROM.** We simply cannot support modified games.

By default, the bot only works with original, official versions of Ruby, Sapphire, Emerald, FireRed, and LeafGreen. If use a modified ROM or a "bad dump," the bot won't recognize it.

If you still want to try it, you can manually "whitelist" your ROM so the bot lets it run.

## How to Whitelist a ROM

1. Go to your `profiles/` folder.
2. Create a new text file and name it `extra_allowed_roms.txt`.
3. Open the file and type either the **exact filename** of your ROM or its **SHA1 hash** (see below). 
4. If you have multiple ROMs, put each one on its own line. Make sure there are no spaces before or after the names/hashes.
5. Save the file and restart the bot.

## How to Find Your ROM's Hash

To get the SHA1 hash of your ROM file:
- **Windows**: Use PowerShell and run: `Get-FileHash 'rom_name.gba' -Algorithm SHA1`
- **Linux**: Run: `sha1sum 'rom_name.gba'`
- **Online**: You can use a tool like [ROM Hasher](https://www.romhacking.net/utilities/1002/).
