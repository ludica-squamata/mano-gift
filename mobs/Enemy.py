from . import Mob
from globs import World as W


class Enemy (Mob):
    atk_img = {}
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.nombre = nombre
        #self.atk_img = self.cargar_anims('mobs/'+nombre+'_atk.png',['A','B','C'])
        
    def atacar(self):
        pass
        #print('Mob '+self.nombre+' ataca al héroe!')
