from .Ventana import Ventana
from pygame import sprite
from globs import Constants as C, World as W

class DialogFrontEnd (Ventana):
    posicion = 0,C.ALTO-int(C.ALTO/5)
    filas = None
    draw_space_rect = None
    text_pos = 3,3
    active = True
    
    def __init__(self, borde):
        self.filas = sprite.LayeredDirty()
        _size = int(C.ANCHO), int(C.ALTO/5)
        if borde == 'RAISED': 
            self.canvas = self.crear_canvas(*_size)
        elif borde == 'SUNKEN':
            self.canvas = self.crear_inverted_canvas(*_size)
        
        Ventana.__init__(self,self.canvas)
        #viniendo de Inventario rápido, el super() es Menu_items
        self.altura_del_texto = self.fuente_M.get_height()+1
        self.ubicar(*self.posicion)
        W.RENDERER.setOverlay(self,C.CAPA_OVERLAYS_DIALOGOS)
        
    def destruir(self):
        W.RENDERER.delOverlay(self)
        W.DIALOG = None
        W.MODO = 'Aventura'
        
    def ubicar(self,x,y):
        if x < 0 or y < 0:
            raise ValueError('Coordenadas inválidas')
        self.rect.move_ip(x,y)
    
    def usar_funcion(self,tecla):
        if tecla in self.funciones:
            self.funciones[tecla]()