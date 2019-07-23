from .letter import LetterElement


class DialogOptionElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):

        nombre = item['name']
        icono = item['icon']
        self.item = item['item']
        self.idx = item['idx']

        super().__init__(parent, nombre, icono)
