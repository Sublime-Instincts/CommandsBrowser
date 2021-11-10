import sublime
import sublime_plugin

from ..utils.core_commands_utils import get_core_commands_data, _kind_mapping


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
            on_select = lambda id: self.on_select(id, items),
            flags = sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT,
            placeholder = "Browse through available commands"
        )


    def on_select(self, id, items):
        if id >= 0:
            pass
