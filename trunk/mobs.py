from pygame import sprite,mask
from random import randint,choice
from misc import Resources as r
from base import _giftSprite
from globs import World as W, Constants as C

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 4
    def __init__(self, ruta_img,stage):
        keys = 'abajo,derecha,arriba,izquierda'.split(',')
        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {}
        for key in keys:
            self.images[key] = spritesheet[keys.index(key)]
        self.image = self.images[self.direccion]
        super().__init__(self.image,stage)

    def cambiar_direccion(self,direccion):
        self.image = self.images[direccion]
        self.direccion = direccion

class PC (Mob):
    centroX = 0
    centroY = 0
    def __init__(self,ruta_imgs,stage):
        self.direccion = 'abajo'
        super().__init__(ruta_imgs,stage)
        

    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de cuadros'''
        self.mapX += dx
        self.mapY += dy
        self.dirty = 1

class Enemy (Mob):
    ticks = 0
    mov_ticks = 0
    AI = None
    start_pos = 0,0

    def __init__(self,key,ruta_imgs,stage,x,y):
        data = r.abrir_json('mobs/enemies.json')#no deberia abrir toda la base por un solo mob
        self.direccion = 'abajo'
        super().__init__(ruta_imgs,stage)
        self.AI = data[key]['AI']
        self.start_pos = x,y

    def mover(self):
        direcciones = {
            'abajo':[0,1],
            'izquierda':[1,0],
            'arriba':[0,-1],
            'derecha':[-1,0]}
        
        if self.AI == None:
            self.ticks += 1
            self.mov_ticks += 1
            self._mover(direcciones)
            if self.mov_ticks == 3:
                self.mov_ticks = 0
                pos = 10
                if randint(1,101) <= pos:
                    self.direccion_aleatoria(direcciones)
        
        else:
            START = self.start_pos
            CURR_X = self.mapX
            CURR_Y = self.mapY
            
            modo = self.AI['modo']
            eje  = self.AI['eje']
            dist = self.AI['dist']
            
            if modo == 'Patrulla':
                if eje == 'x':
                    pA = START[0]-dist
                    pB = START[0]+dist
                    
                    self.cambiar_direccion('izquierda')
                    del direcciones['arriba'],direcciones['abajo']
                    
                    if CURR_X -1 == pA:
                        print("pA_X alcanzado",self.mapX,str(pB))
                        self.cambiar_direccion('izquierda')
                    
                        self._mover(direcciones)
                    if CURR_X +1 == pB:
                        print("pB_X alcanzado",self.mapX,str(pB))
                        self.cambiar_direccion('derecha')
                    
                        self._mover(direcciones)
                    
                    self._mover(direcciones)
                    
                elif eje == 'y':
                    pA = START[1]-dist
                    pB = START[1]+dist
                    
                    self.cambiar_direccion('abajo')
                    del direcciones['izquierda'],direcciones['derecha']
                    
                    if CURR_Y -1 == pA:
                        print("pA_Y alcanzado",self.mapY)
                        self.cambiar_direccion('abajo')
                        
                        self._mover(direcciones)
                    if CURR_Y +1 == pB:
                        print("pB_Y alcanzado",self.mapY)
                        self.cambiar_direccion('arriba')
                    
                        self._mover(direcciones)
                    
                    self._mover(direcciones)
                    
    def _mover(self,direcciones):
        dx,dy = direcciones[self.direccion]
        layers = [C.CAPA_GROUND_ITEMS,
                  C.CAPA_GROUND_MOBS,
                  C.CAPA_HERO]
        
        if self.stage.mapa.mask.overlap(self.mask,(self.mapX + dx, self.mapY)) is not None:
            self.cambiar_direccion (choice(list(direcciones.keys())))
        if self.stage.mapa.mask.overlap(self.mask,(self.mapX, self.mapY + dy)) is not None:
            self.cambiar_direccion (choice(list(direcciones.keys())))
        for layer in layers:
            for spr in self.stage.contents.get_sprites_from_layer(layer):
                if self != spr:
                    if self.colisiona(spr,dx,dy):
                        #este comportamiento podría variar
                        self.cambiar_direccion (choice(list(direcciones.keys())))
        self.reubicar(dx, dy)

    def direccion_aleatoria(self,direcciones):
        self.cambiar_direccion (choice(list(direcciones.keys())))
    
class NPC (Mob):
    pass

class Inventory(object):
    # la mochila
    pass

class Items(object):
    #para cosas que van en el inventario
    pass
