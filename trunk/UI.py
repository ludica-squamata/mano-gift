import pygame
from libs.textrect import render_textrect
from globs import Constants as C, World as W
from base import _giftSprite

class Ventana (_giftSprite):
    canvas = None
    bg_cnvs = 125,125,125 # gris
    bg_color = 0,0,0
    fg_color = 0,125,255
    posicion = x,y = 0,0
    tamanio = ancho,alto = 0,0
    def __init__(self,image):
        super().__init__(image)
    
    def elegir_opcion(self,j,m):
        self.sel += j
        if self.sel < 1: self.sel = 1
        elif self.sel > 2: self.sel = 2
        pygame.draw.line(self.image,self.fg_color,(3,self.sel*22),(C.ANCHO-5,self.sel*22))
        pygame.draw.line(self.image,self.bg_color,(3,(self.sel+m)*22),(C.ANCHO-5,(self.sel+m)*22))

        return self.sel
    
class Dialog (Ventana):
    fuente = None
    sel = 1
    posicion = x,y = 0,384
    def __init__(self, texto):
        self.canvas = pygame.Surface((int(C.ANCHO), int(C.ALTO/5)))
        self.canvas.fill(self.bg_cnvs)
        
        self.fuente = pygame.font.SysFont('verdana', 16)
        rect = pygame.Rect((self.posicion, (C.ANCHO-7, int(C.ALTO/5)-7)))
        image = render_textrect(texto,self.fuente,rect,self.fg_color,self.bg_color)
        
        self.canvas.blit(image,(3,3))
        super().__init__(self.canvas)
        self.ubicar(*rect.topleft)
        self.dirty = 2

    def setText(self, texto):
        rect = pygame.Rect((3, 3, C.ANCHO-7, int(C.ALTO/5)-7))
        if W.onSelect:
            render = render_textrect(texto,self.fuente,rect,self.fg_color,self.bg_color)
            self.canvas.blit(render,rect)
            pygame.draw.line(self.canvas,self.fg_color,(0,self.sel*22),(C.ANCHO-7,self.sel*22))
            self.image = self.canvas
        else:
            render = render_textrect(texto,self.fuente,rect,self.fg_color,self.bg_color)
            self.canvas.blit(render,rect)
            self.image = self.canvas

class Menu (Ventana):
    def __init__(self):
        self.canvas = pygame.Surface((int(C.ANCHO)-20, int(C.ALTO)-20))
        clip = pygame.Rect(3,3,int(C.ANCHO)-27, int(C.ALTO)-27)
        self.canvas.fill(self.bg_cnvs)
        self.canvas.fill(self.bg_color,rect=clip)
        
        fuente = pygame.font.SysFont('verdana', 16)
        fuente.set_underline(True)
        rect = pygame.Rect((-1,-1),(int(C.ANCHO)-27,30))
        titulo =  render_textrect('Pausa',fuente,rect,self.fg_color,self.bg_color,1)
        self.canvas.blit(titulo,(3,3))
        
        super().__init__(self.canvas)
        self.ubicar(10,10)
        self.dirty = 2
        W.onPause = True
    
