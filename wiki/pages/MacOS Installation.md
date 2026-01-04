🏠 [`realbot-g3` Wiki Home](../README.md)

# macOS Installation Guide

<img src="../images/os_apple.png" alt="MacOS" style="max-width: 80px">

> This guide is for Macs with Apple Silicon (M1, M2, M3, etc.).

We’ve updated the bot to use **Python 3.13** and **Tkinter 9**. This is a big improvement because it fixes the visual gliches and weird button alignments that used to happen on macOS. It also means you **no longer have to manually compile** Tcl/Tk or follow those long, complicated setup steps!

### 1. Install Homebrew
If you don't have it yet, go to [brew.sh](https://brew.sh/) and follow the instructions on their homepage to install it.

### 2. Update Homebrew
Open your terminal and make sure everything is up to date:
`brew update && brew upgrade`

### 3. Install the Essentials
Run this command to install the emulator, Python 3.13, and the other tools the bot needs:
`brew install mgba python@3.13 tcl-tk portaudio`

### 4. Set up your Bot Folder
Download the bot's code and move the folder to wherever you want to keep it on your Mac.

### 5. Create a Virtual Environment (Recommended)
It's always better to keep the bot's packages separate from your main system. Open your terminal, go into the bot's folder, and run:

```bash
/opt/homebrew/bin/python3.13 -m venv venv
source venv/bin/activate
```

### 6. Run the Bot!
Now you just need to start the program. The first time you run it, the bot will automatically download and install all the Python libraries it needs (it handles the `requirements.py` stuff for you):
`python realbot.py`

If you'd rather install the requirements yourself first, you can run:
`python requirements.py`

---

## 💡 Troubleshooting

**"The buttons look off or the window is glitchy"**
Check your Python version by typing `python --version`. It must be at least **3.13** to use the new Tkinter 9 features. If you see 3.12 or older, the bot won't look right on macOS.

**"I get a portaudio error"**
Make sure you didn't skip the `brew install portaudio` step. It's required for the bot to handle the game's audio correctly.

**"I can't see (venv) in my terminal"**
Make sure you ran the `source venv/bin/activate` command. You'll need to run this every time you open a new terminal window to start the bot.