import sublime

def command_kind_type(command_type):
    """
    """

    if command_type == "text":
        return (sublime.KIND_ID_NAMESPACE, "T", "Text Command")

    if command_type == "window":
        return (sublime.KIND_ID_FUNCTION, "W", "Window Command")

    if command_type == "application":
        return (sublime.KIND_ID_TYPE, "A", "Application Command")

    if command_type == "find":
        return (sublime.KIND_ID_MARKUP, "F", "Find Command")

