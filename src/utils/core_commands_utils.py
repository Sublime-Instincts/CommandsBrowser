import os
import json
import string
import inspect
import sublime

from .miscellaneous_utils import command_kind_type


kind_mapping = {
    "window": command_kind_type("window"),
    "text": command_kind_type("text"),
    "application": command_kind_type("application"),
    "find": command_kind_type("find")
}


def core_commands_doc_panel(window, docs):
    """ For core commands, since they are impemented in ST core, they can't be
    navigated to, unlike plugin based commands that have an associated python file.
    The JSON files have enough information to store the docs however, so we simply
    present that informaion in a panel.

    Args:
        window (sublime.Window): The window object for which the panel has to be
        created.

        docs (List): This is a list of 2 items. The first one is the command name
        and the second one is the command metadata.

    Returns:
        None
    """
    doc_panel = window.create_output_panel("CommandsBrowser")
    doc_panel.set_read_only(False)

    final_doc_string = ""
    description_string = f"""
    Name of the command: {docs[0]}

    Description: {docs[1]["doc_string"]}
    """
    final_doc_string += inspect.cleandoc(description_string.strip()) + "\n" * 2
    final_doc_string += "Arguments:" + "\n" * 2

    if docs[1].get("args") is not None:
        max_arg_length = max([len(doc["name"]) for doc in docs[1]["args"]])
        max_length = max([(len(doc["name"]) + len(doc["type"]) + 4) for doc in docs[1]["args"]])

        for doc in docs[1]["args"]:
            length_1 = abs(max_arg_length - len(doc["name"]))
            length_2 = abs(max_length - (len(doc["name"]) + len(doc["type"]) + length_1 + 4))

            doc_string = doc["doc_string"] if doc["doc_string"] is not None else "No available description."

            initial_string = f"""
            {doc["name"]}{"":^{length_1}} ({doc["type"]}){"":^{length_2}} - {doc_string}
            """
            final_doc_string += initial_string.strip() + "\n"
    else:
        final_doc_string += "No known args exist for this command."

    doc_panel.run_command("insert", { "characters": final_doc_string })
    doc_panel.settings().set("syntax", "Packages/CommandsBrowser/resources/CommandsBrowser.sublime-syntax")
    doc_panel.settings().set("gutter", False)
    doc_panel.set_read_only(True)

    window.run_command("show_panel", {
        "panel": "output.CommandsBrowser",
    })


def get_core_commands_data(application = "st"):
    """ Given the application type, generates a list of items representing
    command data that can be returned from a CommandInputHandler.list_items
    method.

    Args:
        application (str): The application for which the commands need to be
        retrived. Valid values are 'st' (Sublime Text) or 'sm' (Sublime Merge).

    Returns:
        final_dict (Dict): The final dictionary of commands and their docs.
    """

    json_file_names = [a for a in sublime.find_resources("*.json") if a.startswith(f"Packages/CommandsBrowser/{application}_commands_metadata")]
    final_dict = {}
    for file_name in json_file_names:
        data = json.loads(sublime.load_resource(file_name))
        if data is not None:
            final_dict.update(data)
    return final_dict
