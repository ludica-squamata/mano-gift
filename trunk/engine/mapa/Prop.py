from engine.misc import Util as U
from engine.globs import Constants as C
from engine.base import _giftSprite

class Prop (_giftSprite):
    '''Clase para los objetos de ground_items.
    
    
    Estos objetos no se pueden mover por si mismos, pero usualmente tienen
    algún tipo de interacción (agarrar, mover, cortar, etc).'''
        
    _propiedades = None #indica si es agarrable, cortable, movible, etc.
    _operable = None
    estado = 0
    sombra = None
    def __init__ (self,nombre, imagen, stage, x,y, data = None):
        super().__init__(imagen,stage=stage,x=x,y=y)
        self.nombre = nombre
        self.estado = 0
        self._propiedades = {}
        if data != None:
            if "propiedades" in data:
                for prop in data['propiedades']:
                    self._propiedades[prop] = True;
                
        if self.es('operable'):
            self._operable = [
                (data['propiedades'][prop]['0']['solido'],
                 data['propiedades'][prop]['0']['visible']),
                (data['propiedades'][prop]['1']['solido'],
                 data['propiedades'][prop]['1']['visible'])]
            self.solido = self._operable[0][0]
            self.visible = self._operable[0][1]
    
        if not self.es('sinsombra'):
            self.sombra = U.crear_sombra(self.image, self.mask)
        if not self.es('solido'):
            self.solido = False

    def interaccion(self,x=0,y=0):
        if self.es('agarrable'):
            return True
        
        elif self.es('operable'):
            if self.estado == 0:
                self.estado = 1
            else:
                self.estado = 0
            self.solido = self._operable[self.estado][0]
            self.visible = self._operable[self.estado][1]
            return False

        elif self.es('empujable'):
            #if self.es('pesado'):
            #    if x > 0: x -= 10
            #    elif x < 0: x += 10
            #
            #    if y > 0: y -= 10
            #    elif y < 0: y += 10
            
            image = self.sombra
            image.blit(self.image,[0,0])
            self.image = image
            
            self.reubicar(x,y)
            return False
    
    #devuelve true o false
    def es(self,propiedad):
        return(propiedad in self._propiedades and self._propiedades[propiedad])