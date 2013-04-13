from pygame import sprite,mask
from random import randint,choice
from misc import Resources as r
from base import _giftSprite
from globs import World as W, Constants as C

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 4
    images = {} #incluye todas las imagenes del mob, arriba abajo izquierda y derecha
    def __init__(self, ruta_img,stage):
        keys = 'abajo,derecha,arriba,izquierda'.split(',')
        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {} # si no lo redefino, pasan cosas raras...
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
    AI = None # determina cómo se va a mover el mob
    modo_colision = None# determina qué direccion tomará el mob al chocar con algo
    start_pos = 0,0 
    direcciones = {
        'abajo':[0,1],
        'izquierda':[1,0],
        'arriba':[0,-1],
        'derecha':[-1,0]}

    def __init__(self,key,ruta_imgs,stage,x,y):
        data = r.abrir_json('mobs/enemies.json')#no deberia abrir toda la base por un solo mob
        self.direccion = data[key]['direccion']
        super().__init__(ruta_imgs,stage)
        self.AI = data[key]['AI']
        self.velocidad = data[key]['velocidad']
        self.modo_colision = data[key]['modo_colision']
        self.start_pos = x*C.CUADRO,y*C.CUADRO
        self.ubicar(*self.start_pos)

    def mover(self):
        if self.AI == None:
            self.ticks += 1
            self.mov_ticks += 1
            self._mover()
            if self.mov_ticks == 3:
                self.mov_ticks = 0
                pos = 10
                if randint(1,101) <= pos:
                    self.direccion_aleatoria(self.direcciones)
        
        else:
            START = self.start_pos
            CURR_X = self.mapX
            CURR_Y = self.mapY
            
            modo = self.AI['modo']
            eje  = self.AI['eje']
            dist = self.AI['dist']
            
            if modo == 'Patrulla':
                if eje == 'x':
                    pA = START[0]-round(dist/2)
                    pB = START[0]+round(dist/2)

                    if CURR_X - self.velocidad == pA:
                        self.direccion_contraria()

                    if CURR_X + self.velocidad == pB:
                        self.direccion_contraria()

                elif eje == 'y':
                    pA = START[1]-round(dist/2)
                    pB = START[1]+round(dist/2)
                    
                    if CURR_Y - self.velocidad == pA:
                        self.direccion_contraria()

                    if CURR_Y + self.velocidad == pB:
                        self.direccion_contraria()
                    
                self._mover()
                    
    def _mover(self):
        x,y = self.direcciones[self.direccion]
        dx,dy = x*self.velocidad,y*self.velocidad
        layers = [C.CAPA_GROUND_ITEMS,
                  C.CAPA_GROUND_MOBS,
                  C.CAPA_HERO]
        
        colisiona = False
        if self.stage.mapa.mask.overlap(self.mask,(self.mapX + dx, self.mapY)) is not None:
            colisiona = True
        if self.stage.mapa.mask.overlap(self.mask,(self.mapX, self.mapY + dy)) is not None:
            colisiona = True
        for layer in layers:
            for spr in self.stage.contents.get_sprites_from_layer(layer):
                if self != spr:
                    if self.colisiona(spr,dx,dy):
                        #este comportamiento podría variar
                        colisiona = True
        
        if colisiona == True:
            if self.modo_colision == 'aleatorio':
                self.direccion_aleatoria (self.direcciones)
            
            elif self.modo_colision == 'rebote':
                self.direccion_contraria()
        
        self.reubicar(dx, dy)

    def direccion_aleatoria(self,direcciones):
        self.cambiar_direccion (choice(list(direcciones.keys())))
    
    def direccion_contraria (self):
        if self.direccion == 'arriba':
             self.cambiar_direccion('abajo')
        
        elif self.direccion == 'abajo':
             self.cambiar_direccion('arriba')
        
        elif self.direccion == 'izquierda':
             self.cambiar_direccion('derecha')
        
        elif self.direccion == 'derecha':
             self.cambiar_direccion('izquierda')
    
    
class NPC (Mob):
    pass

class Inventory(object):
    # la mochila
    pass

class Items(object):
    #para cosas que van en el inventario
    pass
