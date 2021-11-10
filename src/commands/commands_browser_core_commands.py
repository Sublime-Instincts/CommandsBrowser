import sublime
import sublime_plugin

from ..utils.core_commands_utils import (
    get_core_commands_data, _kind_mapping, num_core_commands, core_commands_doc_panel
)


class CommandsBrowserCoreCommandsCommand(sublime_plugin.WindowCommand):

    def run(self, application):
        commands_data = get_core_commands_data(application = application)
        items = []
        for key, value in commands_data.items():
            if not value.get("location"):
                annotation_string = "{}".format(value.get("type"))
            else:
                annotation_string = "{} ({})".format(value.get("type"), value.get("location"))

            if application == "sm":
                annotation_string = "{} ({})".format(value.get("type"), value.get("added"))

            item = sublime.QuickPanelItem(
                trigger = key,
                annotation = annotation_string,
                details = value.get("doc_string") if value.get("doc_string") else "No description available",
                kind = _kind_mapping[value.get("command_type")]
            )

            items.append(item)

        self.window.show_quick_panel(
            items = items,
            on_select = lambda idx: self.on_select(idx, commands_data.items()),
            flags = sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT,
            placeholder = f"Browse through {num_core_commands(application)} available {application.upper()} commands ..."
        )


    def on_select(self, idx, commands_data):
        if idx < 0:
            return
        core_commands_doc_panel(self.window, list(commands_data)[idx])
