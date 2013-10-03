from .Ventana import Ventana
from ._opcion import _opcion
from pygame import font, sprite, Rect, draw
from globs import Constants as C, World as W
from libs.textrect import render_textrect

class Dialog (Ventana):
    fuente = None
    posicion = 0,384
    filas = sprite.LayeredDirty()
    
    def __init__(self, texto,onSelect):
        self.canvas = self.crear_canvas(int(C.ANCHO), int(C.ALTO/5))
        self.fuente = font.SysFont('verdana', 16)
        self.altura_del_texto = self.fuente.get_height()+1
        self.draw_space = Rect((3,3), (self.canvas.get_width()-7, int(self.canvas.get_height())-7))
        
        self.setText(texto,onSelect)
        
        super().__init__(self.canvas)
        self.ubicar(*self.posicion)
        self.dirty = 1

    def setText(self, texto,onSelect=False):
        h = self.altura_del_texto
        if onSelect:
            ops = texto.split('\n')
            self.opciones = len(ops)
            for i in range(len(ops)):
                opcion = _opcion(ops[i],self.draw_space.w,(3,(i*22)+1+(i-1)+2))
                self.filas.add(opcion)
            
            self.filas.draw(self.canvas)
            draw.line(self.canvas,self.font_high_color,(3,(self.sel*h)+1+(self.sel-2)),(C.ANCHO-7,(self.sel*h)+1+(self.sel-2)))
        else:
            render = render_textrect(texto,self.fuente,self.draw_space,self.font_none_color,self.bg_cnvs)
            self.canvas.blit(render,self.draw_space)
            
        self.image = self.canvas
    
    def elegir_opcion (self,i):
        self.sel = self.dibujar_lineas_cursor(i,self.canvas,self.draw_space.w,self.sel,self.opciones)
    
    def update (self):
        self.dirty = 1