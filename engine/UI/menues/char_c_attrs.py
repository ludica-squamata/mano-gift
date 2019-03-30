from engine.UI.widgets import BaseWidget


class AttrsScreen(BaseWidget):
    hidden = True

    # noinspection PyMissingConstructor
    def __init__(self, parent):
        self.parent = parent

    def toggle_hidden(self):
        self.hidden = not self.hidden
