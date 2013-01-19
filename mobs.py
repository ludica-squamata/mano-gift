from pygame import sprite
from misc import Resources as r

class MobGroup (sprite.LayeredDirty):
    '''Grupo Básico para todos los Mobs'''
    
    def __init__ (self,*sprites):
        super().__init__(*sprites)

class Mob (sprite.DirtySprite):
    '''Clase base para todos los Mobs'''
    def __init__(self,ruta):
        super().__init__()
        self.x = 0
        self.y = 0
        self.pos = self.x,self.y
        self.velocidad = 32
        self.sprite = r.cargar_imagen(ruta)
        self.rect = self.sprite.get_rect()
        
    def reubicar (self,x,y):
        self.x += x*self.velocidad
        self.y += y*self.velocidad
        self.pos = self.x,self.y
        

class PC (Mob):
    def __init__(self,ruta):
        super().__init__(ruta)

class Enemy (Mob):
    def __init__(self):
        super().__init__()

class NPC (Mob):
    def __init__(self):
        super().__init__()

class Inventory:
    # la mochila
    pass

class Items:
    #para cosas que van en el inventario
    pass

