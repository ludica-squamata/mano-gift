from globs import World as W
from misc import Resources as r
from base import _giftSprite

class LightSource(_giftSprite): #o combinar esto con prop?, no estoy seguro. probablemente de esta forma pueda tener mas flexibilidad
    '''Los objetos de esta clase tienen un area de luz, que permite ver y genera sombras'''
    color_luz = (255,255,255,255)
    area_luz = None #un mask
    origen_luz = None #una coordenada desde donde se calcula el area. por ejemplo para un poste con iluminacion en la punta? por defecto center
    estatico = False #para simular luces lejanas, como el sol. no les cambia el rect.pos
    encendido = True #apaguen esas luces!
    #animacion???
    
    def __init__ (self, nombre, imagen, stage, x, y, data = None):
        super().__init__(imagen,stage=stage,x=x*C.CUADRO,y=y*C.CUADRO)
        #setear el resto de las propiedades del area de luz
        #registrarse en Stage como fuente de luz para recibir actualizaciones
        
    def update(self):
        #revisar todos los Mob y Prop con sombra dentro del area de luz y setearles sus respectivas sombras
        pass