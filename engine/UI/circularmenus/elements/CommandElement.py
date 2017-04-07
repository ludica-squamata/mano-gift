from .LetterElement import LetterElement


class CommandElement(LetterElement):
    active = True
    item = None
    command = None

    def __init__(self, parent, item):

        nombre = item['name']
        icono = item['icon']
        self.command = item['cmd']

        super().__init__(parent, nombre, icono)

    def do_action(self):
        self.command()
        self.parent.back()
        return True
