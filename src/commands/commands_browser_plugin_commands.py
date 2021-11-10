import re
import sys
import inspect
import sublime
import sublime_plugin

from ..utils.plugin_command_utils import (
    get_commands, legacy, _cmd_types
)


def _navigate_to(view, symbol):
    """
    Navigate to the symbol in the given view.
    """
    view.window().run_command("goto_definition", {"symbol": symbol})



class CommandsBrowserPluginCommandsCommand(sublime_plugin.ApplicationCommand):
    """
    Open a quick panel with a list of all commands known to the Sublime plugin
    host for the user to choose from. Picking a command opens the plugin file
    containing the command and navigates to the location where the command is
    defined.

    This command is exposed to both plugin hosts (by way of being in two
    packages) with the Python 3.3 plugin host triggering the command from the
    Python 3.8 host, so that we can gather all available commands.
    """


    def name(self):
        return "commands_browser_plugin_commands_33" if legacy() else "commands_browser_plugin_commands"


    def run(self, cmd_dict=None):
        cmd_dict = cmd_dict or {}
        for cmd_type, cmd_info in _cmd_types.items():
            get_commands(cmd_type, cmd_info["commands"], cmd_dict)

        if legacy():
            return sublime.run_command('commands_browser_plugin_commands', {"cmd_dict": cmd_dict})

        items = []
        for command, details in cmd_dict.items():
            items.append(
                sublime.QuickPanelItem(
                    trigger = details["name"],
                    details = "<i>%s</i>" % details["args"],
                    annotation = "%s.%s" % (details["pkg"] , details["mod"]),
                    kind = _cmd_types[details["type"]]["kind"]
                )
            )

        items.sort(key=lambda o: o.trigger)
        window = sublime.active_window()
        window.show_quick_panel(
            items = items,
            on_select = lambda idx: self.on_select(idx, items, cmd_dict),
            placeholder = f"Browse through {len(items)} available plugin/package commands ..."
        )


    def on_select(self, idx, items, cmd_dict):
        if idx == -1:
            return

        cmd = cmd_dict[items[idx].trigger]
        module = cmd["mod"].replace('.', '/')
        res = '${packages}/%s/%s.py' % (cmd["pkg"], module)

        sublime.active_window().run_command('open_file', {'file': res})
        view = sublime.active_window().active_view()
        if view.is_loading():
            view.settings().set("_jump_to_class", cmd["class"])
        else:
            _navigate_to(view, cmd["class"])



class CommandsBrowserCommandJumpListener(sublime_plugin.ViewEventListener):


    @classmethod
    def is_applicable(cls, settings):
        return settings.has("_jump_to_class")


    def on_load(self):
        symbol = self.view.settings().get("_jump_to_class")
        self.view.settings().erase("_jump_to_class")

        sublime.set_timeout(lambda: _navigate_to(self.view, symbol), 0)
