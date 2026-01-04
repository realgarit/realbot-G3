🏠 [`realbot-g3` Wiki Home](../README.md)

# 🎥 OBS

Edit these settings in [`profiles/obs.yml`](../../modules/config/templates/obs.yml).

> [!NOTE]
> 🚧 **Heads up**: We're still working on the stream stuff, so these settings might change soon.

You can use these settings to set up your stream overlays or web UIs.

## OBS Settings

### OBS WebSocket

To let the bot talk to OBS, you'll need the [obs-websocket](https://github.com/obsproject/obs-websocket) plugin.

In **OBS**, go to **Tools** > **Websocket Server Settings** and check **Enable WebSocket Server**.

- `host`: The IP address for OBS WebSockets.
- `port`: The port it's using.
- `password`: The password you set in OBS (**don't leave this blank**).

### Other Options

- `shiny_delay`: How many frames to wait before catching a shiny. This gives people watching your stream a second to react.
- `discord_delay`: How many seconds to wait before sending a Discord update. This helps avoid spoilers if your stream has a delay.
- `screenshot`: Take a picture of the encounter.
  - The bot waits until your `shiny_delay` is over so your overlays have time to update.
- `replay_buffer`: Save your OBS replay buffer automatically.
- `replay_buffer_delay`: How many seconds to wait before saving the buffer.
  - This runs in the background, so it won't slow down the bot.
  - If your buffer is long enough, you'll catch a few seconds after the encounter too.
- `discord_webhook_url`: Where to post the `screenshot` after a shiny shows up.
