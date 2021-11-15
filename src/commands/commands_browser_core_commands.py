import sublime
import sublime_plugin

from ..utils.core_commands_utils import (
    get_core_commands_data, kind_mapping, core_commands_doc_panel
)

from ..settings import commands_browser_settings
from ..utils.miscellaneous_utils import filter_command_types, log


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
            on_select = lambda idx, event: self.on_select(idx, event, commands_data.items()),
            on_highlight = lambda idx: self.on_highlight(idx, commands_data.items()),
            flags = sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT | sublime.WANT_EVENT,
            placeholder = f"Browse through {len(items)} available {application.upper()} commands ..."
        )


    def on_select(self, idx, event, commands_data):
        """ The callback that runs after picking a quick panel item. When the
        user selects an item, we show the relevant command docs in a panel. If
        the user, holds a configured modifier key while selecting, we also copy
        the command signature to clipboard.

        Args:
            idx (int): The index of the selected command item.
            commands_data (Dict): The commands data.

        Returns:
            None
        """
        if idx < 0:
            return
        core_commands_doc_panel(self.window, list(commands_data)[idx])

        if not event:
            return

        modifier_key = commands_browser_settings("copy_command_signature_modifier_key")
        modifier_key_list = ["ctrl", "primary", "alt", "altgr", "shift", "super"]

        if (type(modifier_key) != str) or (modifier_key not in modifier_key_list):
            log(f"""'{modifier_key}' is an invalid value for the setting
                'copy_command_signature_modifier_key'. Falling back to default value.""")
            modifier_key = "ctrl"

        if modifier_key in event["modifier_keys"]:
            command_data = list(commands_data)[idx]
            command_type = command_data[1]["command_type"]

            if command_type == "text":
                final_string = f"view.run_command("
            if command_type == "application":
                final_string = f"sublime.run_command("
            if command_type in ["window", "find"]:
                final_string = f"window.run_command("

            if not command_data[1].get("args"):
                sublime.set_clipboard(final_string + f'"{command_data[0]}")')
                sublime.status_message("Command signature copied to clipboard.")
                return

            arg_string = ""
            for arg in command_data[1].get("args"):
                arg_name = arg['name']
                arg_string = arg_string + f'"{arg_name}": , '

            final_string = final_string + f'"{command_data[0]}", ' + "{ " + arg_string + " })"
            sublime.set_clipboard(final_string)
            sublime.status_message("Command signature copied to clipboard.")


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

        auto_open = commands_browser_settings("auto_open_doc_panel_on_navigate")

        if (type(auto_open) != bool):
            log(f"""'{auto_open}' is an invalid value for the setting
                'auto_open_doc_panel_on_navigate'. Falling back to default value.""")
            auto_open = False

        if auto_open:
            core_commands_doc_panel(self.window, list(commands_data)[idx])


    def want_event(self):
        """ We need to use this method, if we want to receive the event object
        using which we can trigger different behavior when modifier keys are
        pressed.

        Args:
            None

        Returns:
            (bool): Whether to receive the event object.
        """
        return True
