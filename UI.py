import pygame
from libs.textrect import render_textrect
from globs import Constants as C, World as W
from base import _giftSprite

class Dialog (_giftSprite):
    fg_color = 0,125,255
    bg_color = 0,0,0
    fuente = None
    sel = 1
    def __init__(self, texto):
        self.fuente = pygame.font.SysFont('verdana', 16)
        rect = pygame.Rect((30, 325, C.ANCHO, int(C.ALTO/5)))
        image = render_textrect(texto,self.fuente,rect,self.fg_color,self.bg_color)
        super().__init__(image,x=rect.x, y=rect.y)
        self.rect = pygame.Rect((0, 384, C.ANCHO, int(C.ALTO/5)))
        self.dirty = 2

    def setText(self, texto):
        rect = pygame.Rect((30, 325, C.ANCHO, int(C.ALTO/5)))
        if W.onSelect:
            render = render_textrect(texto,self.fuente,rect,self.fg_color,self.bg_color)
            pygame.draw.line(render,self.fg_color,(0,self.sel*20),(470,self.sel*20))
            self.image = render
        else:
            self.image = render_textrect(texto,self.fuente,rect,self.fg_color,self.bg_color)
    
    def elegir_opcion(self,j,m):
        self.sel += j
        if self.sel < 1: self.sel = 1
        elif self.sel > 2: self.sel = 2
        pygame.draw.line(self.image,self.fg_color,(0,self.sel*20),(470,self.sel*20))
        pygame.draw.line(self.image,self.bg_color,(0,(self.sel+m)*20),(470,(self.sel+m)*20))

        return self.sel

