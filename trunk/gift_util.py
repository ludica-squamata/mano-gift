#coding: utf-8
from sys import path

from pygame import image, sprite


class Globales:
    VELOCIDAD = 1
    TAMANIO_CUADRO = 32

class Pos:
    x = 0
    y = 0
    layer = 0

class Grupos:
    from mobs_base import MobGroup
    gHeroe = MobGroup()
    gEnemigo = MobGroup()
    gNPC = MobGroup()
    gSolidos = MobGroup()
    gMovibles = MobGroup()
    gMapa = sprite.LayeredDirty()

class Mapa (sprite.DirtySprite):
    pass

def cargar_imagen(imagen):
    return image.load(path[0]+'/grafs/'+imagen).convert_alpha()
