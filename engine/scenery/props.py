from engine.base import _giftSprite, _shadowSprite
from engine.misc import Util as U
from engine.misc import Resources as r
from pygame import mask as MASK
from .items import *

class Escenografia(_shadowSprite,_giftSprite):
    def __init__(self,nombre,imagen,x,y,sinsombra=False):
        self.nombre = nombre
        self.tipo = 'Prop'
        super().__init__(imagen,x=x,y=y)
        self.solido = False
        
        #shadowSprite#
        #if not sinsombra:
        #    self.sombra = U.crear_sombra(self.image, self.mask)
        #    image = self.sombra
        #    image.blit(self.image,[0,0])
        #    self.image = image
        #------------#
    
    def update(self):
        self.dirty = 1
        self.updateSombra()

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
    def update(self):
        pass
        
class Movible(Escenografia):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)
        self.data = data
        self.solido = True
        self.accion = 'mover'

class Trepable(Escenografia):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)
        self.data = data
        self.accion = 'trepar'

class Operable(Escenografia):
    estados = {}
    estado_actual = 0
    def __init__(self,nombre,imagen,x,y,data):
        if 'sinsombra' in data['propiedades']: super().__init__(nombre,imagen,x,y,True)
        else: super().__init__(nombre,imagen,x,y)
        if 'solido' in data['propiedades']: self.solido = True
        self.accion = 'operar'
        
        for estado in data['operable']:
            ID = estado['ID']
            self.estados[ID] = {}
            for attr in estado:
                if attr == 'image':
                    img = r.cargar_imagen(estado[attr])
                    mask = MASK.from_surface(img)
                    self.estados[ID].update({'image':img,'mask':mask})
                elif attr == 'next':
                    self.estados[ID].update({'next':estado[attr]})
                else:
                    self.estados[ID].update({attr:estado[attr]})
        
        self.image = self.estados[self.estado_actual]['image']
        self.mask = self.estados[self.estado_actual]['mask']
        self.solido = self.estados[self.estado_actual]['solido']
    
    def operar(self):
        self.estado_actual = self.estados[self.estado_actual]['next']
        for attr in self.estados[self.estado_actual]:
            if hasattr(self,attr):
                setattr(self,attr,self.estados[self.estado_actual][attr])
    def update(self):
        pass

class Destruible(Escenografia):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)
        self.accion = 'romper'
    def update(self):
        pass
