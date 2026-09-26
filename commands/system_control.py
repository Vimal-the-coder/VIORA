import subprocess
from commands.security import confirm_action


def lock_pc():
    """Lock Windows."""
    subprocess.run(
        ["rundll32.exe", "user32.dll,LockWorkStation"]
    )
    return "Locking your computer."


def sleep_pc():
    """Put Windows into sleep mode."""
    subprocess.run(
        [
            "powershell",
            "-Command",
            "Add-Type -AssemblyName System.Windows.Forms; "
            "[System.Windows.Forms.Application]::SetSuspendState("
            "[System.Windows.Forms.PowerState]::Suspend, $false, $false)"
        ]
    )
    return "Putting your computer to sleep."


def restart_pc():
    """Restart Windows after confirmation."""

    if not confirm_action("restart your computer"):
        return "Restart cancelled."

    subprocess.run(
        ["shutdown", "/r", "/t", "0"]
    )
    return "Restarting your computer."


def shutdown_pc():
    """Shut down Windows after confirmation."""

    if not confirm_action("shut down your computer"):
        return "Shutdown cancelled."

    subprocess.run(
        ["shutdown", "/s", "/t", "0"]
    )
    return "Shutting down your computer."


def logout_pc():
    """Log out after confirmation."""

    if not confirm_action("log out of your computer"):
        return "Logout cancelled."

    subprocess.run(
        ["shutdown", "/l"]
    )
    return "Logging you out."