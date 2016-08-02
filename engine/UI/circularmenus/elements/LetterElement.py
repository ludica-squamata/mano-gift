from engine.IO.menucircular import BaseElement
from pygame import font, Surface, SRCALPHA
from pygame.sprite import Sprite


class LetterElement(BaseElement):
    def __init__(self, parent, nombre):
        super().__init__(parent, nombre)
        self._crear_titulo()

    @staticmethod
    def _crear_base(w, h):
        image = Surface((w, h), SRCALPHA)
        image.fill((0, 0, 0, 255))
        image.fill((125, 125, 125, 200), (1, 1, w - 2, h - 2))

        rect = image.get_rect()
        return image, rect

    def _crear_icono_texto(self, icono, w, h):
        image, _rect = self._crear_base(w, h)

        fuente = font.SysFont('Verdana', 15, bold=True)
        render = fuente.render(icono, 1, (0, 0, 0))
        renderect = render.get_rect(center=_rect.center)
        image.blit(render, renderect)
        return image

    def _crear_titulo(self):
        fuente = font.SysFont('Verdana', 15, bold=True)
        w, h = fuente.size(self.nombre)
        negro = 0, 0, 0
        gris = 125, 125, 125

        self.title = Sprite()
        self.title.active = True
        self.title.image = Surface((w + 6, h + 2))
        self.title.image.fill(gris, (1, 1, w + 4, h))
        self.title.image.blit(fuente.render(self.nombre, 1, negro, gris), (2, 1))
        self.title.rect = self.title.image.get_rect()

    def update(self):
        super().update()
        self.title.rect.center = (self.rect.centerx, self.rect.bottom + 15)
