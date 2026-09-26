import os
import shutil
from pathlib import Path


def open_path(path):
    """Open a file or folder using Windows."""
    path = Path(path).expanduser()

    if not path.exists():
        return f"I couldn't find {path}."

    os.startfile(path)
    return f"Opening {path.name}."


def create_folder(path):
    """Create a new folder."""
    path = Path(path).expanduser()

    if path.exists():
        return f"{path.name} already exists."

    path.mkdir(parents=True)
    return f"Folder {path.name} created successfully."


def create_file(path):
    """Create a new empty file."""
    path = Path(path).expanduser()

    if path.exists():
        return f"{path.name} already exists."

    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()

    return f"File {path.name} created successfully."


def rename_path(old_path, new_name):
    """Rename a file or folder."""
    old_path = Path(old_path).expanduser()

    if not old_path.exists():
        return f"I couldn't find {old_path}."

    new_path = old_path.parent / new_name

    if new_path.exists():
        return f"{new_name} already exists."

    old_path.rename(new_path)

    return f"Renamed {old_path.name} to {new_name}."


def move_path(source, destination):
    """Move a file or folder."""
    source = Path(source).expanduser()
    destination = Path(destination).expanduser()

    if not source.exists():
        return f"I couldn't find {source}."

    if not destination.exists():
        return f"I couldn't find the destination {destination}."

    shutil.move(str(source), str(destination))

    return f"Moved {source.name} successfully."