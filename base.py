from pygame import sprite,mask
from misc import Resources as r
#from globs import Constants as C
import pygame

class _giftSprite(sprite.DirtySprite):
    #mapX y mapY estan medidas en pixeles y son relativas al mapa
    mapX = 0
    mapY = 0
    def __init__(self, imagen, stage = '', x = 0, y = 0):
        super().__init__()
        if isinstance(imagen, str):
            self.image = r.cargar_imagen(imagen)
        elif isinstance(imagen, pygame.Surface):
            self.image = imagen
        else:
            raise TypeError('Imagen debe ser una ruta o un Surface')
        self.rect = self.image.get_rect()
        self.mask = mask.from_surface(self.image)
        self.mapX = x
        self.mapY = y
        self.stage = stage

    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de cuadros'''
        self.mapX += dx
        self.mapY += dy
        self.rect.move_ip(dx,dy)
        self.dirty = 1

    def ubicar(self, x, y):
        '''mueve el sprite a una ubicacion especifica. tiene que ser valor positivo'''
        if x < 0 or y < 0:
            raise ValueError('Coordenadas fuera de rango')
        self.mapX = x
        self.mapY = y
        self.dirty = 1

