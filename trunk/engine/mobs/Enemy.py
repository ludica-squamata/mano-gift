from .mob import Mob
from engine.globs import World as W


class Enemy (Mob):
    atk_img = {}
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.nombre = nombre
        #self.atk_img = self.cargar_anims('mobs/'+nombre+'_atk.png',['A','B','C'])
        self.generar_rasgos()
        
    def atacar(self,mob):
        #print('Mob '+self.nombre+' ataca a '+mob.nombre+'!')
        #mob.recibir_danio()
        pass