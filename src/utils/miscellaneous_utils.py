import sublime


def command_kind_type(command_type):
    """ Based on the command_type, returns a tuple that can the be used to have
    appropriate kind information in the quick panel.

    Args:
        command_type (str): The type of command. Valid values are "text", "find",
        "window" and "application".

    Returns:
        kind_information (Tuple[kind_type, str, str]): The kind information tuple.
    """

    if command_type == "text":
        return (sublime.KIND_ID_NAMESPACE, "T", "Text Command")

    if command_type == "window":
        return (sublime.KIND_ID_FUNCTION, "W", "Window Command")

    if command_type == "application":
        return (sublime.KIND_ID_TYPE, "A", "Application Command")

    if command_type == "find":
        return (sublime.KIND_ID_MARKUP, "F", "Find Command")
