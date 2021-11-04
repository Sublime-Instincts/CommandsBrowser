import sublime
import sublime_plugin
from .utils import (
    generate_core_commands_list_items, generate_plugin_commands_list_items
)

_commands_options = {
    "Browse through plugin/package commands": 1,
    "Browse through core ST (Sublime Text) commands": 2,
    "Browse through core SM (Sublime Merge) commands": 3
}


class CommandsOptionsInputHandler(sublime_plugin.ListInputHandler):

    def list_items(self):
        return _commands_options.keys()

    def next_input(self, args):
        if args is not None:
            return CommandsBrowserInputHandler(args["commands_options"])

    def description(self, v, text):
        if _commands_options[text] == 1:
            return "Plugin"
        elif _commands_options[text] == 2:
            return "Core ST"
        else:
            return "Core SM"

    def placeholder(self):
        return "Choose an option ..."


class CommandsBrowserInputHandler(sublime_plugin.ListInputHandler):

    def __init__(self, commands_option):
        self.commands_option = commands_option

    def list_items(self):
        if _commands_options[self.commands_option] == 1:
            return generate_plugin_commands_list_items()
        elif _commands_options[self.commands_option] == 2:
            return generate_core_commands_list_items("st")
        elif _commands_options[self.commands_option] == 3:
            return generate_core_commands_list_items("sm")

    def placeholder(self):
        if _commands_options[self.commands_option] == 1:
            return "Browse through x available plugin commands ..."
        return "Browse through x available core commands ..."


class CommandsBrowserCommand(sublime_plugin.WindowCommand):

    def run(self, commands_options, commands_browser):
        pass

    def input(self, args):
        if args is not None:
            return CommandsOptionsInputHandler()

    def input_description(self):
        return "Commands Browser"