import re
import sys
import inspect

from .miscellaneous_utils import command_kind_type

from sublime_plugin import (
    application_command_classes, window_command_classes, text_command_classes
)


_cmd_types = {
    "application": {
        "name": "ApplicationCommand",
        "commands": application_command_classes,
        "kind": command_kind_type("application")
    },
    "window": {
        "name": "WindowCommand",
        "commands": window_command_classes,
        "kind": command_kind_type("window")
    },
    "text": {
        "name": "TextCommand",
        "commands": text_command_classes,
        "kind": command_kind_type("text")
    }
}


def legacy():
    """ Gives information on whether the plugin is running in the legacy 3.3.6
    host.

    Args:
        None

    Returns:
        (bool): Whether the plugin is running in 3.3.6 host.
    """
    return sys.version_info < (3, 8, 0)


def navigate_to(view, symbol):
    """
    Navigate to the symbol in the given view.

    Args:
        view (sublime.View):
        symbol (str):

    Returns:
        None
    """
    view.window().run_command("goto_definition", {"symbol": symbol})


def get_commands(cmd_type, commands, cmd_dict_out):
    """
    Given a list of commands of a particular type, decode each command in the list
    into a dictionary that describes it and store it into the output dictionary
    keyed by the package that defined it.

    The output dictionary gains keys for each package, where the values are
    dictionaries which contain keys that describe the commands of each of the
    supported typed.

    Args:
        cmd_type (str): The type of command. Valid values are "app", "wnd", "txt".
        commands (List[str]): List of commands retrieved from the plugin host.
        cmd_dict_out (Dict): A dictionary containing the decoded command details.

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
        command (str): An individual class object (representing a command).
        cmd_type (str):

    Returns:
        (Dict[str, Unknown]): The target command information.
    """
    return {
        "type": cmd_type,
        "pkg": command.__module__.split(".")[0],
        "mod": ".".join(command.__module__.split(".")[1:]),
        "name": get_name(command),
        "args": get_args(command),
        "class": command.__name__,
        "host": "3.8"
    }


def get_args(cmd_class):
    """ Return a string that represents the arguments to the run method of the
    Sublime command class provided, edited to remove the internal python arguments
    that are not needed to invoke the command from Sublime.

    Args:
        cmd_class ():

    Returns:
        (str): Arguments taken by the command in the form of a string.
    """
    args = str(inspect.signature(cmd_class.run))
    return re.compile(r"^\(self(?:, )?(?:edit, |edit)?(.*)\)$").sub(r"{ \1 }", args)


def get_name(cmd_class):
    """ Return the internal Sublime command name as Sublime would infer it from
    the name of the implementing class. This is taken from the name() method of
    the underlying Command class in sublime_plugin.py.

    Args:
        cmd_class (str): A string representing the command class.

    Returns:
        name (str): The command name representing the command class.
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
