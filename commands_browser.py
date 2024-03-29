import sublime

from pathlib import Path
from zipfile import ZipFile

from .src.settings import load_commands_browser_settings
from .src import (
    CommandsBrowserCoreCommandsCommand,
    CommandsBrowserPluginCommandsCommand, CommandsBrowserCommandJumpListener
)


def loaded():
    """ Wraps what needs to be present in plugin_loaded so that it can be used
    in sublime.set_timeout.

    Args:
        None

    Returns:
        None
    """
    load_commands_browser_settings()

    package_root = Path(sublime.installed_packages_path())
    package_name = __package__ + "33.sublime-package"
    package_file = package_root / package_name
    if package_file.exists():
        return

    # static list of resources to pack into python 3.3 package
    res_dir = "Packages/" + __package__ + "/src/py33/"
    res_files = ["browse.py"]

    # Create intermediate package file, which is not yet loaded by ST
    tmp_file = package_root / (package_name + "-new")
    with ZipFile(tmp_file, "w") as pkg:
        pkg.writestr(".hidden-sublime-package", "")
        for res in res_files:
            pkg.writestr(res, sublime.load_resource(res_dir + res))

    # Enable package by renaming to target name
    tmp_file.rename(package_file)


def plugin_loaded():
    """ This function is called when the package is loaded, but before the API
    functions are made available. We need to do 2 things here.

    1. Load the settings file.

    2. Since we need a way to collect commands from the 3.3 host, we need to
       create an additional folder (CommandsBrowser33) with a plugin that can
       register a command to help collect that data. This is similar to the
       strategy followed by APR.
    """

    # I have no idea why the contents of loaded() needs to happen on the next
    # UI refresh tick. If it's placed directly in plugin_loaded(), then the
    # settings somehow return None instead of their default values and
    # find_resources fails to find the py33 file.
    sublime.set_timeout(loaded, 0)


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

    # Since we do not have a reference to the window object for which the panel
    # was created, we simply loop through the available windows and destroy the
    # panel (If it exists), for each one.
    for window in sublime.windows():
        window.destroy_output_panel("CommandsBrowser")

    package_root = Path(sublime.installed_packages_path())
    package_name = __package__ + "33.sublime-package"
    package_file = package_root / package_name

    try:
        package_file.unlink()
    except Exception as e:
        print(f"[CommandsBrowser]: Failed to remove {package_name} with exception {e}")
