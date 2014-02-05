from .Ventana import Ventana
from UI.widgets import _opcion
from pygame import font, sprite, Rect, draw
from globs import Constants as C, World as W
from libs.textrect import render_textrect

class Dialog (Ventana):
    posicion = 0,384
    filas = sprite.LayeredDirty()
    
    def __init__(self, texto,onSelect):
        self.canvas = self.crear_canvas(int(C.ANCHO), int(C.ALTO/5))
        self.altura_del_texto = self.fuente_M.get_height()+1
        self.draw_space = Rect((3,3), (self.canvas.get_width()-7, int(self.canvas.get_height())-7))
        
        self.setText(texto,onSelect)
        
        super().__init__(self.canvas)
        self.ubicar(*self.posicion)
        self.dirty = 1

    def setText(self,texto,onSelect=False):
        h = self.altura_del_texto
        if onSelect:
            self.opciones = len(texto)
            for i in range(len(texto)):
                opcion = _opcion(texto[i],self.draw_space.w,(3,i*h+i+2))
                self.filas.add(opcion)
            
            self.filas.draw(self.canvas)
            self.elegir_opcion(-1)
        else:
            render = render_textrect(texto,self.fuente_M,self.draw_space,self.font_none_color,self.bg_cnvs)
            self.canvas.blit(render,self.draw_space)
            
        self.image = self.canvas
    
    def elegir_opcion (self,i):
        self.sel = self.dibujar_lineas_cursor(i,self.canvas,self.draw_space.w,self.sel,self.opciones)
    
    def confirmar_seleccion(self):
        pass
    
    
    def update (self):
        self.dirty = 1