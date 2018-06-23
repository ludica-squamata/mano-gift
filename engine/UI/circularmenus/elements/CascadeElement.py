from .LetterElement import LetterElement
from .InventoryElement import InventoryElement
from .CommandElement import CommandElement


class CascadeElement(LetterElement):
    active = True

    def __init__(self, parent, item):

        nombre = item['name']
        icono = item['icon']
        cascada = item.get('csc')

        super().__init__(parent, nombre, icono)

        for j in range(len(cascada)):
            item = cascada[j]
            obj = None
            if type(item) is dict:
                if 'csc' in item:
                    obj = CascadeElement(self.parent, cascada[j])
                elif 'cmd' in item:
                    obj = CommandElement(self.parent, cascada[j])
            elif hasattr(item, "nombre"):
                obj = InventoryElement(self.parent, cascada[j])

            obj.idx = j
            self.cascada.append(obj)

    def do_action(self):
        if not len(self.cascada):
            return True
