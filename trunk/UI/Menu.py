from .Ventana import Ventana
from ._boton import _boton
from ._item_inv import _item_inv
from pygame import sprite, font, Rect, Surface, draw
from libs.textrect import render_textrect
from globs import Constants as C, World as W
from .modos import modo

class Menu (Ventana):
    botones = []
    cur_btn = 0
    current = ''
    canvas = None
    newMenu = False
    
    def __init__(self,titulo,botones):
        self.nombre = titulo
        self.current = self
        self.canvas = self.crear_canvas(C.ANCHO-20,C.ALTO-20)
        if len(botones) != 0:
            self.botones = sprite.LayeredDirty()
            self.botones.empty()
            self.establecer_botones(botones,6)
        self.crear_titulo(titulo,self.font_high_color,self.bg_cnvs,C.ANCHO-20)
        self.funciones = {
            "arriba":self.selectOne,
            "abajo":self.selectOne,
            "izquierda":self.selectOne,
            "derecha":self.selectOne,
            "hablar":self.PressOne}
        super().__init__(self.canvas)
        self.ubicar(10,10)
        self.dirty = 1
        
    def establecer_botones(self,botones,ancho_mod):
        for btn in botones:
            nombre = btn['boton']
            pos = btn['pos']
            boton = self._crear_boton(nombre,ancho_mod,*pos)
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
        
    def _crear_boton(self,texto,ancho_mod,x,y):
        ancho = C.CUADRO*ancho_mod
        
        rect = Rect((x,y),((ancho)-6,C.CUADRO-6))
        
        cnvs_pre = Surface(((ancho)+6,C.CUADRO+6))
        cnvs_pre.fill(self.bg_cnvs)
        cnvs_sel = cnvs_pre.copy()
        cnvs_uns = cnvs_pre.copy()
        
        fnd_pre = self.crear_inverted_canvas(ancho,C.CUADRO)
        fnd_uns = self.crear_canvas((ancho),C.CUADRO)
        
        for i in range(round(((C.CUADRO*ancho)+6)/3)):
            #linea punteada horizontal superior
            draw.line(cnvs_sel,self.font_high_color,(i*7,0),((i*7)+5,0),2)
            
            #linea punteada horizontal inferior
            draw.line(cnvs_sel,self.font_high_color,(i*7,C.CUADRO+4),((i*7)+5,C.CUADRO+4),2)
        
        for i in range(round((C.CUADRO+6)/3)):
            #linea punteada vertical derecha
            draw.line(cnvs_sel,self.font_high_color,(0,i*7),(0,(i*7)+5),2)
            
            #linea punteada vertical izquierda
            draw.line(cnvs_sel,self.font_high_color,(ancho+4,i*7),(ancho+4,(i*7)+5),2)
        
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
    
    def DeselectAll(self,lista):
        if len(lista) > 0:
            for item in lista:
                item.serDeselegido()
                item.dirty = 1
            lista.draw(self.canvas)
    
    def selectOne(self,direccion):
        self.DeselectAll(self.botones)
        if len(self.botones) > 0:
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
        if len(self.botones) > 0:
            self.current.serPresionado()
            self.botones.draw(self.canvas)
        
        self.newMenu = True
        
    def mover_cursor(self,item):
        if type(item) == _boton:
            for i in range(len(self.botones)):
                spr = self.botones.get_sprite(i)
                if  spr.nombre == item.nombre:
                    self.cur_btn = i
                    self.current = spr
                    break
                    
        elif type(item) == _item_inv:
            for i in range(len(self.filas)):
                spr = self.filas.get_sprite(i)
                if item.nombre == spr.nombre:
                    self.cur_opt = self.filas.get_sprite(i)
                    self.current = spr#.nombre
                    break
    
    def usar_funcion(self,tecla):
        if tecla in ('arriba','abajo','izquierda','derecha'):
            self.funciones[tecla](tecla)
        else:
            self.funciones[tecla]()
        
        return self.newMenu
    
    def update (self):
        self.newMenu = False
        self.dirty = 1
        if not modo.onVSel:
            draw.line(self.image,self.bg_cnvs,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))