from engine.base import AzoeSprite
from engine.UI.estilo import Estilo
from pygame import Surface, Rect, SRCALPHA


class BaseWidget(Estilo, AzoeSprite):
    enabled = True
    isSelected = False
    img_sel = None
    img_uns = None

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
        canvas.fill(self.bg_bisel_bg, rect=clip)

        clip = Rect(3, 3, ancho, alto)
        canvas.fill(self.bg_bisel_fg, rect=clip)

        clip = Rect(3, 3, ancho - 7, alto - 7)
        canvas.fill(self.bg_cnvs, rect=clip)

        return canvas

    def create_sunken_canvas(self, ancho, alto):
        canvas = Surface((ancho, alto))

        clip = Rect(0, 0, ancho, alto)
        canvas.fill(self.bg_bisel_fg, rect=clip)

        clip = Rect(3, 3, ancho, alto)
        canvas.fill(self.bg_bisel_bg, rect=clip)

        clip = Rect(3, 3, ancho - 7, alto - 7)
        canvas.fill(self.bg_cnvs, rect=clip)

        return canvas

    def crear_marco(self, ancho, alto):
        marco = Surface([ancho, alto], SRCALPHA)

        clip = Rect(0, 0, ancho, alto)
        marco.fill(self.bg_bisel_bg, rect=clip)

        clip = Rect(3, 3, ancho, alto)
        marco.fill(self.bg_bisel_fg, rect=clip)

        clip = Rect(3, 3, ancho - 7, alto - 7)
        marco.fill((0, 0, 0, 0), clip)

        return marco

    def create_filled_canvas(self, ancho, alto):
        pass

    def create_titled_canvas(self, ancho, alto, titulo):
        marco = self.create_sunken_canvas(ancho, alto)
        megacanvas = Surface((marco.get_width(), marco.get_height() + 17))
        megacanvas.fill(self.bg_cnvs)
        texto = self.fuente_P.render(titulo, True, self.font_none_color, self.bg_cnvs)
        megacanvas.blit(marco, (0, 17))
        megacanvas.blit(texto, (3, 7))

        return megacanvas
