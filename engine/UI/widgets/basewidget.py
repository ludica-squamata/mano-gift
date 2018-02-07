from engine.base import AzoeSprite
from pygame import Surface, Rect, SRCALPHA, font
from engine.globs.colores import CANVAS_BG, BISEL_BG, BISEL_FG, TEXT_FG


class BaseWidget(AzoeSprite):
    enabled = True
    isSelected = False
    img_sel = None
    img_uns = None
    w, h = 0, 0

    def ser_elegido(self):
        """Cambia la imagen a la versión resaltada"""
        if self.enabled:
            self.image = self.img_sel
            self.isSelected = True

    def ser_deselegido(self):
        """Cambia la imagen a la versión no elegida"""
        if self.enabled:
            self.image = self.img_uns
            self.isSelected = False

    @staticmethod
    def create_raised_canvas(ancho, alto):
        canvas = Surface((ancho, alto))

        clip = Rect(0, 0, ancho, alto)
        canvas.fill(BISEL_BG, rect=clip)

        clip = Rect(3, 3, ancho, alto)
        canvas.fill(BISEL_FG, rect=clip)

        clip = Rect(3, 3, ancho - 7, alto - 7)
        canvas.fill(CANVAS_BG, rect=clip)

        return canvas

    @staticmethod
    def create_sunken_canvas(ancho, alto):
        canvas = Surface((ancho, alto))

        clip = Rect(0, 0, ancho, alto)
        canvas.fill(BISEL_FG, rect=clip)

        clip = Rect(3, 3, ancho, alto)
        canvas.fill(BISEL_BG, rect=clip)

        clip = Rect(3, 3, ancho - 7, alto - 7)
        canvas.fill(CANVAS_BG, rect=clip)

        return canvas

    @staticmethod
    def crear_marco(ancho, alto):
        marco = Surface([ancho, alto], SRCALPHA)

        clip = Rect(0, 0, ancho, alto)
        marco.fill(BISEL_BG, rect=clip)

        clip = Rect(3, 3, ancho, alto)
        marco.fill(BISEL_FG, rect=clip)

        clip = Rect(3, 3, ancho - 7, alto - 7)
        marco.fill((0, 0, 0, 0), clip)

        return marco

    @staticmethod
    def create_filled_canvas(ancho, alto):
        pass

    def create_titled_canvas(self, ancho, alto, titulo):
        fuente = font.Font('engine/libs/Verdana.ttf', 14)
        marco = self.create_sunken_canvas(ancho, alto)
        megacanvas = Surface((marco.get_width(), marco.get_height() + 17))
        megacanvas.fill(CANVAS_BG)
        texto = fuente.render(titulo, True, TEXT_FG, CANVAS_BG)
        megacanvas.blit(marco, (0, 17))
        megacanvas.blit(texto, (3, 7))

        return megacanvas
