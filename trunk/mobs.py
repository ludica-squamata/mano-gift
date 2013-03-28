from pygame import sprite,mask
from random import randint,choice
from misc import Resources as r
from base import _giftSprite

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 4
    def __init__(self, ruta_img,stage):
        keys = 'abajo,derecha,arriba,izquierda'.split(',')
        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {}
        for key in keys:
            self.images[key] = spritesheet[keys.index(key)]
        self.image = self.images['abajo']
        self.direccion = 'abajo'
        super().__init__(self.image,stage)
    
    def cambiar_direccion(self,direccion):
        self.image = self.images[direccion]
        self.direccion = direccion
    
class PC (Mob):
    centroX = 0
    centroY = 0
    def __init__(self,ruta_imgs,stage):
        super().__init__(ruta_imgs,stage)
    
    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de cuadros'''
        self.mapX += dx
        self.mapY += dy
        self.dirty = 1

class Enemy (Mob):
    ticks = 0
    mov_ticks = 0
    def __init__(self,ruta_imgs,stage):
        super().__init__(ruta_imgs,stage)
        
    
    def mover(self,hero):
        self.ticks += 1
        self.mov_ticks += 1
        direcciones = ['abajo','izquierda','arriba','derecha']
        movs = [[0,1],[1,0],[0,-1],[-1,0]]
        dx,dy = 0,0
                
        if self.mov_ticks == 3:
            pos = 10
            if randint(1,101) <= pos:
                self.cambiar_direccion (choice(direcciones))
            
            dx,dy = movs[direcciones.index(self.direccion)]
            self.mov_ticks = 0
        if not self.colisiona(hero,dx,dy):
            self.reubicar(dx, dy)
        else:#este comportamiento podría variar
             self.cambiar_direccion (choice(direcciones))
            
class NPC (Mob):
    pass

class Inventory(object):
    # la mochila
    pass

class Items(object):
    #para cosas que van en el inventario
    pass
