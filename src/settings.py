import sublime


def load_commands_browser_settings():
    """ Loads the default CommandsBrowser settings.

    Args:
        None

    Returns:
        None
    """

    commands_browser_settings.obj = sublime.load_settings("CommandsBrowser.sublime-settings")
    commands_browser_settings.default = {
        "cb.auto_open_doc_panel_on_navigate": False,
        "cb.filter_plugin_commands_on_host": "all",
        "cb.filter_plugin_commands_on_type": ["text", "window", "application"],
        "cb.filter_core_commands_on_type": ["text", "window", "application", "find"]
    }


def commands_browser_settings(key):
    """ Returns the value of the key for a given setting.

    Args:
        key (str): The target key, whose value is required.

    Returns:
        value (Any): The value of said key.
    """

    default = commands_browser_settings.default.get(key, None)
    return commands_browser_settings.obj.get(key, default)


def commands_browser_set_setting(key, value):
    """ Set's the value of the given key in question and saves the settings.

    Args:
        key (str): The target key.
        value (Any): The target value.

    Returns:
        None
    """

    if value is not None:
        commands_browser_settings.obj.set(key, value)
        sublime.save_settings("CommandsBrowser.sublime-settings")
        return

    default = commands_browser_settings.default.get(key, None)
    commands_browser_settings.obj.set(key, default)
    sublime.save_settings("CommandsBrowser.sublime-settings")
