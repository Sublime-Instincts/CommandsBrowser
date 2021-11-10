import re
import sys
import inspect
import sublime
import sublime_plugin

from sublime_plugin import (
    application_command_classes, window_command_classes, text_command_classes
)

from ..utils.miscellaneous_utils import command_kind_type


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


def _navigate_to(view, symbol):
    """
    Navigate to the symbol in the given view.
    """
    view.window().run_command("goto_definition", {"symbol": symbol})



class CommandsBrowserPluginCommandsCommand(sublime_plugin.ApplicationCommand):
    """
    Open a quick panel with a list of all commands known to the Sublime plugin
    host for the user to choose from. Picking a command opens the plugin file
    containing the command and navigates to the location where the command is
    defined.

    This command is exposed to both plugin hosts (by way of being in two
    packages) with the Python 3.3 plugin host triggering the command from the
    Python 3.8 host, so that we can gather all available commands.
    """
    arg_re = re.compile(r"^\(self(?:, )?(?:edit, |edit)?(.*)\)$")

    def legacy(self):
        return sys.version_info < (3, 8, 0)

    def name(self):
        return "commands_browser_plugin_commands_33" if self.legacy() else "commands_browser_plugin_commands"

    def run(self, cmd_dict=None):
        cmd_dict = cmd_dict or {}
        for cmd_type, cmd_info in cmd_types.items():
            self.get_commands(cmd_type, cmd_info["commands"], cmd_dict)

        if self.legacy():
            return sublime.run_command('commands_browser_plugin_commands', {"cmd_dict": cmd_dict})

        items = []
        for command,details in cmd_dict.items():
            items.append(QuickPanelItem(details["name"],
                                        "<i>%s</i>" % details["args"],
                                        "%s.%s" % (details["pkg"] , details["mod"]),
                                        cmd_types[details["type"]]["kind"]))

        items.sort(key=lambda o: o.trigger)

        sublime.active_window().show_quick_panel(items,
                                                 lambda i: self.pick(i, items, cmd_dict))

    def pick(self, idx, items, cmd_dict):
        if idx == -1:
            return

        cmd = cmd_dict[items[idx].trigger]
        module = cmd["mod"].replace('.', '/')
        res = '${packages}/%s/%s.py' % (cmd["pkg"], module)

        sublime.active_window().run_command('open_file', {'file': res})
        view = sublime.active_window().active_view()
        if view.is_loading():
            view.settings().set("_jump_to_class", cmd["class"])
        else:
            _navigate_to(view, cmd["class"])

    def get_commands(self, cmd_type, commands, cmd_dict_out):
        """
        Given a list of commands of a particular type, decode each command in
        the list into a dictionary that describes it and store it into the
        output dictionary keyed by the package that defined it.

        The output dictionary gains keys for each package, where the values are
        dictionaries which contain keys that describe the commands of each of
        the supported typed.
        """
        for command in commands:
            decoded = self.decode_cmd(command, cmd_type)
            cmd_dict_out[decoded["name"]] = decoded

    def decode_cmd(self, command, cmd_type):
        """
        Given a class that implements a command of the provided type, return
        back a dictionary that contains the properties of the command for later
        display.
        """
        return {
            "type": cmd_type,
            "pkg": command.__module__.split(".")[0],
            "mod": ".".join(command.__module__.split(".")[1:]),
            "name": self.get_name(command),
            "args": self.get_args(command),
            "class": command.__name__
        }

    def get_args(self, cmd_class):
        """
        Return a string that represents the arguments to the run method of the
        Sublime command class provided, edited to remove the internal python
        arguments that are not needed to invoke the command from Sublime.
        """
        args = str(inspect.signature(cmd_class.run))
        return self.arg_re.sub(r"{ \1 }", args)

    def get_name(self, cmd_class):
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


class CommandJumpListener(sublime_plugin.ViewEventListener):
    @classmethod
    def is_applicable(cls, settings):
        return settings.has("_jump_to_class")

    def on_load(self):
        symbol = self.view.settings().get("_jump_to_class")
        self.view.settings().erase("_jump_to_class")

        sublime.set_timeout(lambda: _navigate_to(self.view, symbol), 0)