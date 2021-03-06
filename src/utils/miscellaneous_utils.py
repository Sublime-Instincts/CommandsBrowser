import sublime

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
        return (sublime.KIND_ID_COLOR_BLUISH, "T", "Text Command")

    if command_type == "window":
        return (sublime.KIND_ID_COLOR_REDISH, "W", "Window Command")

    if command_type == "application":
        return (sublime.KIND_ID_COLOR_PURPLISH, "A", "Application Command")

    if command_type == "find":
        return (sublime.KIND_ID_COLOR_YELLOWISH, "F", "Find Command")


def log(message):
    """ A simple logger that will log the given message to the console.

    Args:
        message (str): The message to log.

    Returns:
        None
    """
    message = " ".join([msg.strip() for msg in message.split("\n")])
    print(f"[CommandsBrowser]: {message}")


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
            '{setting_name}'. Falling back to default value.""")
        cmd_type_filter_list = commands_browser_settings.default.get(f"{setting_name}")

    cmd_type_list = commands_browser_settings.default.get(f"{setting_name}")
    cmd_type_filter_list = [i for i in cmd_type_filter_list if i in cmd_type_list]

    if not len(cmd_type_filter_list):
        cmd_type_filter_list = commands_browser_settings.default.get(f"{setting_name}")

    return cmd_type_filter_list


def filter_package_setting():
    """ Filters the setting 'filter_plugin_commands_on_package' to get rid of
    any invalid values a user may set and sanitize it to sane defaults.

    Args:
        None

    Returns:
        package_filter (string | List[str]): The sanitised package filter list.
    """
    package_filter = commands_browser_settings("filter_plugin_commands_on_package")

    if (
        ((type(package_filter) != str) and (type(package_filter) != list)) or
        (package_filter != "all")
    ):
        log(f"""'{package_filter}' is an invalid value for the setting
        'filter_plugin_commands_on_package'. Falling back to default value.""")
        package_filter = "all"

    return package_filter
