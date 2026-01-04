🏠 [`realbot-g3` Wiki Home](../README.md)

# 📡 HTTP Server

Edit these settings in [`profiles/http.yml`](../../modules/config/templates/http.yml).

You can use the HTTP server to power things like custom stream overlays or web interfaces.

Just a heads up: if you turn this on, you can only run one bot instance at a time on that port. If you try to run more, they'll show an error when you start them up.

## Settings

`enable` - Turn the HTTP server on or off.

`ip` - The IP address the server uses.

`port` - The port the server listens on.
- If you want to run multiple bots, each one needs its own port.

### How to use it

The bot's built-in server can give you all sorts of data about the game and your current settings. It even lets you control the bot remotely.

If you have the server running, you can find these pages:
- **Example UI**: [http://127.0.0.1:8888/](http://127.0.0.1:8888/)
- **API Docs**: [http://127.0.0.1:8888/docs/](http://127.0.0.1:8888/docs/)
