from .Ventana import Ventana
from ._opcion import _opcion
from pygame import font, sprite, Rect, draw
from globs import Constants as C, World as W
from libs.textrect import render_textrect

class Dialog (Ventana):
    fuente = None
    posicion = 0,384
    filas = sprite.LayeredDirty()
    
    def __init__(self, texto):
        self.canvas = self.crear_canvas(int(C.ANCHO), int(C.ALTO/5))
        self.fuente = font.SysFont('verdana', 16)
        self.altura_del_texto = self.fuente.get_height()+1
        self.draw_space = Rect((3,3), (self.canvas.get_width()-7, int(self.canvas.get_height())-7))
        
        self.setText(texto)
        
        super().__init__(self.canvas)
        self.ubicar(*self.posicion)
        self.dirty = 1

    def setText(self, texto):
        h = self.altura_del_texto
        if W.onSelect:
            ops = texto.split('\n')
            self.opciones = len(ops)
            for i in range(len(ops)):
                opcion = _opcion(ops[i],self.draw_space.w,(3,(i*22)+1+(i-1)+2))
                self.filas.add(opcion)
            
            self.filas.draw(self.canvas)
            draw.line(self.canvas,self.font_high_color,(3,self.sel*h),(C.ANCHO-7,self.sel*h)) 
        else:
            render = render_textrect(texto,self.fuente,self.draw_space,self.font_none_color,self.bg_cnvs)
            self.canvas.blit(render,self.draw_space)
            
        self.image = self.canvas
    
    def update (self):
        self.dirty = 1