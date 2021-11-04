import sublime
import inspect
import sublime_plugin


class CoreCommandsDocPanelCommand(sublime_plugin.WindowCommand):


    def run(self, docs):
        doc_panel = self.window.create_output_panel("CoreCommandsBrowser")
        final_doc_string = ""
        description_string = f"""
        Name of the command: {docs[0]}

        Description: {docs[1]["doc_string"]}
        """

        final_doc_string += inspect.cleandoc(description_string.strip()) + "\n" * 2
        final_doc_string += "Arguments:" + "\n" * 2

        # Find the longest argument name.

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
            final_doc_string += "No args exist for this command."

        doc_panel.run_command("insert", { "characters": final_doc_string })
        doc_panel.settings().set("syntax", "Packages/CoreCommandsBrowser/resources/CoreCommandsBrowser.sublime-syntax")
        doc_panel.settings().set("context_menu", "CoreCommandsBrowser.sublime-menu")
        self.window.run_command("show_panel", {
            "panel": "output.CoreCommandsBrowser",
        })