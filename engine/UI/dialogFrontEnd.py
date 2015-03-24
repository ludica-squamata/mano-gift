from pygame.sprite import LayeredDirty
from engine.globs import Constants as C, EngineData as ED
from .Ventana import Ventana

class DialogFrontEnd (Ventana):
    posicion = 0,C.ALTO-int(C.ALTO/5)
    filas = None
    draw_space_rect = None
    text_pos = 3,3
    active = True
    
    def __init__(self, borde):
        self.filas = LayeredDirty()
        _size = int(C.ANCHO), int(C.ALTO/5)
        if borde == 'RAISED': 
            self.canvas = self.crear_canvas(*_size)
        elif borde == 'SUNKEN':
            self.canvas = self.crear_inverted_canvas(*_size)
        
        Ventana.__init__(self,self.canvas)
        #viniendo de Inventario rápido, el super() es Menu_items
        self.altura_del_texto = self.fuente_M.get_height()+1
        self.ubicar(*self.posicion)
        ED.RENDERER.addOverlay(self,C.CAPA_OVERLAYS_DIALOGOS)
        
    def destruir(self):
        ED.DIALOG = None
        ED.RENDERER.delOverlay(self)
        
    def ubicar(self,x,y):
        if x < 0 or y < 0:
            raise ValueError('Coordenadas inválidas')
        self.rect.move_ip(x,y)
    
    def usar_funcion(self,tecla):
        if tecla in self.funciones:
            if tecla == 'arriba':
                self.funciones[tecla](-1)
            elif tecla == 'abajo':
                self.funciones[tecla](+1)
            elif tecla in ['izquierda','derecha']:
                self.funciones[tecla](tecla)
            else:
                self.funciones[tecla]()