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
    sel = 1
    def __init__(self,image):
        super().__init__(image)
    
    def elegir_opcion(self,j,m):
        blanco = 255,255,255
        negro = 0,0,0
        self.sel += j
        if self.sel < 1: self.sel = 1
        elif self.sel > 2: self.sel = 2
        pygame.draw.line(self.image,blanco,(3,self.sel*22),(C.ANCHO-5,self.sel*22))
        pygame.draw.line(self.image,blanco,(3,(self.sel+m)*22),(C.ANCHO-5,(self.sel+m)*22))

        return self.sel
    
class Dialog (Ventana):
    fuente = None
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
    opciones = pygame.sprite.LayeredDirty()
    cur_opt = 0
    cur_btn = 0
    current = ''
    
    def __init__(self,titulo,contenido):
        self.botones.empty()
        self.opciones.empty()
        
        self.canvas = pygame.Surface((int(C.ANCHO)-20, int(C.ALTO)-20))
        self.crear_titulo(titulo)
        self.establecer_botones(contenido['botones'])
        self.crear_contenido(contenido['contenido'])
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
            self.cur_btn = 0
            selected = self.botones.get_sprite(self.cur_btn)
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
    
    def DeselectAllButtons(self):
        for boton in self.botones:
            boton.serDeselegido()
            boton.dirty = 2
        self.botones.draw(self.canvas)
    
    def selectOne(self,direccion):
        self.DeselectAllButtons()
        pygame.draw.line(self.image,self.bg_color,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))
        self.current = self.botones.get_sprite(self.cur_btn)
        if direccion in self.current.direcciones:
            selected = self.current.direcciones[direccion]
        else:
            selected = self.current.nombre

        for i in range(len(self.botones)):
            boton = self.botones.get_sprite(i)
            if boton.nombre == selected:
                boton.serElegido()
                self.mover_cursor(boton)
                break
                    
        self.botones.draw(self.canvas)
    
    def crear_contenido(self,contenido):
        if contenido == 'Inventario':
            self.sel += 2
            W.onVSel = True
            count = 22
            for key in W.HERO.inventario:
                count += 22
                fila = self._crear_filas_items(key.capitalize(),str(W.HERO.inventario[key]),(11,count))
                
                self.opciones.add(fila)
            
            if len(self.opciones) > 0:
                self.current = self.opciones.get_sprite(self.cur_opt).nombre
                self.DeselectAllButtons()
                self.opciones.draw(self.canvas)
                pygame.draw.line(self.canvas,self.fg_color,(10,66),(self.canvas.get_width()-10,66))
    
    def _crear_filas_items(self,nombre,cant,pos):
        fuente = pygame.font.SysFont('verdana', 16)
        rect = pygame.Rect(pos,((C.CUADRO*6)-6,22))
        
        txt_nmbr = render_textrect(nombre,fuente,rect,self.fg_color,self.bg_color,1)
        txt_cant = render_textrect('x'+cant,fuente,rect,self.fg_color,self.bg_color,1)

        canvas = pygame.Surface((self.canvas.get_width()-24,rect.h))
        canvas.blit(txt_nmbr,(7,0))
        canvas.blit(txt_cant,(260,0))
        
        return _item_inv(nombre,canvas,rect.topleft)
    
    def elegir_opcion(self,j):
        if len(self.opciones) > 0:
            self.DeselectAllButtons()
            W.onVSel = True
            m = -j
            self.sel += j
            if self.sel < 3: self.sel = 3
            elif self.sel > len(self.opciones)+2: self.sel = len(self.opciones)+2
            
            pygame.draw.line(self.image,self.fg_color,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))
            pygame.draw.line(self.image,self.bg_color,(10,(self.sel+m)*22),(self.canvas.get_width()-10,(self.sel+m)*22))
            
            return self.mover_cursor(self.opciones.get_sprite(self.sel-3))
    
    def mover_cursor(self,item):
        if type(item) == _boton:
            for i in range(len(self.botones)):
                spr = self.botones.get_sprite(i)
                if  spr.nombre == item.nombre:
                    self.cur_btn = i
                    self.current = spr.nombre
                    break
            W.onVSel = False
                    
        elif type(item) == _item_inv:
            for i in range(len(self.opciones)):
                spr = self.opciones.get_sprite(i)
                if item.nombre == spr.nombre:
                    self.cur_opt = i
                    self.current = spr.nombre
                    break
            W.onVSel = True
        
        return spr.nombre
    
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

class _item_inv (_giftSprite):
    nombre = ''
    image = None
    isSelected = False
    pos = 0,0
    
    def __init__(self,nombre,canvas,pos):
        self.nombre = nombre
        self.image = canvas
        self.pos = pos
        super().__init__(self.image)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.dirty = 2
    
    def __repr__(self):
        return self.nombre+' _item_inv DirtySprite'
    
