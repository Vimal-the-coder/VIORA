from commands.app_launcher import open_app
from commands.file_manager import open_path
from commands.system_control import (
    lock_pc,
    sleep_pc,
    restart_pc,
    shutdown_pc,
    logout_pc,
)
from commands.web_commands import execute_web_command


def route_command(command):
    """
    Route commands using local Python logic.

    Known commands are executed immediately.
    Unknown commands return None so that
    voice_assistant.py can send them to Gemini.
    """

    command = command.lower().strip()

    # =========================
    # APP / WEBSITE COMMANDS
    # =========================

    if command.startswith("open "):

        target = command[5:].strip()

        # Try application launcher first
        app_result = open_app(target)

        if app_result:
            return app_result

        # Then try website commands
        web_result = execute_web_command(command)

        if web_result:
            return web_result

    # =========================
    # WEB COMMANDS
    # =========================

    web_result = execute_web_command(command)

    if web_result:
        return web_result

    # =========================
    # FILE / FOLDER COMMANDS
    # =========================

    if "open downloads" in command:
        from pathlib import Path
        return open_path(Path.home() / "Downloads")

    if "open documents" in command:
        from pathlib import Path
        return open_path(Path.home() / "Documents")

    if "open desktop" in command:
        from pathlib import Path
        return open_path(Path.home() / "Desktop")

    # =========================
    # LOCK
    # =========================

    if any(phrase in command for phrase in [
        "lock computer",
        "lock pc",
        "lock my computer",
        "lock my pc",
    ]):
        return lock_pc()

    # =========================
    # SLEEP
    # =========================

    if any(phrase in command for phrase in [
        "sleep computer",
        "sleep pc",
        "sleep my computer",
        "sleep my pc",
    ]):
        return sleep_pc()

    # =========================
    # RESTART
    # =========================

    if any(phrase in command for phrase in [
        "restart computer",
        "restart pc",
        "restart my computer",
        "restart my pc",
    ]):
        return restart_pc()

    # =========================
    # SHUTDOWN
    # =========================

    if any(phrase in command for phrase in [
        "shutdown computer",
        "shutdown pc",
        "shutdown my computer",
        "shutdown my pc",
        "shut down computer",
        "shut down pc",
        "shut down my computer",
        "shut down my pc",
    ]):
        return shutdown_pc()

    # =========================
    # LOGOUT
    # =========================

    if any(phrase in command for phrase in [
        "log out",
        "logout",
        "log me out",
    ]):
        return logout_pc()

    # =========================
    # NOTHING MATCHED
    # =========================

    return None