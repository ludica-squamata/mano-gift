from engine.base import _giftSprite
from engine.misc import Util as U
from .items import *

class Escenografia(_giftSprite):#,shadowSprite):
    def __init__(self,nombre,imagen,x,y,sinsombra=False):
        self.nombre = nombre
        self.tipo = 'Prop'
        super().__init__(imagen,x=x,y=y)
        self.solido = False
        
        #shadowSprite#
        if not sinsombra:
            self.sombra = U.crear_sombra(self.image, self.mask)
            image = self.sombra
            image.blit(self.image,[0,0])
            self.image = image
        #------------#
    
    def update(self):
        self.dirty = 1

class Agarrable(Escenografia):
    def __init__(self,nombre,imagen,x,y,data):
        self.data = data
        super().__init__(nombre,imagen,x,y,True)
        self.subtipo = data['subtipo']
        self.accion = 'agarrar'
    
    def __call__(self):
        args = self.nombre,self.image,self.data
        if self.subtipo == 'consumible':  return Consumible(*args)
        elif self.subtipo == 'equipable': return Equipable(*args)
        elif self.subtipo == 'armadura':  return Armadura(*args)
        elif self.subtipo == 'arma':      return Arma(*args)
        elif self.subtipo == 'accesorio': return Accesorio(*args)
        elif self.subtipo == 'pocion':    return Pocion(*args)
        
class Movible(Escenografia):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)
        self.solido = True
        self.accion = 'mover'

class Trepable(Escenografia):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)
        self.accion = 'trepar'

class Operable(Escenografia):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)
        self.accion = 'operar'
    
    def operar(self):
        pass

class Destruible(Escenografia):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)
        self.accion = 'romper'
