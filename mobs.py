from pygame import sprite
from random import randint
from misc import Resources as r
from base import _giftSprite

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 4

class PC (Mob):
    centroX = 0
    centroY = 0

    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de cuadros'''
        self.mapX += dx
        self.mapY += dy
        self.dirty = 1

class Enemy (Mob):
    def mover(self):
        dx = randint(-1,1)*self.velocidad
        dy = randint(-1,1)*self.velocidad
        return dx,dy

class NPC (Mob):
    pass

class Inventory(object):
    # la mochila
    pass

class Items(object):
    #para cosas que van en el inventario
    pass
