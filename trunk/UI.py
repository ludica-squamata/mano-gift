import pygame
from libs.textrect import render_textrect
from globs import Constants as C
from base import _giftSprite

class Dialog (_giftSprite):
    fg_color = 0,255,0
    bg_color = 0,0,0
    fuente = None
    def __init__(self, texto):
        self.fuente = pygame.font.Font(None, 22)
        rect = pygame.Rect((30, 325, C.ANCHO, int(C.ALTO/5)))
        texto = render_textrect(texto,self.fuente,rect,self.fg_color,self.bg_color)
        super().__init__(texto,x=rect.x, y=rect.y)
        self.rect = pygame.Rect((0, 384, C.ANCHO, int(C.ALTO/5)))
        self.dirty = 2

    def setText(self, texto):
        self.image = render_textrect(texto,self.fuente,rect,self.fg_color,self.bg_color)
