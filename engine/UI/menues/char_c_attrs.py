from engine.UI.widgets import BaseWidget


class AttrsScreen(BaseWidget):
    hidden = True

    # noinspection PyMissingConstructor
    def __init__(self, parent):
        self.parent = parent
        self.ins_txt = 'Y esto otro son  las instrucciones para los Atributos'

    def toggle_hidden(self):
        self.hidden = not self.hidden
