from .src.settings import load_commands_browser_settings
from .src import *


def plugin_loaded():
    load_commands_browser_settings()


def plugin_unloaded():
    pass