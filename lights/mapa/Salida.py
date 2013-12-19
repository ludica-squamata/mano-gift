from pygame import sprite, Rect, Surface, mask as MASK, PixelArray
from misc import Resources as r, Util as U
from globs import Constants as C, World as W, Tiempo as T, QuestManager, MobGroup
from base import _giftSprite
from mobs import NPC, Enemy
from UI import Dialog, Menu, Menu_Items, Menu_Equipo,Menu_Pausa,Menu_Debug
from mobs.scripts.a_star import generar_grilla

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