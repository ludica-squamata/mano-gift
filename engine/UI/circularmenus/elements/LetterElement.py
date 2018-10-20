from engine.IO.menucircular import BaseElement
from pygame import Surface, SRCALPHA, font
from engine.globs.colores import TEXT_FG, CANVAS_BG
from .title import Title


class LetterElement(BaseElement):
    title = None
    active = True

    def __init__(self, parent, nombre, icono):

        super().__init__(parent, nombre)

        if type(icono) is str:
            self.img_uns = self._crear_icono_texto(icono, 21, 21)
            self.img_sel = self._crear_icono_texto(icono, 33, 33)

        elif type(icono) is Surface:
            self.img_uns = self._crear_icono_image(icono, 21, 21)
            self.img_sel = self._crear_icono_image(icono, 33, 33)

        self.rect_uns = self.img_uns.get_rect()
        self.rect_sel = self.img_sel.get_rect()

        if self.check_placement():
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns

        self.title = Title(self, nombre)

    @staticmethod
    def _crear_base(w, h):
        image = Surface((w, h), SRCALPHA)
        image.fill(TEXT_FG)
        gris = CANVAS_BG
        gris.a = 200
        image.fill(gris, (1, 1, w - 2, h - 2))

        rect = image.get_rect()
        return image, rect

    def _crear_icono_texto(self, icono, w, h):
        fuente = font.Font('engine/libs/Verdanab.ttf', 15)
        image, _rect = self._crear_base(w, h)
        render = fuente.render(icono, 1, TEXT_FG)
        renderect = render.get_rect(center=_rect.center)
        image.blit(render, renderect)
        return image

    def _crear_icono_image(self, icono, w, h):
        image, _rect = self._crear_base(w, h)
        iconrect = icono.get_rect(center=_rect.center)
        image.blit(icono, iconrect)

        return image
