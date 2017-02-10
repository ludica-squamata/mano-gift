from engine.globs import EngineData as Ed
from .LetterElement import LetterElement
from .title import Title
from .itemdescription import DescriptiveArea


class InventoryElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):

        self.item = item

        super().__init__(parent, self.item.nombre)

        self.img_uns = self._crear_icono_image(21, 21)
        self.img_sel = self._crear_icono_image(33, 33)

        self.rect_uns = self.img_uns.get_rect()
        self.rect_sel = self.img_sel.get_rect()

        if self.in_place:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns

        self.title = Title(self, self.item.nombre)
        if self.item is not None:
            self.description = DescriptiveArea(self, item)

    def _crear_icono_image(self, w, h):
        image, _rect = self._crear_base(w, h)
        cant = Ed.HERO.inventario.cantidad(self.item)
        render = self.fuente_MP.render(str(cant), 1, self.font_none_color)
        renderect = render.get_rect(bottomright=_rect.bottomright)
        iconrect = self.item.image.get_rect(center=_rect.center)

        image.blit(self.item.image, iconrect)
        image.blit(render, renderect)

        return image

    def do_action(self):
        if self.item is not None and self.item.tipo == 'consumible':
            value = self.item.usar(Ed.HERO)
            self.img_uns = self._crear_icono_image(21, 21)
            self.img_sel = self._crear_icono_image(33, 33)
            self.image = self.img_sel
            return value
        return True
