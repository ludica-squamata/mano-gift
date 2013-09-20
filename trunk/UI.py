from pygame import draw, sprite, font, Surface, Rect
from libs.textrect import render_textrect
from globs import Constants as C, World as W
from base import _giftSprite
from misc import Resources as r

class Ventana (_giftSprite):
    canvas = None
    button_bg_color = 100,100,100
    font_high_color = 255,255,255
    font_none_color = 0,0,0
    bg_cnvs = 125,125,125
    bg_bisel_bg = 175,175,175
    bg_bisel_fg = 100,100,100
    posicion = x,y = 0,0
    tamanio = ancho,alto = 0,0
    sel = 1
    opciones = 0
    
    def __init__(self,image):
        super().__init__(image)

    def crear_canvas(self,ancho,alto):
        canvas = Surface((ancho,alto))
        
        clip = Rect(0,0,ancho, alto)
        canvas.fill(self.bg_bisel_bg,rect=clip)
        
        clip = Rect(3,3,ancho, alto)
        canvas.fill(self.bg_bisel_fg,rect=clip)
        
        clip = Rect(3,3,ancho-7, alto-7)
        canvas.fill(self.bg_cnvs,rect=clip)
        
        return canvas
    
    def crear_inverted_canvas (self,ancho,alto):
        canvas = Surface((ancho, alto))
        
        clip = Rect(0,0,ancho, alto)
        canvas.fill(self.bg_bisel_fg,rect=clip)
        
        clip = Rect(3,3,ancho, alto)
        canvas.fill(self.bg_bisel_bg,rect=clip)
        
        clip = Rect(3,3,ancho-7, alto-7)
        canvas.fill(self.bg_cnvs,rect=clip)
        
        return canvas
        
    def elegir_opcion(self,i):
        self.sel += i
        if self.sel < 1: self.sel = 1
        elif self.sel > self.opciones: self.sel = self.opciones
        draw.line(self.image,self.font_high_color,(3,self.sel*22),(C.ANCHO-5,self.sel*22))
        draw.line(self.image,self.bg_cnvs,(3,(self.sel-i)*22),(C.ANCHO-5,(self.sel-i)*22))

        return self.sel
    
class Dialog (Ventana):
    fuente = None
    posicion = x,y = 0,384
    
    def __init__(self, texto):
        self.canvas = self.crear_canvas(int(C.ANCHO), int(C.ALTO/5))
        
        self.fuente = font.SysFont('verdana', 16)
        rect = Rect((self.posicion, (C.ANCHO-7, int(C.ALTO/5)-7)))
        image = render_textrect(texto,self.fuente,rect,self.font_none_color,self.bg_cnvs)
        
        self.canvas.blit(image,(3,3))
        super().__init__(self.canvas)
        self.ubicar(*rect.topleft)
        self.dirty = 2

    def setText(self, texto):
        rect = Rect((3, 3, C.ANCHO-7, int(C.ALTO/5)-7))
        render = render_textrect(texto,self.fuente,rect,self.font_none_color,self.bg_cnvs)
        self.canvas.blit(render,rect)
        if W.onSelect:
            self.opciones = len(texto.split('\n'))
            draw.line(self.canvas,self.font_high_color,(3,self.sel*22),(C.ANCHO-7,self.sel*22))    
        self.image = self.canvas
        
class Menu (Ventana):
    botones = None
    cur_btn = 0
    current = ''
    canvas = None
    
    def __init__(self,titulo,botones):
        self.botones = sprite.LayeredDirty()
        self.botones.empty()
        self.canvas = self.crear_canvas(C.ANCHO-20,C.ALTO-20)
        self.crear_titulo(titulo,self.font_high_color,self.bg_cnvs,C.ANCHO-20)
        self.establecer_botones(botones)
        super().__init__(self.canvas)
        self.ubicar(10,10)
        self.dirty = 2    
    
    def crear_titulo(self,titulo,fg_color,bg_color,ancho):
        ttl_fuente = font.SysFont('verdana', 16)
        ttl_fuente.set_underline(True)
        ttl_rect = Rect((3,3),(ancho-7,30))
        ttl_txt =  render_textrect(titulo,ttl_fuente,ttl_rect,fg_color,bg_color,1)
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
            self.current = selected
            
            
        self.botones.draw(self.canvas)
        
    def _crear_boton(self,texto,x,y):
        rect = Rect((x,y),((C.CUADRO*6)-6,C.CUADRO-6))
        
        cnvs_pre = Surface(((C.CUADRO*6)+6,C.CUADRO+6))
        cnvs_pre.fill(self.bg_cnvs)
        cnvs_sel = cnvs_pre.copy()
        cnvs_uns = cnvs_pre.copy()
        
        fnd_pre = self.crear_inverted_canvas((C.CUADRO*6),C.CUADRO)
        fnd_uns = self.crear_canvas((C.CUADRO*6),C.CUADRO)
        
        blanco = 255,255,255
        for i in range(round(((C.CUADRO*6)+6)/3)):
            #linea punteada horizontal superior
            draw.line(cnvs_sel,blanco,(i*7,0),((i*7)+5,0),2)
            
            #linea punteada horizontal inferior
            draw.line(cnvs_sel,blanco,(i*7,C.CUADRO+4),((i*7)+5,C.CUADRO+4),2)
        
        for i in range(round((C.CUADRO+6)/3)):
            #linea punteada vertical derecha
            draw.line(cnvs_sel,blanco,(0,i*7),(0,(i*7)+5),2)
            
            #linea punteada vertical izquierda
            draw.line(cnvs_sel,blanco,((C.CUADRO*6)+4,i*7),((C.CUADRO*6)+4,(i*7)+5),2)
        
        cnvs_sel.blit(fnd_uns,(3,3))
        cnvs_uns.blit(fnd_uns,(3,3))
        cnvs_pre.blit(fnd_pre,(3,3))
        
        font_se = font.SysFont('verdana', 16, bold = True)
        font_un = font.SysFont('verdana', 16)
        
        btn_sel = render_textrect(texto,font_se,rect,self.font_high_color,self.bg_cnvs,1)
        btn_uns = render_textrect(texto,font_un,rect,self.font_none_color,self.bg_cnvs,1)        
        
        cnvs_uns.blit(btn_uns,(6,6))
        cnvs_sel.blit(btn_sel,(6,6))
        cnvs_pre.blit(btn_sel,(6,6))
        
        return _boton(texto,cnvs_sel,cnvs_pre,cnvs_uns,rect.topleft)
    
    def DeselectAllButtons(self):
        for boton in self.botones:
            boton.serDeselegido()
            boton.dirty = 2
        self.botones.draw(self.canvas)
    
    def selectOne(self,direccion):
        self.DeselectAllButtons()
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
    
    def PressOne(self):
        self.current.serPresionado()
        self.botones.draw(self.canvas)
        
    def mover_cursor(self,item):
        if type(item) == _boton:
            for i in range(len(self.botones)):
                spr = self.botones.get_sprite(i)
                if  spr.nombre == item.nombre:
                    self.cur_btn = i
                    self.current = spr
                    break
            W.onVSel = False
                    
        elif type(item) == _item_inv:
            for i in range(len(self.filas)):
                spr = self.filas.get_sprite(i)
                if item.nombre == spr.nombre:
                    self.cur_opt = i
                    self.current = spr#.nombre
                    break
            W.onVSel = True
    
    def update (self):
        if not W.onVSel:
            draw.line(self.image,self.bg_cnvs,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))
            
class Menu_Inventario (Menu):
    cur_opt = 0
    filas = sprite.LayeredDirty()
    descripcion_area = None
    fuente = ''
    
    def __init__(self,botones):
        self.fuente = font.SysFont('verdana', 16)
        super().__init__('Inventario',botones)
        self.crear_contenido()
        self.dirty = 2
        self.sel = 3

    def crear_contenido(self):
        self.filas.empty()
        erase = Surface((self.canvas.get_width()-19,270))
        erase.fill(self.bg_cnvs)
        self.canvas.blit(erase,(10,44))
        self.crear_espacio_descriptivo()
        count = 22
        for item in W.HERO.inventario:
            count += 22
            fila = _item_inv(item,(11,count))
            
            self.filas.add(fila)
        
        if len(self.filas) > 0:            
            self.opciones = len(self.filas)
            self.elegir_fila(0)
            W.onVSel = True
            self.filas.draw(self.canvas)
            draw.line(self.canvas,self.font_high_color,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))
    
    def crear_espacio_descriptivo(self):
        marco = self.crear_inverted_canvas((self.canvas.get_width()-15),53)
        megacanvas = Surface((marco.get_width(),marco.get_height()+17))
        megacanvas.fill(self.bg_cnvs)
        
        fuente = font.SysFont('verdana', 14)
        texto = fuente.render('Efecto',True,self.font_none_color,self.bg_cnvs)
        
        megacanvas.blit(marco,(0,17))
        megacanvas.blit(texto,(3,7))
        
        self.canvas.blit(megacanvas,(7,340))
        self.descripcion_area = marco.get_rect()
        
    def elegir_fila(self,j):
        if self.opciones > 0:
            self.DeselectAllButtons()
            W.onVSel = True
            self.sel += j
            if self.sel < 3: self.sel = 3
            elif self.sel > self.opciones+2: self.sel = self.opciones+2
            
            draw.line(self.image,self.font_high_color,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))
            draw.line(self.image,self.bg_cnvs,(10,(self.sel-j)*22),(self.canvas.get_width()-10,(self.sel-j)*22))
            
            self.mover_cursor(self.filas.get_sprite(self.sel-3))
            
            render_area = Rect((-1,-1),(self.descripcion_area.w-12,self.descripcion_area.h-12))
            desc = render_textrect(self.current.item.efecto_des,
                                   self.fuente,render_area,
                                   self.font_high_color,self.bg_cnvs)
            self.canvas.blit(desc,(12,363))
            
    def confirmar_seleccion (self):
        cant = W.HERO.usar_item(self.current.item)
        altura = self.current.image.get_height()
        self.current.reducir_cant()
        if cant <= 0:
            self.opciones -= 1
            if self.opciones <= 0:
                self.mover_cursor(self.botones.get_sprite(0))
                W.onVSel = False
                draw.line(self.image,self.bg_cnvs,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))
        self.crear_contenido()
   
class _boton (_giftSprite):
    nombre = ''
    img_uns = None
    img_sel = None
    isSelected = False
    pos = 0,0
    direcciones = {}
    
    def __init__(self,nombre,sel,pre,uns,pos):
        self.direcciones = {}
        self.nombre = nombre
        self.img_sel = sel
        self.img_pre = pre
        self.img_uns = uns
        self.pos = pos
        super().__init__(self.img_uns)
        self.rect = self.img_sel.get_rect(topleft=self.pos)
        self.dirty = 2
    
    def serPresionado (self):
        self.image = self.img_pre
        self.isSelected = True
        self.rect = self.img_pre.get_rect(topleft=self.pos)
    
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
    item_ID = 0
    image = None
    pos = 0,0
    fuente = ''
    rect = ''
    bg_color = 125,125,125
    fg_color = 255,255,255
    
    def __init__(self,item,pos):
        self.item = item
        self.fuente = font.SysFont('verdana', 16)
        self.rect = Rect(pos,((C.CUADRO*6)-6,22))
        
        nombre = self.item.nombre.capitalize()
        cant = self.item.cantidad
        
        self.img_nmbr = render_textrect(nombre,self.fuente,self.rect,self.fg_color,self.bg_color,1)
        self.img_cant = render_textrect('x'+str(cant),self.fuente,self.rect,self.fg_color,self.bg_color,1)
        self.nombre = nombre
        self.cant = cant
        self.construir_fila()
        self.pos = pos
        super().__init__(self.image)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.dirty = 2
    
    def reducir_cant(self):
        self.cant -= 1
        if self.cant > 0:
            self.img_cant = render_textrect('x'+str(self.cant),self.fuente,self.rect,self.fg_color,self.bg_color,1)
            self.construir_fila()
        else:
            self.kill()
        
    def construir_fila(self):
        image = Surface((int(C.ANCHO)-44,self.rect.h))
        image.fill(self.bg_color)
        image.blit(self.img_nmbr,(7,0))
        image.blit(self.img_cant,(260,0))
        
        self.image = image
        self.rect = self.image.get_rect(topleft=self.pos)
    
    def __repr__(self):
        return self.nombre+' _item_inv DirtySprite'
    
