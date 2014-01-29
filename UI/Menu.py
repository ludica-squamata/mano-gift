from .Ventana import Ventana
from globs import Constants as C, World as W
from ._boton import _boton
from ._item_inv import _item_inv

class Menu (Ventana):
    botones = []
    keyup = {}
    cur_btn = 0
    current = ''
    canvas = None
    newMenu = False
    
    def __init__(self,titulo):
        self.nombre = titulo
        self.current = self
        self.canvas = self.crear_canvas(C.ANCHO-20,C.ALTO-20)
        self.crear_titulo(titulo,self.font_high_color,self.bg_cnvs,C.ANCHO-20)
        self.funciones = {
            "arriba":lambda dummy : None,
            "abajo":lambda dummy : None,
            "izquierda":lambda dummy : None,
            "derecha":lambda dummy : None,
            "hablar":lambda : None}
        super().__init__(self.canvas)
        self.ubicar(10,10)
        self.dirty = 1
        
        W.MENUS[titulo] = self

    def DeselectAll(self,lista):
        if len(lista) > 0:
            for item in lista:
                item.serDeselegido()
                item.dirty = 1
            lista.draw(self.canvas)
            
    def mover_cursor(self,item):
        if type(item) == _boton:
            for i in range(len(self.botones)):
                spr = self.botones.get_sprite(i)
                if  spr.nombre == item.nombre:
                    self.cur_btn = i
                    self.current = spr
                    break
                    
        elif type(item) == _item_inv:
            for i in range(len(self.filas)):
                spr = self.filas.get_sprite(i)
                if item.nombre == spr.nombre:
                    self.cur_opt = self.filas.get_sprite(i)
                    self.current = spr#.nombre
                    break
    
    def cancelar(self):
        '''Esta funcion es un hook para otras funciones del mismo nombre.'''
        return True
    
    def usar_funcion(self,tecla):
        if tecla in ('arriba','abajo','izquierda','derecha'):
            self.funciones[tecla](tecla)
        else:
            self.funciones[tecla]()
    
    def keyup_function(self,tecla):
        if tecla in self.keyup:
            self.keyup[tecla]()
    
    def update (self):
        self.dirty = 1
    
    def PressButton(self):
        if len(self.botones) > 0:
            self.current.serPresionado()
            self.botones.draw(self.canvas)
    
    def ReleaseButton(self):
        self.DeselectAll(self.botones)
        self.current.serElegido()
        self.botones.draw(self.canvas)
          
    def Reset(self):
        '''Resetea el estado de la ventana. Esta función es solo un hook.'''
        pass
    
    def __repr__(self):
        return 'Menu_'+self.nombre+' (en '+str(len(self.groups()))+' grupos)'