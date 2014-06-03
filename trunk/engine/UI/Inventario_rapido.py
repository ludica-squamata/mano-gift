from .menues.menu_Items import Menu_Items
from .dialogFrontEnd import DialogFrontEnd
from engine.globs import World as W, Constants as C
from pygame import Rect

class Inventario_rapido (DialogFrontEnd,Menu_Items):
    sel = 0
    
    def __init__(self):
        
        self.draw_space_rect = Rect (3,3,int(C.ANCHO)-7,int(C.ALTO/5)-7)
        self.funciones = {
            'hablar':self.confirmar_seleccion,
            'cerrar':self.destruir,
            'arriba':self.elegir_opcion,
            'abajo':self.elegir_opcion
        }
        
        #for i in Inventario_rapido.__mro__:
        #    print(i)
        
        super().__init__('SUNKEN')
    
    def confirmar_seleccion (self):
        if self.opciones > 0:
            if W.HERO.usar_item(self.current.item) <= 0:
                self.opciones -= 1
                if self.opciones <= 0:
                    self.destruir()
    
    def elegir_opcion (self,i):
        self.sel = self.posicionar_cursor(i,self.sel,self.opciones)
        
    def update (self): 
        self.crear_contenido(self.draw_space_rect)
        self.canvas.blit(self.draw_space,self.draw_space_rect.topleft)
        self.dirty = 1