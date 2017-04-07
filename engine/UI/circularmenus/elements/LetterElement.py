from engine.IO.menucircular import BaseElement
from pygame import Surface, SRCALPHA
from engine.UI.estilo import Estilo
from .title import Title


class LetterElement(BaseElement, Estilo):
    title = None

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

        if self.in_place:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns

        self.title = Title(self, nombre)

    def _crear_base(self, w, h):
        image = Surface((w, h), SRCALPHA)
        image.fill(self.font_none_color)
        gris = self.bg_cnvs
        gris.a = 200
        image.fill(gris, (1, 1, w - 2, h - 2))

        rect = image.get_rect()
        return image, rect

    def _crear_icono_texto(self, icono, w, h):
        image, _rect = self._crear_base(w, h)
        render = self.fuente_Ib.render(icono, 1, self.font_none_color)
        renderect = render.get_rect(center=_rect.center)
        image.blit(render, renderect)
        return image

    def _crear_icono_image(self, icono, w, h):
        image, _rect = self._crear_base(w, h)
        iconrect = icono.get_rect(center=_rect.center)
        image.blit(icono, iconrect)

        return image
