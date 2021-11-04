import os
import sys
import json
import string
import sublime

_kind_mapping = {
    "window": (sublime.KIND_ID_FUNCTION, "W", "Window Command"),
    "text": (sublime.KIND_ID_NAMESPACE, "T", "Text Command"),
    "application": (sublime.KIND_ID_TYPE, "A", "Application Command"),
    "find": (sublime.KIND_ID_MARKUP, "F", "Find Command")
}

def num_core_commands(application):
    return len(get_core_commands_data(application))

def get_core_commands_data(application = "st"):
    """
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
    """
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
            text=key,
            value=key,
            annotation=annotation_string,
            details=value.get("doc_string") if value.get("doc_string") else "No description available",
            kind=_kind_mapping[value.get("command_type")]
        )
        items.append(item)
    return items