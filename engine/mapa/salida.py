from pygame import Rect
from engine.globs import Constants as C
from engine.base import _giftSprite


class Salida (_giftSprite):
    def __init__(self,data):
        self.x,self.y,alto,ancho = data['rect']
        self.dest = data['dest']# string, mapa de destino.
        self.link = data['link']# string, nombre de la entrada en dest con la cual conecta
        _rect = Rect((0,0),(alto, ancho))
        #_image = ((alto, ancho))
        #_image.fill((255,0,0))
        super().__init__(rect = _rect,x = self.x, y= self.y)
        self.ubicar(self.x,self.y)
        self.mask.fill()
        #self.image.set_colorkey((0,0,0))
        self.solido = False