🏠 [`realbot-g3` Wiki Home](../README.md)

# 🧩 Plugins

If you know Python and want to change how the bot works, you can create a plugin.

Plugins are small scripts that run when certain things happen in the game—like when a battle starts or an egg hatches. You can find a full list of these events in [modules/plugin_interface.py](../../modules/plugin_interface.py).

## Making a Plugin

To make a plugin, just create a `.py` file inside the `plugins/` folder. Make sure it's directly in that folder and not in a subfolder.

Your file needs a class that uses `BotPlugin`. Here's the simplest setup:

```python
from modules.plugin_interface import BotPlugin

class MyPlugin(BotPlugin):
    pass
```

This doesn't do anything yet, but you can add your own code by overiding methods from the `BotPlugin` class. Check [modules/plugin_interface.py](../../modules/plugin_interface.py) to see what you can change.

## Why Use Plugins?

The `plugins/` folder is ignored by Git and the bot's auto-updater. This means your code won't get deleted or overwritten when you update the bot. If you edit the bot's main code directly, you might lose your changes during an update.

## Examples

The bot actually uses plugins for some of its own features. You can see how those work in the [modules/built_in_plugins/](../../modules/built_in_plugins/) folder.
