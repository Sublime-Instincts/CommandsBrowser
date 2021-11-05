import os
import json
import string
import inspect
import sublime


_kind_mapping = {
    "window": (sublime.KIND_ID_FUNCTION, "W", "Window Command"),
    "text": (sublime.KIND_ID_NAMESPACE, "T", "Text Command"),
    "application": (sublime.KIND_ID_TYPE, "A", "Application Command"),
    "find": (sublime.KIND_ID_MARKUP, "F", "Find Command")
}


def core_commands_doc_panel(window, docs):
    """
    """
    doc_panel = window.create_output_panel("CommandsBrowser")
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
            length_1 = max_arg_length - len(doc["name"])
            length_2 = max_length - (len(doc["name"]) + len(doc["type"]) + length_1 + 4)
            doc_string = doc["doc_string"] if doc["doc_string"] is not None else "No available description."
            initial_string = f"""
            {doc["name"]}{"":^{length_1}} ({doc["type"]}){"":^{length_2}} - {doc_string}
            """
            final_doc_string += initial_string.strip() + "\n"
    else:
        final_doc_string += "No known args exist for this command."

    doc_panel.run_command("insert", { "characters": final_doc_string })
    doc_panel.settings().set("syntax", "Packages/CommandsBrowser/resources/CommandsBrowser.sublime-syntax")
    doc_panel.settings().set("context_menu", "CommandsBrowser.sublime-menu")
    window.run_command("show_panel", {
        "panel": "output.CommandsBrowser",
    })


def num_core_commands(application):
    """ Given the application type, returns the number of commands.

    Args:
        application (str): The application for which the number of commands needs
        to be calculated. Valid values are 'st' (Sublime Text) or 'sm' (Sublime Merge).

    Returns:
        length (int): The number of commands for that application.
    """
    return len(get_core_commands_data(application))


def get_core_commands_data(application = "st"):
    """ Given the application type, generates a list of items representing
    command data that can be returned from a CommandInputHandler.list_items
    method.

    Args:
        application (str): The application for which the commands need to be
        retrived. Valid values are 'st' (Sublime Text) or 'sm' (Sublime Merge).

    Returns:
        final_dict (Dict):
    """
    package_path = os.path.join(sublime.packages_path(), "CommandsBrowser")
    metadata_folder = os.path.join(package_path, f"{application}_commands_metadata")
    json_file_names = [name + ".json" for name in list(string.ascii_lowercase)]
    final_dict = {}
    for file_name in json_file_names:
        with open(os.path.join(metadata_folder, file_name), "r") as file:
            data = json.loads(file.read())
            if data is not None:
                final_dict.update(data)
    return final_dict


def generate_core_commands_list_items(application):
    """ Given the application type, generates a list of items representing
    command data that can be returned from a CommandInputHandler.list_items
    method.

    Args:
        application (str): The application for which the commands need to be
        retrived. Valid values are 'st' (Sublime Text) or 'sm' (Sublime Merge).

    Returns:
        items (List[sublime.ListInputItem]): The items list representing the
        command information.
    """
    commands_data = get_core_commands_data(application = application)
    items = []
    for key, value in commands_data.items():
        if not value.get("location"):
            annotation_string = "{}".format(value.get("type"))
        else:
            annotation_string = "{} ({})".format(value.get("type"), value.get("location"))

        if application == "sm":
            annotation_string = "{} ({})".format(value.get("type"), value.get("added"))

        item = sublime.ListInputItem(
            text = key,
            value = (key, commands_data[key]),
            annotation = annotation_string,
            details = value.get("doc_string") if value.get("doc_string") else "No description available",
            kind = _kind_mapping[value.get("command_type")]
        )

        items.append(item)
    return items
