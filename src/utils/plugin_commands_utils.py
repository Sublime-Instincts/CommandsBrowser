import re
import sys
import inspect
import sublime

from sublime_plugin import (
    application_command_classes, window_command_classes, text_command_classes
)

from .miscellaneous_utils import command_kind_type


cmd_types = {
    "app": {
        "name": "ApplicationCommand",
        "commands": application_command_classes,
        "kind": command_kind_type("application")
    },
    "wnd": {
        "name": "WindowCommand",
        "commands": window_command_classes,
        "kind": command_kind_type("window")
    },
    "txt": {
        "name": "TextCommand",
        "commands": text_command_classes,
        "kind": command_kind_type("text")
    }
}


def navigate_to_plugin_file(view, command):
    """ Navigates to the plugin file that defined the chosen command.

    Args:
        view (sublime.View): The active view.
        command (str): The name of the command picked by the user.

    Returns:
        None
    """
    cmd_dict = generate_plugin_commands_list_items()[1]
    cmd = cmd_dict[command]
    module = cmd["mod"].replace('.', '/')
    res = '${packages}/%s/%s.py' % (cmd["pkg"], module)

    sublime.active_window().run_command('open_file', {'file': res})
    view = sublime.active_window().active_view()
    if view.is_loading():
        view.settings().set("_jump_to_class", cmd["class"])
    else:
        view.window().run_command("goto_definition", {"symbol": cmd["class"]})


def legacy():
    """ If the plugin host happens to be Python 3.3.6 (The old legacy host), then
    this function returns true.

    Args:
        None

    Returns:
        (bool): Whether the plugin host happens to be the legacy one.
    """
    return sys.version_info < (3, 8, 0)


def num_plugin_commands():
    """ Returns the total number of plugin commands available in plugin host.

    Args:
        None

    Returns:
        length (int): The total number of commands.
    """
    return (
        len(application_command_classes + window_command_classes + text_command_classes)
    )


def generate_plugin_commands_list_items(cmd_dict = None):
    """ Given the application type, returns the number of commands.

    Args:
        application (str): The application for which the number of commands needs
        to be calculated. Valid values are 'st' (Sublime Text) or 'sm' (Sublime Merge).

    Returns:
        length (int): The number of commands for that application.
    """
    cmd_dict = cmd_dict or {}

    for cmd_type, cmd_info in cmd_types.items():
        get_commands(cmd_type, cmd_info["commands"], cmd_dict)

    if legacy():
        return sublime.run_command('browse_commands', {"cmd_dict": cmd_dict})

    items = []
    for command, details in cmd_dict.items():
        item = sublime.ListInputItem(
            text = details["name"],
            value = details["name"],
            details = "<i>%s</i>" % details["args"],
            annotation = "%s.%s" % (details["pkg"] , details["mod"]),
            kind = cmd_types[details["type"]]["kind"]
        )
        items.append(item)
    items.sort(key=lambda o: o.text)

    return items, cmd_dict


def get_commands(cmd_type, commands, cmd_dict_out):
    """
    Given a list of commands of a particular type, decode each command in
    the list into a dictionary that describes it and store it into the
    output dictionary keyed by the package that defined it.

    The output dictionary gains keys for each package, where the values are
    dictionaries which contain keys that describe the commands of each of
    the supported typed.

    Args:
        cmd_type ():
        commands ():
        cmd_dict_out (Dict):

    Returns:
        None
    """
    for command in commands:
        decoded = decode_cmd(command, cmd_type)
        cmd_dict_out[decoded["name"]] = decoded


def decode_cmd(command, cmd_type):
    """
    Given a class that implements a command of the provided type, return back a
    dictionary that contains the properties of the command for later display.

    Args:
        command ():
        cmd_type ():

    Returns
        (Dict): The plugin command metadat information as a dictionary.
    """
    return {
        "type": cmd_type,
        "pkg": command.__module__.split(".")[0],
        "mod": ".".join(command.__module__.split(".")[1:]),
        "name": get_name(command),
        "args": get_args(command),
        "class": command.__name__
    }


def get_args(cmd_class):
    """
    Return a string that represents the arguments to the run method of the
    Sublime command class provided, edited to remove the internal python
    arguments that are not needed to invoke the command from Sublime.

    Args:
        cmd_class (str):

    Return:
        args (str): Representing
    """
    args = str(inspect.signature(cmd_class.run))
    return re.compile(r"^\(self(?:, )?(?:edit, |edit)?(.*)\)$").sub(r"{ \1 }", args)


def get_name(cmd_class):
    """
    Return the internal Sublime command name as Sublime would infer it from the
    name of the implementing class. This is taken from the name() method of the
    underlying Command class in sublime_plugin.py.

    Args:
        cmd_class (str):

    Returns:
        name (str):
    """
    clsname = cmd_class.__name__
    name = clsname[0].lower()
    last_upper = False
    for c in clsname[1:]:
        if c.isupper() and not last_upper:
            name += '_'
            name += c.lower()
        else:
            name += c
        last_upper = c.isupper()
    if name.endswith("_command"):
        name = name[0:-8]
    return name