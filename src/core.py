import sublime
import sublime_plugin

from .utils import (
    generate_core_commands_list_items, generate_plugin_commands_list_items,
    num_plugin_commands, num_core_commands, core_commands_doc_panel,
    navigate_to_plugin_file
)

_commands_option = {
    "Browse through plugin/package commands": 1,
    "Browse through core ST (Sublime Text) commands": 2,
    "Browse through core SM (Sublime Merge) commands": 3
}


class CommandsOptionInputHandler(sublime_plugin.ListInputHandler):


    def list_items(self):
        return list(_commands_option.items())


    def next_input(self, args):
        if args is not None:
            return CommandsBrowserInputHandler(args["commands_option"])


    def description(self, v, text):
        if _commands_option[text] == 1:
            return "Plugin"
        elif _commands_option[text] == 2:
            return "Core ST"
        else:
            return "Core SM"


    def placeholder(self):
        return "Choose an option ..."


class CommandsBrowserInputHandler(sublime_plugin.ListInputHandler):


    def __init__(self, commands_option):
        self.commands_option = int(commands_option)


    def list_items(self):
        if self.commands_option == 1:
            return generate_plugin_commands_list_items()[0]
        elif self.commands_option == 2:
            return generate_core_commands_list_items("st")
        elif self.commands_option == 3:
            return generate_core_commands_list_items("sm")


    def placeholder(self):
        if self.commands_option == 1:
            return f"Browse through {num_plugin_commands()} available plugin commands ..."
        if self.commands_option == 2:
            return f"Browse through {num_core_commands('st')} available core commands ..."
        if self.commands_option == 3:
            return f"Browse through {num_core_commands('sm')} available core commands ..."


class CommandsBrowserCommand(sublime_plugin.WindowCommand):


    def run(self, commands_option, commands_browser):
        if int(commands_option) != 1:
            core_commands_doc_panel(self.window, commands_browser)
            return
        view = self.window.active_view()
        navigate_to_plugin_file(view, commands_browser)


    def input(self, args):
        if args.get("commands_option"):
            return CommandsBrowserInputHandler(args["commands_option"])
        if not (args.get("commands_option") and args.get("commands_browser")):
            return CommandsOptionInputHandler()


    def input_description(self):
        return "Commands Browser"