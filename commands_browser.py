import os
import sublime
from shutil import copyfile
from .src.settings import load_commands_browser_settings
from .src import (
    CommandsBrowserCoreCommandsCommand,
    CommandsBrowserPluginCommandsCommand, CommandsBrowserCommandJumpListener
)


def plugin_loaded():
    load_commands_browser_settings()

    commands_browser_33_path = os.path.join(sublime.packages_path(), "CommandsBrowser33")
    file_to_copy_path = os.path.join(sublime.packages_path(), "CommandsBrowser", "src/py33/browse.py")
    dest_file_path = os.path.join(commands_browser_33_path, "browse.py")
    if not os.path.exists(commands_browser_33_path):
        os.makedirs(commands_browser_33_path)
    if not os.path.exists(dest_file_path):
        with open(dest_file_path, "w"):
            pass
    copyfile(file_to_copy_path, dest_file_path)


def plugin_unloaded():
    pass