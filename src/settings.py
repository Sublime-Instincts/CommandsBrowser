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
        "ccb.auto_open_panel_on_navigate": False
    }


def commands_browser_settings(key):
    """
    """

    default = commands_browser_settings.default.get(key, None)
    return commands_browser_settings.obj.get(key, default)


def commands_browser_set_setting(key, value):
    """
    """

    if value is not None:
        commands_browser_settings.obj.set(key, value)
        sublime.save_settings("CommandsBrowser.sublime-settings")
        return

    # If the user doesn't specify any value to be set for that particular key,
    # we just obtain the default value of that setting and save it.
    default = commands_browser_settings.default.get(key, None)
    commands_browser_settings.obj.set(key, default)
    sublime.save_settings("CommandsBrowser.sublime-settings")