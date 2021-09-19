import os
import json
import string
import sublime
import sublime_plugin

def plugin_loaded():
    global settings
    settings = sublime.load_settings("CoreCommandsViewer.sublime-settings")


kind_mapping = {
    "window": (sublime.KIND_ID_FUNCTION, "W", "Window Command"),
    "text": (sublime.KIND_ID_NAMESPACE, "T", "Text Command"),
    "application": (sublime.KIND_ID_TYPE, "A", "Application Command"),
    "find": (sublime.KIND_ID_MARKUP, "F", "Find Command")
}


class CoreCommandsViewerCommand(sublime_plugin.WindowCommand):

    def run(self, application):
        commands_data = self.get_commands_data(application = application)
        items = []
        for key, value in commands_data.items():
            if not value.get("location"):
                annotation_string = "{}".format(value.get("type"))
            else:
                annotation_string = "{} ({})".format(value.get("type"), value.get("location"))

            item = sublime.QuickPanelItem(
                trigger=key,
                annotation=annotation_string,
                details=value.get("doc_string") if value.get("doc_string") else "No description available",
                kind=kind_mapping[value.get("command_type")]
            )
            items.append(item)

        self.window.show_quick_panel(
            items = items,
            on_select = lambda id: self.on_select(id, items, commands_data),
            on_highlight = lambda id: self.on_highlight(id, items, commands_data),
            placeholder = f"Browse through {len(items)} available core & default commands ...",
            flags = sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT
        )


    def on_select(self, id, items, final_dict):
        if id < 0:
            return
        if settings.get("ccv.auto_open_panel_on_navigate"):
            return
        docs = self.get_docs(id, items, final_dict)
        self.window.run_command("command_doc_panel", { "docs": docs })

    @staticmethod
    def get_commands_data(application = "st"):
        metadata_folder = os.path.join(os.path.dirname(__file__), f"{application}_commands_metadata")
        json_file_names = [name + ".json" for name in list(string.ascii_lowercase)]
        final_dict = {}
        for file_name in json_file_names:
            with open(os.path.join(metadata_folder, file_name), "r") as file:
                data = json.loads(file.read())
                if data is not None:
                    final_dict.update(data)
        return final_dict


    def on_highlight(self, id, items, final_dict):
        if id < 0:
            return
        docs = self.get_docs(id, items, final_dict)
        if not settings.get("ccv.auto_open_panel_on_navigate"):
            return
        self.window.run_command("command_doc_panel", { "docs": docs })

    @staticmethod
    def get_docs(id, items, final_dict):
        item = items[id].trigger
        for key, value in final_dict.items():
            if key == item:
                docs = value.get("args")
        return docs


class CommandDocPanelCommand(sublime_plugin.WindowCommand):

    def run(self, docs):
        doc_panel = self.window.create_output_panel("DocPanel")
        final_doc_string = ""
        if docs is not None:
            for doc in docs:
                doc_string = doc["doc_string"] if doc["doc_string"] is not None else "No available description."
                initial_string = f"""
                {doc["name"]} ({doc["type"]}){"":^10} - {doc_string}
                """
                final_doc_string += initial_string.strip() + "\n"
        else:
            final_doc_string = "No args exist for this command."
        doc_panel.run_command("insert", { "characters": final_doc_string })
        doc_panel.settings().set("syntax", "Packages/CoreCommandsViewer/resources/CoreCommandsViewer.sublime-syntax")
        self.window.run_command("show_panel", {
            "panel": "output.DocPanel"
        })