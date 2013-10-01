from .Ventana import Ventana
from ._boton import _boton
from ._item_inv import _item_inv
from pygame import sprite, font, Rect, Surface, draw
from libs.textrect import render_textrect
from globs import Constants as C, World as W

class Menu (Ventana):
    botones = []
    cur_btn = 0
    current = ''
    canvas = None
    _onVSel = {}
    
    def __init__(self,titulo,botones):
        self.botones = sprite.LayeredDirty()
        self.botones.empty()
        self.canvas = self.crear_canvas(C.ANCHO-20,C.ALTO-20)
        self.crear_titulo(titulo,self.font_high_color,self.bg_cnvs,C.ANCHO-20)
        self.establecer_botones(botones)
        self._onVSel = {
            "arriba":False,
            "abajo":False,
            "izquierda":False,
            "derecha":False}
        super().__init__(self.canvas)
        self.ubicar(10,10)
        self.dirty = 1
    
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
        
        for i in range(round(((C.CUADRO*6)+6)/3)):
            #linea punteada horizontal superior
            draw.line(cnvs_sel,self.font_high_color,(i*7,0),((i*7)+5,0),2)
            
            #linea punteada horizontal inferior
            draw.line(cnvs_sel,self.font_high_color,(i*7,C.CUADRO+4),((i*7)+5,C.CUADRO+4),2)
        
        for i in range(round((C.CUADRO+6)/3)):
            #linea punteada vertical derecha
            draw.line(cnvs_sel,self.font_high_color,(0,i*7),(0,(i*7)+5),2)
            
            #linea punteada vertical izquierda
            draw.line(cnvs_sel,self.font_high_color,((C.CUADRO*6)+4,i*7),((C.CUADRO*6)+4,(i*7)+5),2)
        
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
        if self.botones != []:
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
                    self.cur_opt = self.filas.get_sprite(i)
                    self.current = spr#.nombre
                    break
            W.onVSel = True
    
    def _onVSel_(self,direccion):
        return self._onVSel[direccion]
    
    def update (self):
        self.dirty = 1
        if not W.onVSel:
            draw.line(self.image,self.bg_cnvs,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))