from .LetterElement import LetterElement
from .title import Title
from .InventoryElement import InventoryElement
from .CommandElement import CommandElement


class CascadeElement(LetterElement):
    active = True

    def __init__(self, parent, item):

        nombre = item['name']
        icono = item['icon']
        cascada = item.get('csc')

        super().__init__(parent, nombre)

        self.img_uns = self._crear_icono_texto(icono, 21, 21)
        self.img_sel = self._crear_icono_texto(icono, 33, 33)
        self.rect_uns = self.img_uns.get_rect()
        self.rect_sel = self.img_sel.get_rect()

        if self.in_place:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns

        self.title = Title(self, nombre)

        for j in range(len(cascada)):
            item = cascada[j]
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
