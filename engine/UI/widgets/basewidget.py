from engine.base import GiftSprite
from engine.UI.estilo import Estilo
from pygame import Surface, Rect


class BaseWidget(Estilo, GiftSprite):
    enabled = True
    #canvas = None
    isSelected = False

    def __init__(self, img):
        super().__init__(img)

    def ser_elegido(self):
        """Cambia la imagen a la versión resaltada"""

        self.image = self.img_sel
        self.isSelected = True

    def ser_deselegido(self):
        """Cambia la imagen a la versión no elegida"""

        self.image = self.img_uns
        self.isSelected = False

    def create_raised_canvas(self, ancho, alto):
        canvas = Surface((ancho, alto))

        clip = Rect(0, 0, ancho, alto)
        canvas.fill(self.bg_bisel_bg, rect = clip)

        clip = Rect(3, 3, ancho, alto)
        canvas.fill(self.bg_bisel_fg, rect = clip)

        clip = Rect(3, 3, ancho - 7, alto - 7)
        canvas.fill(self.bg_cnvs, rect = clip)

        return canvas

    def create_sunken_canvas(self, ancho, alto):
        canvas = Surface((ancho, alto))

        clip = Rect(0, 0, ancho, alto)
        canvas.fill(self.bg_bisel_fg, rect = clip)

        clip = Rect(3, 3, ancho, alto)
        canvas.fill(self.bg_bisel_bg, rect = clip)

        clip = Rect(3, 3, ancho - 7, alto - 7)
        canvas.fill(self.bg_cnvs, rect = clip)

        return canvas

    def crear_marco(self, ancho, alto):
        marco = Surface([ancho, alto])

        clip = Rect(0, 0, ancho, alto)
        marco.fill(self.bg_bisel_bg, rect = clip)

        clip = Rect(3, 3, ancho, alto)
        marco.fill(self.bg_bisel_fg, rect = clip)

        clip = Rect(3, 3, ancho - 7, alto - 7)
        marco.set_clip(clip)

        return marco

    def create_filled_canvas(self,ancho,alto):
        pass
