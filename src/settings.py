import sublime


def load_commands_browser_settings():
    """ Loads the default CommandsBrowser settings.

    Args:
        None

    Returns:
        None
    """
    print("[CommandsBrowser]: Settings intialized")
    commands_browser_settings.obj = sublime.load_settings("CommandsBrowser.sublime-settings")
    commands_browser_settings.default = {
        "auto_open_doc_panel_on_navigate": False,
        "filter_plugin_commands_on_host": "all",
        "filter_plugin_commands_on_type": ["text", "window", "application"],
        "filter_core_commands_on_type": ["text", "window", "application", "find"],
        "copy_command_signature_modifier_key": "ctrl"
    }
    print(commands_browser_settings.default)


def commands_browser_settings(key):
    """ Returns the value of the key for a given setting.

    Args:
        key (str): The target key, whose value is required.

    Returns:
        value (Any): The value of said key.
    """
    print(commands_browser_settings.default)
    default = commands_browser_settings.default.get(key, None)
    print(f"[CommandsBrowser]: {key} - {commands_browser_settings.obj.get(key, default)}")
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
