import pygame
from libs.textrect import render_textrect
from globs import Constants as C
from base import _giftSprite

class Dialog (_giftSprite):
    def __init__(self, texto):
        self.layer = C.CAPA_OVERLAYS
        fuente = pygame.font.Font(None, 22)
        fg_color = 0,255,0
        bg_color = 0,0,0
        rect = pygame.Rect((30, 325, C.ANCHO, int(C.ALTO/5)))
        
        self.texto = render_textrect(texto,fuente,rect,fg_color,bg_color)
        super().__init__(self.texto,x=rect.x, y=rect.y)
        
