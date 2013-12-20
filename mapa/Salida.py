from pygame import Surface
from globs import Constants as C
from base import _giftSprite


class Salida (_giftSprite):
    def __init__(self,data):
        self.x,self.y,alto,ancho = data['rect']
        self.dest = data['dest']# string, mapa de destino.
        self.link = data['link']# string, nombre de la entrada en dest con la cual conecta
        image = Surface((alto, ancho))
        #image.fill((255,0,0))
        super().__init__(image,x = self.x, y= self.y)
        self.ubicar(self.x*C.CUADRO,self.y*C.CUADRO)
        self.mask.fill()
        self.image.set_colorkey((0,0,0))
        self.solido = False