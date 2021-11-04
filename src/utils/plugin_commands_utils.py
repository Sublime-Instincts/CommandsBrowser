import re
import sys
import inspect
import sublime

from sublime_plugin import (
    application_command_classes, window_command_classes, text_command_classes
)


KIND_APPLICATION = (sublime.KIND_ID_TYPE, "A", "Application Command")
KIND_WINDOW = (sublime.KIND_ID_FUNCTION, "W", "Window Command")
KIND_TEXT = (sublime.KIND_ID_NAMESPACE, "T", "Text Command")


cmd_types = {
    "app": {
        "name": "ApplicationCommand",
        "commands": application_command_classes,
        "kind": KIND_APPLICATION
    },
    "wnd": {
        "name": "WindowCommand",
        "commands": window_command_classes,
        "kind": KIND_WINDOW
    },
    "txt": {
        "name": "TextCommand",
        "commands": text_command_classes,
        "kind": KIND_TEXT
    }
}

def legacy():
    return sys.version_info < (3, 8, 0)


def generate_plugin_commands_list_items(cmd_dict = None):
    """
    """
    cmd_dict = cmd_dict or {}
    for cmd_type, cmd_info in cmd_types.items():
        get_commands(cmd_type, cmd_info["commands"], cmd_dict)

    if legacy():
        return sublime.run_command('browse_commands', {"cmd_dict": cmd_dict})

    items = []
    for command, details in cmd_dict.items():
        item = sublime.ListInputItem(
            text=details["name"],
            value=details["name"],
            details="<i>%s</i>" % details["args"],
            annotation="%s.%s" % (details["pkg"] , details["mod"]),
            kind=cmd_types[details["type"]]["kind"]
        )
        items.append(item)

    items.sort(key=lambda o: o.text)
    return items


def get_commands(cmd_type, commands, cmd_dict_out):
    """
    Given a list of commands of a particular type, decode each command in
    the list into a dictionary that describes it and store it into the
    output dictionary keyed by the package that defined it.

    The output dictionary gains keys for each package, where the values are
    dictionaries which contain keys that describe the commands of each of
    the supported typed.
    """
    for command in commands:
        decoded = decode_cmd(command, cmd_type)
        cmd_dict_out[decoded["name"]] = decoded


def decode_cmd(command, cmd_type):
    """
    Given a class that implements a command of the provided type, return
    back a dictionary that contains the properties of the command for later
    display.
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
    """
    args = str(inspect.signature(cmd_class.run))
    return re.compile(r"^\(self(?:, )?(?:edit, |edit)?(.*)\)$").sub(r"{ \1 }", args)


def get_name(cmd_class):
    """
    Return the internal Sublime command name as Sublime would infer it from
    the name of the implementing class. This is taken from the name()
    method of the underlying Command class in sublime_plugin.py.
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