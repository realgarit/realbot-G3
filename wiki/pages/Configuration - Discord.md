🏠 [`realbot-g3` Wiki Home](../README.md)

# 📢 Discord

Edit these settings in [`profiles/discord.yml`](../../modules/config/templates/discord.yml).

You can connect the bot to Discord to get pings for shinies, see your stats, or get updates on how your hunt is going.

For privacy, everything is **turned off** by default.

## Discord Rich Presence

- `rich_presence`: This shows what the bot is doing on your Discord profile (like what route it's on or how many encounters it's at).
  - You need to have Discord open on the same computer.
  - Only turn this on for one bot at a time, or Discord might get confused.

## Discord Webhooks

- `global_webhook_url`: This is the main link for your Discord channel.
  - To get one: Go to **Channel Settings** > **Integrations** > **Webhooks** > **New Webhook**.
  - ⚠ **Careful**: Don't share this URL with anyone. If they have it, they can post whatever they want to your channel.

- `delay`: How many seconds to wait before posting. This is handy if you're streaming and don't want to spoil a shiny before it shows up on screen.

- `bot_id`: A name for your bot that shows up at the bottom of messages. This helps if you're running a few bots and want to know which one is talking.

### Setting up Webhooks

- `enable`: Switch this to `true` or `false` to turn the webhook on or off.

- `webhook_url`: If you want a specific update (like shinies) to go to a different channel, put that URL here. It'll ignore the global one.

- `ping_mode`: Set this to `user` or `role` if you want the bot to ping you. Leave it blank if you want it to stay quiet.

- `ping_id`: The ID for the person or role you want to ping.
  - To get this, you'll need Developer Mode on in Discord. Then just right-click a user or role and hit **Copy ID**.

### Message Types

- `shiny_pokemon_encounter`: Pings you when a shiny shows up.

- `blocked_shiny_encounter`: Pings you when the bot hits a shiny that's on your [block list](Configuration%20-%20Catch%20Block%20List.md).

- `pokemon_encounter_milestones`: Updates you every few encounters (like every 1,000).

- `shiny_pokemon_encounter_milestones`: Updates you after a certain number of shinies.

- `total_encounter_milestones`: Updates you when your total count hits a big number.

- `phase_summary`: Gives you a recap of the current hunt.
  - You can set it to post once after a while, and then regularly after that.
  - It's great for keeping track of those long, painful hunts.

- `anti_shiny_pokemon_encounter`: Pings you for "anti-shinies."
  - These are just the mathematical opposite of a shiny. We added this just for fun.

- `custom_filter_pokemon_encounter`: Pings you when the bot finds something that matches your [custom filters](Configuration%20-%20Custom%20Catch%20Filters.md).

- `pickup`: Tells you when your Pokémon find items with the Pickup ability.
  - It'll give you a summary after they've found a few things.

- `tcg_cards`: The bot will find a TCG card image for the Pokémon it just ran into and post it.

