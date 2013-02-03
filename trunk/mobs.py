from pygame import sprite
from misc import Resources as r
from globs import Constants as C
from base import _giftSprite

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 0

class PC (Mob):
    centroX = 0
    centroY = 0

class Enemy (Mob):
    def __init__(self):
        super().__init__()

class NPC (Mob):
    def __init__(self):
        super().__init__()

class Inventory(object):
    # la mochila
    pass

class Items(object):
    #para cosas que van en el inventario
    pass
