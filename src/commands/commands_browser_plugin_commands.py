import re
import os
import sys
import inspect
import sublime
import sublime_plugin

from ..utils.plugin_command_utils import (
    get_commands, legacy, _cmd_types, navigate_to
)

from ..settings import commands_browser_settings
from ..utils.miscellaneous_utils import log


class CommandsBrowserPluginCommandsCommand(sublime_plugin.ApplicationCommand):


    def name(self):
        return "commands_browser_plugin_commands_33" if legacy() else "commands_browser_plugin_commands"


    def run(self, cmd_dict = None):
        cmd_dict = cmd_dict or {}
        for cmd_type, cmd_info in _cmd_types.items():
            get_commands(cmd_type, cmd_info["commands"], cmd_dict)

        if legacy():
            return sublime.run_command('commands_browser_plugin_commands', { "cmd_dict": cmd_dict })

        items = []
        host = commands_browser_settings("cb.filter_plugin_commands_on_host")

        if (type(host) != str) or (host not in ["all", "3.3", "3.8"]):
            log(f"""'{host}' is an invalid value for the setting
                'cb.filter_plugin_commands_on_host'. Falling back to default value of 'all'.""")

        for _, details in cmd_dict.items():

            if host != "all":
                if details["host"] != host:
                    continue

            items.append(
                sublime.QuickPanelItem(
                    trigger = details["name"],
                    details = f"<i>{details['args']}</i>",
                    annotation = f"{details['pkg']}.{details['mod']} ({details['host']})",
                    kind = _cmd_types[details["type"]]["kind"]
                )
            )

        items.sort(key=lambda o: o.trigger)

        window = sublime.active_window()

        window.show_quick_panel(
            items = items,
            on_select = lambda idx: self.on_select(idx, items, cmd_dict),
            placeholder = f"Browse through {len(items)} available plugin/package commands ...",
            flags = sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT
        )


    def on_select(self, idx, items, cmd_dict):
        if idx < 0:
            return

        cmd = cmd_dict[items[idx].trigger]
        module = cmd["mod"].replace('.', '/')
        res = '${packages}/%s/%s.py' % (cmd["pkg"], module)

        sublime.active_window().run_command('open_file', {'file': res})
        view = sublime.active_window().active_view()
        if view.is_loading():
            view.settings().set("_jump_to_class", cmd["class"])
        else:
            navigate_to(view, cmd["class"])



class CommandsBrowserCommandJumpListener(sublime_plugin.ViewEventListener):


    @classmethod
    def is_applicable(cls, settings):
        return settings.has("_jump_to_class")


    def on_load(self):
        symbol = self.view.settings().get("_jump_to_class")
        self.view.settings().erase("_jump_to_class")

        sublime.set_timeout(lambda: navigate_to(self.view, symbol), 0)
