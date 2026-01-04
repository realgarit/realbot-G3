# Copyright (c) 2026 realgarit
import queue
import sys
from collections import deque
from typing import Generator

from modules.core.console import console
from modules.core.context import context
from modules.game.memory import get_game_state
from modules.modes import BotMode, BotModeError, FrameInfo, get_bot_listeners, get_bot_mode_by_name
from modules.core.plugins import plugin_profile_loaded, load_built_in_plugins
from modules.core.state_cache import state_cache
from modules.stats.stats import StatsDatabase
from modules.core.tasks import get_global_script_context, get_tasks

# This queue holds tasks for the next frame.
# The HTTP server uses it to do stuff like check the party data from the main thread.
# Each task runs once and then disappears.
work_queue: queue.Queue[callable] = queue.Queue()


# This tracks button presses so the HTTP server can show them in the event stream.
inputs_each_frame: deque[int] = deque(maxlen=128)


class ManualBotMode(BotMode):
    @staticmethod
    def name() -> str:
        return "Manual"

    def run(self) -> Generator:
        yield


def main_loop() -> None:
    """
    This function is run after the user has selected a profile and the emulator has been started.
    """
    try:
        if context.rom.game_name.startswith("Unsupported "):
            console.print("\n[red bold]You are running an unsupported game![/]")
            console.print(
                "\n[red]This ROM does not appear to be an exact copy of an original Gen3 game.\nIt's possible that is has been modified, or that it got corrupted while dumping the cartridge.\nWhile this might still work, chances are that some or all bot functions will not.[/]"
            )
            console.print("\n[red bold]Please do not ask for support if there are any problem with this game.[/]\n")

        # We only load built-in plugins if the config needs them.
        # Since profiles can change these settings, we wait until the profile is loaded.
        #
        # Any plugins you add yourself are loaded earlier so they can show up in the bot modes list.
        load_built_in_plugins()
        plugin_profile_loaded(context.profile)

        context.stats = StatsDatabase(context.profile)

        if context.config.http.http_server.enable:
            from modules.web.http import start_http_server

            start_http_server(
                host=context.config.http.http_server.ip,
                port=context.config.http.http_server.port,
            )

        context.bot_listeners = get_bot_listeners(context.rom)
        previous_frame_info: FrameInfo | None = None

        while True:
            # Here's where we handle tasks from the work queue at a safe moment between frames.
            while not work_queue.empty():
                callback = work_queue.get_nowait()
                callback()
                work_queue.task_done()

            context.frame += 1

            game_state = get_game_state()
            script_context = get_global_script_context()
            script_stack = script_context.stack if script_context is not None and script_context.is_active else []
            task_list = get_tasks()
            if task_list is not None:
                active_tasks = [task.symbol.lower() for task in task_list]
            else:
                active_tasks = []

            frame_info = FrameInfo(
                frame_count=context.emulator.get_frame_count(),
                game_state=game_state,
                active_tasks=active_tasks,
                script_stack=script_stack,
                controller_stack=[controller.__qualname__ for controller in context.controller_stack],
                previous_frame=previous_frame_info,
            )

            # If the emulator resets, we need to reset the bot listeners too.
            if previous_frame_info is not None and previous_frame_info.frame_count > frame_info.frame_count:
                state_cache.reset()
                context.bot_listeners = get_bot_listeners(context.rom)

            if context.bot_mode == "Manual":
                if not isinstance(context.bot_mode_instance, ManualBotMode):
                    context.emulator.reset_held_buttons()
                context.bot_mode_instance = ManualBotMode()
            elif len(context.controller_stack) == 0:
                context.bot_mode_instance = get_bot_mode_by_name(context.bot_mode)()
                context.controller_stack.append(context.bot_mode_instance.run())

            try:
                for listener in context.bot_listeners.copy():
                    listener.handle_frame(context.bot_mode_instance, frame_info)
                if context.bot_mode == "Manual":
                    context.controller_stack = []
                if len(context.controller_stack) > 0:
                    next(context.controller_stack[-1])
            except (StopIteration, GeneratorExit):
                context.controller_stack.pop()
            except BotModeError as e:
                context.emulator.reset_held_buttons()
                context.message = str(e)
                context.set_manual_mode()
            except TimeoutError:
                console.print_exception()
                sys.exit(1)
            except Exception as e:
                console.print_exception()
                context.emulator.reset_held_buttons()
                context.message = f"Internal Bot Error: {str(e)}"
                if context.debug:
                    context.debug_stepping_mode()
                    if hasattr(sys, "gettrace") and sys.gettrace() is not None:
                        breakpoint()
                else:
                    context.set_manual_mode()

            inputs_each_frame.append(context.emulator.get_inputs())
            context.emulator.run_single_frame()
            previous_frame_info = frame_info
            previous_frame_info.previous_frame = None

    except SystemExit:
        raise
    except Exception:
        console.print_exception(show_locals=True)
        sys.exit(1)
