import sublime
import sublime_plugin

from ..utils.plugin_command_utils import (
    get_commands, legacy, cmd_types, navigate_to
)

from ..settings import commands_browser_settings
from ..utils.miscellaneous_utils import log, filter_command_types


class CommandsBrowserPluginCommandsCommand(sublime_plugin.ApplicationCommand):
    """ The command that powers the commands browser for viewing plugin/package
    based commands.

    Args:
        cmd_dict (Dict): The command information in the form of a dict collected
        from the 3.3 host.
    """

    def name(self):
        return "commands_browser_plugin_commands_33" if legacy() else "commands_browser_plugin_commands"


    def run(self, cmd_dict = None):
        cmd_dict = cmd_dict or {}
        for cmd_type, cmd_info in cmd_types.items():
            get_commands(cmd_type, cmd_info["commands"], cmd_dict)

        if legacy():
            return sublime.run_command('commands_browser_plugin_commands', { "cmd_dict": cmd_dict })

        items = []
        host = commands_browser_settings("cb.filter_plugin_commands_on_host")

        if (type(host) != str) or (host not in ["all", "3.3", "3.8"]):
            log(f"""'{host}' is an invalid value for the setting
                'cb.filter_plugin_commands_on_host'. Falling back to default value.""")
            host = "all"

        cmd_type_filter_list = filter_command_types("filter_plugin_commands_on_type")

        for _, details in cmd_dict.items():

            if host != "all":
                if details["host"] != host:
                    continue

            if details["type"] not in cmd_type_filter_list:
                continue

            items.append(
                sublime.QuickPanelItem(
                    trigger = details["name"],
                    details = f"<i>{details['args']}</i>",
                    annotation = f"{details['pkg']}.{details['mod']} ({details['host']})",
                    kind = cmd_types[details["type"]]["kind"]
                )
            )

        if not len(items):
            sublime.status_message("No commands available for preview.")
            return

        items.sort(key=lambda o: o.trigger)

        window = sublime.active_window()
        window.show_quick_panel(
            items = items,
            on_select = lambda idx: self.on_select(idx, items, cmd_dict),
            placeholder = f"Browse through {len(items)} available plugin/package commands ...",
            flags = sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT
        )


    def on_select(self, idx, items, cmd_dict):
        """ The callback that runs after picking a quick panel item. When the
        user selects an item, we navigate to the plugin file that implements the
        command, to the location of the class.

        Args:
            idx (int): The index of the selected command item.
            items (List): The plugin commands list data.
            cmd_dict (Dict): The plugin commands data.

        Returns:
            None
        """
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
