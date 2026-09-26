import os
import subprocess


# Common Windows applications
APP_PATHS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "command prompt": "cmd.exe",
    "file explorer": "explorer.exe",
}


def open_app(app_name):
    """
    Open an application by name.
    """

    app_name = app_name.lower().strip()

    # Windows built-in applications
    if app_name in APP_PATHS:
        subprocess.Popen(APP_PATHS[app_name])
        return f"Opening {app_name}."

    # Google Chrome
    if app_name == "chrome":
        chrome_paths = [
            os.path.expandvars(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
            ),
            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
            ),
        ]

        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path])
                return "Opening Chrome."

        return "I couldn't find Google Chrome."

    # Visual Studio Code
    if app_name in ["vs code", "visual studio code", "code"]:
        try:
            subprocess.Popen(["code"])
            return "Opening Visual Studio Code."
        except FileNotFoundError:
            return "I couldn't find Visual Studio Code."

    return None