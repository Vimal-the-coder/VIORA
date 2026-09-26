import os
import subprocess
import webbrowser
from pathlib import Path


def execute_command(command):
    command = command.lower().strip()

    # Open common applications
    if "open notepad" in command:
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad."

    elif "open calculator" in command:
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator."

    elif "open command prompt" in command or "open cmd" in command:
        subprocess.Popen(["cmd.exe"])
        return "Opening Command Prompt."

    elif "open file explorer" in command or "open explorer" in command:
        subprocess.Popen(["explorer.exe"])
        return "Opening File Explorer."

    # Websites
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    # Open folders
    elif "open downloads" in command:
        os.startfile(Path.home() / "Downloads")
        return "Opening Downloads."

    elif "open documents" in command:
        os.startfile(Path.home() / "Documents")
        return "Opening Documents."

    # Lock Windows
    elif "lock computer" in command or "lock pc" in command:
        subprocess.run(
            ["rundll32.exe", "user32.dll,LockWorkStation"]
        )
        return "Locking the computer."

    # Sleep Windows
    elif "sleep computer" in command or "sleep pc" in command:
        subprocess.run(
            ["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"]
        )
        return "Putting the computer to sleep."

    return None