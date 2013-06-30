from . import Mob
from globs import World as W


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
