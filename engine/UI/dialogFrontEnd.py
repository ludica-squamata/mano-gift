from pygame.sprite import LayeredUpdates
from engine.globs import Constants as Cs, EngineData as Ed
from .Ventana import Ventana


class DialogFrontEnd (Ventana):
    posicion = 0, Cs.ALTO-int(Cs.ALTO/5)
    filas = None
    draw_space_rect = None
    text_pos = 3, 3
    active = True
    
    def __init__(self, borde):
        self.filas = LayeredUpdates()
        _size = int(Cs.ANCHO), int(Cs.ALTO/5)
        if borde == 'RAISED': 
            self.canvas = self.crear_canvas(*_size)
        elif borde == 'SUNKEN':
            self.canvas = self.crear_inverted_canvas(*_size)
        
        super().__init__(self.canvas)
        self.fuente = self.fuente_M
        self.altura_del_texto = self.fuente.get_height()
        self.ubicar(*self.posicion)
        Ed.RENDERER.add_overlay(self, Cs.CAPA_OVERLAYS_DIALOGOS)
        
    def destruir(self):
        Ed.DIALOG = None
        Ed.RENDERER.del_overlay(self)
        
    def ubicar(self, x=0, y=0, z=0):
        if x < 0 or y < 0:
            raise ValueError('Coordenadas inválidas')
        self.rect.move_ip(x, y)
