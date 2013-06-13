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
    botones = pygame.sprite.LayeredDirty()
    cur_pos = 0
    
    def __init__(self):
        self.canvas = pygame.Surface((int(C.ANCHO)-20, int(C.ALTO)-20))
        clip = pygame.Rect(3,3,int(C.ANCHO)-27, int(C.ALTO)-27)
        self.canvas.fill(self.bg_cnvs)
        self.canvas.fill(self.bg_color,rect=clip)
        
        ttl_fuente = pygame.font.SysFont('verdana', 16)
        ttl_fuente.set_underline(True)
        ttl_rect = pygame.Rect((3,3),(int(C.ANCHO)-27,30))
        titulo =  render_textrect('Pausa',ttl_fuente,ttl_rect,self.fg_color,self.bg_color,1)
        self.canvas.blit(titulo,ttl_rect.topleft)

        btn_texts= ['Personaje','Inventario','Grupo','Opciones','Salir']
        btn_pos = [(7,93),(260,93),(7,253),(260,253),(125,349)]
        for i in range(len(btn_texts)):
            boton = self._crear_boton(btn_texts[i],*btn_pos[i])
            self.botones.add(boton)
        
        selected = self.botones.get_sprite(self.cur_pos)
        selected.serElegido()
        self.botones.draw(self.canvas)
        super().__init__(self.canvas)
        self.ubicar(10,10)
        self.dirty = 2
        W.onPause = True
            
    def _crear_boton(self,texto,x,y):
        rect = pygame.Rect((x,y),((C.CUADRO*6)-6,C.CUADRO-6))
        fnd_sel = pygame.Surface(((C.CUADRO*6),C.CUADRO))
        fnd_sel.fill(self.bg_cnvs)
        fnd_uns = fnd_sel.copy()
        
        font_se = pygame.font.SysFont('verdana', 17, bold = True)
        font_un = pygame.font.SysFont('verdana', 16)
        
        btn_sel = render_textrect(texto,font_se,rect,self.fg_color,self.bg_color,1)
        btn_uns = render_textrect(texto,font_un,rect,self.fg_color,self.bg_color,1)
        
        fnd_uns.blit(btn_uns,(3,3))
        fnd_sel.blit(btn_sel,(3,3))
        
        return _boton_(texto,fnd_sel,fnd_uns,*rect.topleft)
    
    def DeselectAll(self):
        for boton in self.botones:
            boton.serDeselegido()
    
    def selectOne(self,x,y):
        
        mod = x*2+y
        self.cur_pos += mod
        if self.cur_pos < 0:
            self.cur_pos = 0
        elif self.cur_pos > len(self.botones)-1:
            self.cur_pos = len(self.botones)-1
                
        self.DeselectAll()
        selected = self.botones.get_sprite(self.cur_pos)
        selected.serElegido()
        self.botones.draw(self.canvas)
    
class _boton_ (_giftSprite):
    nombre = ''
    img_sel = None
    img_uns = None
    isSelected = False
    
    def __init__(self,nombre,sel,uns,x,y):
        self.nombre = nombre
        self.img_sel = sel
        self.img_uns = uns
        super().__init__(self.img_uns)
        self.rect = self.img_sel.get_rect(topleft=(x,y))
        
    def serElegido(self):
        self.image = self.img_sel
        self.isSelected = True
    
    def serDeselegido(self):
        self.image = self.img_uns
        self.isSelected = False
    
