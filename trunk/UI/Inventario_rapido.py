from .menues.Menu_Items import Menu_Items
from .Ventana import Ventana
from globs import World as W, Constants as C
from pygame import Rect, font


class Inventario_rapido (Menu_Items,Ventana):
    posicion = 0,C.ALTO-int(C.ALTO/5)
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
        self.funciones = {
            'hablar':self.confirmar_seleccion
        }
    
    def confirmar_seleccion (self):
        if self.opciones > 0:
            cant = W.HERO.usar_item(self.current.item)        
            if cant <= 0:
                self.opciones -= 1
                if self.opciones <= 0:
                    W.MAPA_ACTUAL.endDialog()
    
    def elegir_opcion (self,i):
        self.sel = self.dibujar_lineas_cursor(i,self.canvas,self.draw_space.get_width(),self.sel,self.opciones)
        
    def update (self):
        self.crear_contenido(self.draw_space_rect)
        self.dirty = 1