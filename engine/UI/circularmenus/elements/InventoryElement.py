from .LetterElement import LetterElement
from pygame import font
from engine.globs import EngineData as Ed


class InventoryElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):

        if type(item) is dict:
            nombre = item['name']
            icono = item['icon']
            cascada = item.get('csc')
            self.item = None
        else:
            nombre = item.nombre
            icono = item.image
            cascada = None
            self.item = item

        super().__init__(parent, nombre)

        if type(icono) is str:
            self.img_uns = self._crear_icono_texto(icono, 21, 21)
            self.img_sel = self._crear_icono_texto(icono, 33, 33)
        else:
            self.img_uns = self._crear_icono_image(icono, 21, 21)
            self.img_sel = self._crear_icono_image(icono, 33, 33)

        self.rect_uns = self.img_uns.get_rect()
        self.rect_sel = self.img_sel.get_rect()

        if self.in_place:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns

        if cascada is not None:
            for item in cascada:
                self.cascada.append(InventoryElement(self.parent, item))

    def _crear_icono_image(self, icono, w, h):
        image, _rect = self._crear_base(w, h)
        fuente = font.SysFont('Verdana', 12)
        cant = Ed.HERO.inventario.cantidad(self.item)
        render = fuente.render(str(cant), 1, (0, 0, 0))
        renderect = render.get_rect(bottomright=_rect.bottomright)
        iconrect = icono.get_rect(center=_rect.center)

        image.blit(icono, iconrect)
        image.blit(render, renderect)

        return image

    def do_action(self):
        if self.item is not None:
            if hasattr(self.item, 'usar'):
                return Ed.HERO.usar_item(self.item)
        return True
