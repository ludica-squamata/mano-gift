from pygame import sprite,mask
from misc import Resources as r
#from globs import Constants as C
import pygame

class _giftSprite(sprite.DirtySprite):
    #mapX y mapY estan medidas en pixeles y son relativas al mapa
    mapX = 0
    mapY = 0
    nombre = '' # Para diferenciar mobs del mismo tipo (enemy por ejemplo)
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
        self.rect.move_ip(x,y)
        self.dirty = 1
    
    def colisiona(self, sprite, off_x = 0, off_y = 0):
        if self.nombre != sprite.nombre:
            rectA = self.mask.get_bounding_rects()[0]
            rectA.x = self.mapX+off_x
            rectA.y = self.mapY+off_y
            
            rectB = sprite.mask.get_bounding_rects()[0]
            rectB.x = sprite.mapX
            rectB.y = sprite.mapY
            
            #if rectA.colliderect(rectB) == 1:
            #    print(self.nombre+' colisiona con '+sprite.nombre)
            return rectA.colliderect(rectB)
        
    

