import sublime
import textwrap

from ..settings import commands_browser_settings


def command_kind_type(command_type):
    """ Based on the command_type, returns a tuple that can the be used to have
    appropriate kind information in the quick panel.

    Args:
        command_type (str): The type of command. Valid values are "text", "find",
        "window" and "application".

    Returns:
        kind_information (Tuple[kind_type, str, str]): The kind information tuple.
    """

    if command_type == "text":
        return (sublime.KIND_ID_NAMESPACE, "T", "Text Command")

    if command_type == "window":
        return (sublime.KIND_ID_FUNCTION, "W", "Window Command")

    if command_type == "application":
        return (sublime.KIND_ID_TYPE, "A", "Application Command")

    if command_type == "find":
        return (sublime.KIND_ID_MARKUP, "F", "Find Command")


def log(message):
    """ A simple logger that will log the given message to the console.

    Args:
        message (str): The message to log.

    Returns:
        None
    """
    print(f"[CommandsBrowser]: {textwrap.dedent(message)}")


def filter_command_types(setting_name):
    """ The user settings for filter_plugin_commands_on_type and
    filter_core_commands_on_type can be riddled with problems like invalid values
    or wrong command types. This function sanitizes the setting value.

    Args:
        setting_name (str): The name of the setting.

    Returns:
        cmd_type_filter_list (List[str]): The sanitised command type list based
        on which, we will filter the commands
    """
    cmd_type_filter_list = commands_browser_settings(f"{setting_name}")

    if (type(cmd_type_filter_list) != list) or (len(cmd_type_filter_list) == 0):
        log(f"""'{cmd_type_filter_list}' is an invalid value for the setting
            'cb.{setting_name}'. Falling back to default value.""")
        cmd_type_filter_list = commands_browser_settings.default.get(f"{setting_name}")

    cmd_type_list = commands_browser_settings.default.get(f"{setting_name}")
    cmd_type_filter_list = [i for i in cmd_type_filter_list if i in cmd_type_list]

    if not len(cmd_type_filter_list):
        cmd_type_filter_list = commands_browser_settings.default.get(f"{setting_name}")

    return cmd_type_filter_list
