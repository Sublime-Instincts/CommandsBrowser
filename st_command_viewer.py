import os
import yaml
import string
import sublime
import sublime_plugin

kind_mapping = {
    "window": (sublime.KIND_ID_FUNCTION, "W", "Window Command"),
    "text": (sublime.KIND_ID_NAMESPACE, "T", "Text Command"),
    "application": (sublime.KIND_ID_FUNCTION, "A", "Application Command"),
    "find": (sublime.KIND_ID_MARKUP, "F", "Find Command")
}

class CoreCommandsViewerCommand(sublime_plugin.WindowCommand):

    def run(self):
        metadata_folder = os.path.join(os.path.dirname(__file__), "st_commands_metadata")
        yaml_file_names = [name + ".yaml" for name in list(string.ascii_lowercase)]
        final_dict = {}
        for file_name in yaml_file_names:
            with open(os.path.join(metadata_folder, file_name), "r") as file:
                command_data = file.read()
                data = yaml.load(command_data, Loader=yaml.FullLoader)
                if data is not None:
                    final_dict.update(data)
        items = []
        for key, value in final_dict.items():
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
            items=items,
            on_select=self.on_select,
            on_highlight=lambda id: self.on_highlight(id, items, final_dict),
            placeholder="Browse through available core & default commands ...",
            flags=sublime.KEEP_OPEN_ON_FOCUS_LOST | sublime.MONOSPACE_FONT
        )

    def on_select(self, id):
        pass

    def on_highlight(self, id, items, final_dict):
        if id >= 0:
            item = items[id].trigger
            for key, value in final_dict.items():
                if key == item:
                    docs = value.get("args")
            self.window.run_command("command_doc_panel", { "docs": docs })

class CommandDocPanelCommand(sublime_plugin.WindowCommand):

    def run(self, docs):
        doc_panel = self.window.create_output_panel("DocPanel")
        final_doc_string = ""
        if docs is not None:
            for doc in docs:
                initial_string = """
                {} ({}) - {}
                """.format(doc["name"], doc["type"], doc["doc_string"])
                final_doc_string += initial_string.strip() + "\n"
        else:
            final_doc_string = "No args exist for this command."
        doc_panel.run_command("insert", { "characters": final_doc_string })
        doc_panel.settings().set("syntax", "Packages/CoreCommandsViewer/DocPanel.sublime-syntax")
        self.window.run_command("show_panel", {
            "panel": "output.DocPanel"
        })