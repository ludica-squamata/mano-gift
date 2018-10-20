from .LetterElement import LetterElement


class CommandElement(LetterElement):
    active = True
    item = None
    _command = None

    def __init__(self, parent, item):

        nombre = item['name']
        icono = item['icon']
        self._command = item['cmd']

        super().__init__(parent, nombre, icono)

    def command(self):
        self._command()
        self.parent.back()
