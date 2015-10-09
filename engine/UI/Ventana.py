from .widgets import BaseWidget
from pygame import Surface, Rect, font, draw
from engine.libs.textrect import render_textrect


class Ventana(BaseWidget):
    posicion = x, y = 0, 0
    tamanio = ancho, alto = 0, 0
    sel = 0
    opciones = 0

    def __init__(self, image):
        super().__init__(image)

    def crear_espacio_titulado(self, ancho, alto, titulo):
        marco = self.crear_inverted_canvas(ancho, alto)
        megacanvas = Surface((marco.get_width(), marco.get_height() + 17))
        megacanvas.fill(self.bg_cnvs)
        texto = self.fuente_P.render(titulo, True, self.font_none_color, self.bg_cnvs)
        megacanvas.blit(marco, (0, 17))
        megacanvas.blit(texto, (3, 7))

        return megacanvas

    def posicionar_cursor(self, i):
        self.sel += i
        if self.sel < 0:
            self.sel = 0

        elif self.sel > self.opciones - 1:
            self.sel = self.opciones - 1

    def crear_titulo(self, titulo, fg_color, bg_color, ancho):
        ttl_rect = Rect((3, 3), (ancho - 7, 30))
        ttl_txt = render_textrect(titulo, self.fuente_Mu, ttl_rect, fg_color, bg_color, 1)
        self.canvas.blit(ttl_txt, ttl_rect.topleft)
