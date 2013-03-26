from pygame import sprite,mask
from random import randint
from misc import Resources as r
from base import _giftSprite

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 4
    
class PC (Mob):
    centroX = 0
    centroY = 0
    def __init__(self,stage):
        self.images = {'abajo':r.cargar_imagen('grafs/heroe_color_abajo.png'),
                  'arriba':r.cargar_imagen('grafs/heroe_color_arriba.png'),
                  'izquierda':r.cargar_imagen('grafs/heroe_color_izquierda.png'),
                  'derecha':r.cargar_imagen('grafs/heroe_color_derecha.png')}
        self.image = self.images['abajo']
        super().__init__(self.image,stage)
        self.direccion = ''
    
    def cambiar_direccion(self,direccion):
        self.image = self.images[direccion]
        self.direccion = direccion
        self.mask = mask.from_surface(self.image)

    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de cuadros'''
        self.mapX += dx
        self.mapY += dy
        self.dirty = 1

class Enemy (Mob):
    ticks = mov_ticks = 0
    def mover(self):
        self.ticks += 1
        self.mov_ticks += 1
        dx,dy = 0,0
        if self.mov_ticks == 3:
            pos = 10
            if randint(1,100) <= pos:
                dx = randint(-1,1)*self.velocidad
                dy = randint(-1,1)*self.velocidad
            self.mov_ticks = 0
        
        self.reubicar(dx, dy)

class NPC (Mob):
    pass

class Inventory(object):
    # la mochila
    pass

class Items(object):
    #para cosas que van en el inventario
    pass
