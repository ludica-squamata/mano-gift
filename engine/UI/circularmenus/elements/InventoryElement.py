from engine.globs import EngineData as Ed
from .LetterElement import LetterElement
from .itemdescription import DescriptiveArea


class InventoryElement(LetterElement):
    active = True
    item = None
    description = None

    def __init__(self, parent, item):

        self.item = item
        self.img_uns = self._create_icon_stack(21, 21, False)
        self.img_sel = self._create_icon_stack(33, 33, True)

        super().__init__(parent, self.item.nombre, None)
        self.description = DescriptiveArea(self, item)

    def _create_icon_stack(self, w, h, count):
        image, _rect = self._crear_base(w, h)
        if count:
            cant = Ed.HERO.inventario.cantidad(self.item)
            render = self.fuente_MP.render(str(cant), 1, self.font_none_color)
            renderect = render.get_rect(bottom=_rect.bottom+1, right=_rect.right-1)
            image.blit(render, renderect)

        iconrect = self.item.image.get_rect(center=_rect.center)
        image.blit(self.item.image, iconrect)

        return image

    def do_action(self):
        if self.item is not None and self.item.tipo == 'consumible':
            value = self.item.usar(Ed.HERO)
            self.img_sel = self._create_icon_stack(33, 33, True)
            self.image = self.img_sel
            return value
        return True
