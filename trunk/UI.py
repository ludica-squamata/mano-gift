import pygame
from libs.textrect import render_textrect
from globs import Constants as C, World as W
from base import _giftSprite
from misc import Resources as r

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
    current = ''
    
    def __init__(self,titulo,botones):
        self.botones.empty()
        
        self.canvas = pygame.Surface((int(C.ANCHO)-20, int(C.ALTO)-20))
        self.crear_titulo(titulo)
        self.establecer_botones(botones)
        super().__init__(self.canvas)
        self.ubicar(10,10)
        self.dirty = 2
        
    def crear_titulo(self,titulo):
        clip = pygame.Rect(3,3,int(C.ANCHO)-27, int(C.ALTO)-27)
        self.canvas.fill(self.bg_cnvs)
        self.canvas.fill(self.bg_color,rect=clip)
        
        ttl_fuente = pygame.font.SysFont('verdana', 16)
        ttl_fuente.set_underline(True)
        ttl_rect = pygame.Rect((3,3),(int(C.ANCHO)-27,30))
        ttl_txt =  render_textrect(titulo,ttl_fuente,ttl_rect,self.fg_color,self.bg_color,1)
        self.canvas.blit(ttl_txt,ttl_rect.topleft)
        
    def establecer_botones(self,botones):
        for btn in botones:
            nombre = btn['boton']
            pos = btn['pos']
            boton = self._crear_boton(nombre,*pos)
            for direccion in ['arriba','abajo','izquierda','derecha']:
                if direccion in btn:
                    boton.direcciones[direccion] = btn[direccion]
            
            self.botones.add(boton)
        
        if len(self.botones) > 0:
            self.cur_pos = 0
            selected = self.botones.get_sprite(self.cur_pos)
            selected.serElegido()
            self.current = selected.nombre
            
            
        self.botones.draw(self.canvas)
        
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
        
        return _boton(texto,fnd_sel,fnd_uns,rect.topleft)
    
    def DeselectAll(self):
        for boton in self.botones:
            boton.serDeselegido()
            boton.dirty = 2
        self.botones.draw(self.canvas)
    
    def selectOne(self,direccion):
        self.DeselectAll()
        self.current = self.botones.get_sprite(self.cur_pos)
        if direccion in self.current.direcciones:
            selected = self.current.direcciones[direccion]
        else:
            selected = self.current.nombre
        
        for i in range(len(self.botones)):
            boton = self.botones.get_sprite(i)
            if boton.nombre == selected:
                boton.serElegido()
                self.current = boton.nombre
                self.cur_pos = i
                break
                    
        self.botones.draw(self.canvas)
        return self.cur_pos
    
class _boton (_giftSprite):
    nombre = ''
    img_sel = None
    img_uns = None
    isSelected = False
    pos = 0,0
    direcciones = {}
    
    def __init__(self,nombre,sel,uns,pos):
        self.direcciones = {}
        self.nombre = nombre
        self.img_sel = sel
        self.img_uns = uns
        self.pos = pos
        super().__init__(self.img_uns)
        self.rect = self.img_sel.get_rect(topleft=self.pos)
        self.dirty = 2
        
    def serElegido(self):
        self.image = self.img_sel
        self.isSelected = True
        self.rect = self.img_sel.get_rect(topleft=self.pos)
    
    def serDeselegido(self):
        self.image = self.img_uns
        self.isSelected = False
        self.rect = self.img_sel.get_rect(topleft=self.pos)
    
    def __repr__(self):
        return self.nombre+' _boton DirtySprite'
    
    
    
