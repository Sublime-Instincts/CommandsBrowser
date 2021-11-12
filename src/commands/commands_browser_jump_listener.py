import sublime
import sublime_plugin


class CommandsBrowserCommandJumpListener(sublime_plugin.ViewEventListener):


    @classmethod
    def is_applicable(cls, settings):
        return settings.has("_jump_to_class")


    def on_load(self):
        symbol = self.view.settings().get("_jump_to_class")
        self.view.settings().erase("_jump_to_class")

        sublime.set_timeout(lambda: navigate_to(self.view, symbol), 0)
