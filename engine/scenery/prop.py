from engine.base import _giftSprite
from engine.misc import Util as U

class Prop(_giftSprite):#,shadowSprite):
    def __init__(self,nombre,imagen,x,y):
        self.nombre = nombre
        self.tipo = 'Prop'
        super().__init__(imagen,x=x,y=y)
        self.solido = False
        
        #shadowSprite#
        self.sombra = U.crear_sombra(self.image, self.mask)
        image = self.sombra
        image.blit(self.image,[0,0])
        self.image = image
        #------------#
        
    
    def es(self,propiedad):
        if propiedad == 'solido':
            return False
        else: #empujable
            return True#no tiene sentido
        #pero si no lo pongo así,
        #no puedo pasar tras los arboles
        #algo tiene que ver con actualizar_grilla
        
    
    def interaccion(self,x=0,y=0):
        return False