import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller, required to access files packed for one-file PyInstaller option"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)