import sublime
import sublime_plugin

from ..utils.core_commands_utils import (
    get_core_commands_data, _kind_mapping, core_commands_doc_panel
)

from ..settings import commands_browser_settings
from ..utils.miscellaneous_utils import filter_command_types


class CommandsBrowserCoreCommandsCommand(sublime_plugin.WindowCommand):

    def run(self, application):
        commands_data = get_core_commands_data(application = application)
        items = []

        if application == "st":
            cmd_type_filter_list = filter_command_types("filter_core_commands_on_type")

        for key, value in commands_data.items():
            if not value.get("location"):
                annotation_string = "{}".format(value.get("type"))
            else:
                annotation_string = "{} ({})".format(value.get("type"), value.get("location"))

            if application == "st":
                if value["command_type"] not in cmd_type_filter_list:
                    continue

            if application == "sm":
                annotation_string = "{} ({})".format(value.get("type"), value.get("added"))

            item = sublime.QuickPanelItem(
                trigger = key,
                annotation = annotation_string,
                details = value.get("doc_string") if value.get("doc_string") else "No description available",
                kind = _kind_mapping[value.get("command_type")]
            )

            items.append(item)

        if not len(items):
            sublime.status_message("No commands available for preview.")
            return

        self.window.show_quick_panel(
            items = items,
            on_select = lambda idx: self.on_select(idx, commands_data.items()),
            on_highlight = lambda idx: self.on_highlight(idx, commands_data.items()),
            flags = sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT,
            placeholder = f"Browse through {len(items)} available {application.upper()} commands ..."
        )


    def on_select(self, idx, commands_data):
        if idx < 0:
            return
        core_commands_doc_panel(self.window, list(commands_data)[idx])


    def on_highlight(self, idx, commands_data):
        if idx < 0:
            return
        if commands_browser_settings("cb.auto_open_doc_panel_on_navigate"):
            core_commands_doc_panel(self.window, list(commands_data)[idx])
