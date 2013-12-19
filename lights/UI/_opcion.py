from .Colores import Colores
from base.base import _giftSprite
from pygame import font, Rect
from libs.textrect import render_textrect

class _opcion (Colores,_giftSprite):
    def __init__(self,texto,ancho,pos):
        fuente = font.SysFont('verdana', 16)
        _rect = Rect((-1,-1),(ancho,fuente.get_height()+1))
        
        image = render_textrect(texto,fuente,_rect,self.font_none_color,self.bg_cnvs)
        super().__init__(image)
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1