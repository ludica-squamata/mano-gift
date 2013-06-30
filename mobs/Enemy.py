from pygame import mask,Surface,time
from random import randint,choice
from misc import Resources as r
from . import Mob
from globs import World as W, Constants as C, Tiempo as T


class Enemy (Mob):
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.nombre = nombre
        
    def atacar(self):
        rango = 15

        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango

        for sprite in self.stage.contents:
            if sprite == W.HERO:
                if self.colisiona(sprite,x,y):
                    print('Mob '+self.nombre+' ataca al héroe!')
