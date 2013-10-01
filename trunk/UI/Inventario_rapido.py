from .Menu_Inventario import Menu_Inventario
from .Ventana import Ventana
from globs import World as W, Constants as C
from pygame import Rect, font


class Inventario_rapido (Menu_Inventario,Ventana):
    posicion = 0,384
    canvas = ''
    sel = 0
    
    def __init__(self):
        self.canvas = self.crear_inverted_canvas(int(C.ANCHO), int(C.ALTO/5))
        self.draw_space_rect = Rect (3,3,int(C.ANCHO)-7,int(C.ALTO/5)-7)
        self.fuente = font.SysFont('verdana', 16)
        self.altura_del_texto = self.fuente.get_height()+1
        self.crear_contenido(self.draw_space_rect)
        Ventana.__init__(self,self.canvas)
        W.MAPA_ACTUAL.dialogs.add(self,layer=C.CAPA_OVERLAYS_DIALOGOS)
        self.rect = Rect((self.posicion, (C.ANCHO, int(C.ALTO/5))))
        self.dirty = 1
        W.onDialog = True
    
    def confirmar_seleccion (self):
        cant = W.HERO.usar_item(self.current.item)        
        if cant <= 0:
            self.opciones -= 1
            if self.opciones <= 0:
                W.MAPA_ACTUAL.endDialog()
        
    def update (self):
        self.crear_contenido(self.draw_space_rect)
        self.dirty = 1