from engine.globs import EngineData as ED
#from engine.misc import Resources as r
from engine.base import _giftSprite
from pygame import Surface, draw

class LightSource(_giftSprite): #o combinar esto con prop?, no estoy seguro. probablemente de esta forma pueda tener mas flexibilidad
    '''Los objetos de esta clase tienen un area de luz, que permite ver y genera sombras'''
    color = 255,255,255,255
    area = None #un mask
    forma = 'Circulo' # circulo por defecto.
    origen = None #una coordenada desde donde se calcula el area. por ejemplo para un poste con iluminacion en la punta? por defecto center
    intensidad = 0
    
    estatico = False #para simular luces lejanas, como el sol. no les cambia el rect.pos
    encendido = True #apaguen esas luces!
    #animacion???
    
    
    def __init__ (self,intensidad,color,forma,origen):
        self.intensidad = intensidad
        self.color = color
        self.forma = forma
        self.origen = origen
        
        
        imagen = self._crear(100)
        self.rect = imagen.get_rect(center = self.origen)
        super().__init__(imagen,x = self.rect.x,y=self.rect.y)
        ED.RENDERER.addFgObj(self)
        #setear el resto de las propiedades del area de luz
        #registrarse en Stage como fuente de luz para recibir actualizaciones
    
    def _crear(self,radio):
        if self.forma == 'Circulo':
            img = Surface((radio*2,radio*2))
            draw.circle(img, self.color, (radio,radio), radio)
        img.set_alpha(self.intensidad)        
    
    def update(self):
        #revisar todos los Mob y Prop con sombra dentro del area de luz y setearles sus respectivas sombras
        pass