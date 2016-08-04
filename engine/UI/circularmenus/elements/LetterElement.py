from engine.IO.menucircular import BaseElement
from pygame import Surface, SRCALPHA
from engine.UI.estilo import Estilo


class LetterElement(BaseElement, Estilo):

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
