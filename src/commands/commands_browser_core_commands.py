import sublime
import sublime_plugin

from ..utils.core_commands_utils import (
    get_core_commands_data, kind_mapping, core_commands_doc_panel
)

from ..settings import commands_browser_settings
from ..utils.miscellaneous_utils import filter_command_types


class CommandsBrowserCoreCommandsCommand(sublime_plugin.WindowCommand):
    """ The command that powers the commands browser for viewing core ST/SM
    commands.

    Args:
        application (str): The application for which the command data has to be
        fetched. Valid values are 'st' (Sublime Text) & 'sm' (Sublime Merge).
    """

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

            command_item = sublime.QuickPanelItem(
                trigger = key,
                annotation = annotation_string,
                details = value.get("doc_string") if value.get("doc_string") else "No description available",
                kind = kind_mapping[value.get("command_type")]
            )

            items.append(command_item)

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
        """ The callback that runs after picking a quick panel item. When the
        user selects an item, we show the relevant command docs in a panel.

        Args:
            idx (int): The index of the selected command item.
            commands_data (Dict): The commands data.

        Returns:
            None
        """
        if idx < 0:
            return
        core_commands_doc_panel(self.window, list(commands_data)[idx])


    def on_highlight(self, idx, commands_data):
        """ The callback that runs everytime when navigating through quick panel
        items. If the user has the setting 'cb.auto_open_doc_panel_on_navigate'
        turned on in user package preferences, then we show the panel every time
        the user navigates.

        Args:
            idx (int): The index of the selected command item.
            commands_data (Dict): The commands data.

        Returns:
            None
        """
        if idx < 0:
            return
        if commands_browser_settings("auto_open_doc_panel_on_navigate"):
            core_commands_doc_panel(self.window, list(commands_data)[idx])
