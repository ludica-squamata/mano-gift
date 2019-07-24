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


class DialogObjectElement(LetterElement):
    active = True
    item = None
    idx = 0

    def __init__(self, parent, idx, item):
        self.item = item
        self.idx = idx
        self.img_uns = self._create(21, 21)
        self.img_sel = self._create(33, 33)

        super().__init__(parent, self.item.nombre, None)

    def _create(self, w, h):
        image, _rect = self._crear_base(w, h)
        iconrect = self.item.image.get_rect(center=_rect.center)
        image.blit(self.item.image, iconrect)

        return image

    def do_action(self):
        pass
