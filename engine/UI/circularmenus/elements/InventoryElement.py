from engine.globs import EngineData, TEXT_FG
from .LetterElement import LetterElement
from .itemdescription import DescriptiveArea
from pygame import font


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
            fuente = font.Font('engine/libs/Verdana.ttf', 12)
            cant = EngineData.HERO.inventario.cantidad(self.item)
            render = fuente.render(str(cant), 1, TEXT_FG)
            renderect = render.get_rect(bottom=_rect.bottom+1, right=_rect.right-1)
            image.blit(render, renderect)

        iconrect = self.item.image.get_rect(center=_rect.center)
        image.blit(self.item.image, iconrect)

        return image

    def do_action(self):
        if self.item is not None and self.item.tipo == 'consumible':
            value = self.item.usar(EngineData.HERO)
            self.img_sel = self._create_icon_stack(33, 33, True)
            self.image = self.img_sel
            return value
        return True
