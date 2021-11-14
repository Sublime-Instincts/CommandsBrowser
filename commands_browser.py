import os
import shutil
import sublime
from .src.settings import load_commands_browser_settings
from .src import (
    CommandsBrowserCoreCommandsCommand,
    CommandsBrowserPluginCommandsCommand, CommandsBrowserCommandJumpListener
)


def plugin_loaded():
    """ This function is called when the package is loaded, but before the API
    functions are made available. We need to do 2 things here.

    1. Load the settings file.

    2. Since we need a way to collect commands from the 3.3 host, we need to
       create an additional folder (CommandsBrowser33) with a plugin that can
       register a command to help collect that data. This is similar to the
       strategy followed by APR.
    """
    load_commands_browser_settings()

    commands_browser_33_path = os.path.join(sublime.packages_path(), "CommandsBrowser33")
    file_to_copy_path = os.path.join(sublime.packages_path(), "CommandsBrowser", "src/py33/browse.py")
    dest_file_path = os.path.join(commands_browser_33_path, "browse.py")
    if not os.path.exists(commands_browser_33_path):
        os.makedirs(commands_browser_33_path)
    if not os.path.exists(dest_file_path):
        with open(dest_file_path, "w"):
            pass

    try:
        shutil.copyfile(file_to_copy_path, dest_file_path)
    except Exception as e:
        print(f"[CommandsBrowser]: Failed to add CommandsBrowser33 with exception {e}")


def plugin_unloaded():
    """ This function is called when the package is unloaded. We need to do 2
    things here as well.

    1. Remove the CommandsBrowser33 folder. This is important because if the user
       ignores the CommandsBrowser package or uninstalls the package, we shouldn't
       keep the CommandsBrowser33 folder lying around.

    2. We need to destroy the core commands panel created (If any). This is because
       when the package unloads, the syntax file goes with it, which could cause
       the panel to throw error dialogs because it now refernces a non existing
       syntax file.
    """
    commands_browser_33_path = os.path.join(sublime.packages_path(), "CommandsBrowser33")

    # Since we do not have a reference to the window object for which the panel
    # was created, we simply loop through the available windows and destroy the
    # panel (If it exists), for each one.
    for window in sublime.windows():
        window.destroy_output_panel("CommandsBrowser")

    try:
        shutil.rmtree(commands_browser_33_path)
    except Exception as e:
        print(f"[CommandsBrowser]: Failed to remove CommandsBrowser33 with exception {e}")
