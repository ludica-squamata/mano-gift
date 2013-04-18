from pygame import sprite,mask
from random import randint,choice
from misc import Resources as r
from base import _giftSprite
from globs import World as W, Constants as C
from UI import Dialog

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 4
    images = {} #incluye todas las imagenes del mob, arriba abajo izquierda y derecha
    direcciones = {'abajo':[0,1],'izquierda':[1,0],'arriba':[0,-1],'derecha':[-1,0],'ninguna':[0,0]}
    direccion = 'abajo'
    ticks,mov_ticks = 0,0
    AI = None # determina cómo se va a mover el mob
    modo_colision = None# determina qué direccion tomará el mob al chocar con algo
    start_pos = 0,0
    
    def __init__(self, ruta_img,stage,x=None,y=None,data = None):
        keys = 'abajo,derecha,arriba,izquierda'.split(',')
        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {} # si no lo redefino, pasan cosas raras...
        for key in keys:
            self.images[key] = spritesheet[keys.index(key)]
        self.image = self.images[self.direccion]
        super().__init__(self.image,stage)
        
        if data != None:
            self.direccion = data['direccion']
            self.AI = data['AI']
            self.velocidad = data['velocidad']
            self.modo_colision = data['modo_colision']
        
        if x != None and y != None:
            self.start_pos = x*C.CUADRO,y*C.CUADRO
            self.reubicar(*self.start_pos)

    def cambiar_direccion(self, directo = None, modo = 'usuario'):
        direccion = 'ninguna'
        
        if modo == 'random':
            direccion = choice(list(self.direcciones.keys()))
        
        elif modo == 'contraria':
            if self.direccion == 'arriba':
                direccion = 'abajo'
            
            elif self.direccion == 'abajo':
                direccion = 'arriba'
            
            elif self.direccion == 'izquierda':
                direccion = 'derecha'
            
            elif self.direccion == 'derecha':
                direccion = 'izquierda'
        
        elif modo == 'usuario':
            direccion = directo
         
        if direccion != 'ninguna':
            self.image = self.images[direccion]
        self.direccion = direccion
    
    def mover(self):
        if self.AI == None:
            self.ticks += 1
            self.mov_ticks += 1
            self._mover()
            if self.mov_ticks == 3:
                self.mov_ticks = 0
                pos = 10
                if randint(1,101) <= pos:
                    self.cambiar_direccion(self,modo='random')
        
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

                    if CURR_X - self.velocidad == pA or CURR_X + self.velocidad == pB:
                        self.cambiar_direccion(self,modo=self.modo_colision)

                elif eje == 'y':
                    pA = START[1]-round(dist/2)
                    pB = START[1]+round(dist/2)
                    
                    if CURR_Y - self.velocidad == pA or CURR_Y + self.velocidad == pB:
                        self.cambiar_direccion(self,modo=self.modo_colision)
                    
                self._mover()
                                
    def _mover(self):
        x,y = self.direcciones[self.direccion]
        dx,dy = x*self.velocidad,y*self.velocidad
        layers = [C.CAPA_GROUND_ITEMS,C.CAPA_GROUND_MOBS,C.CAPA_HERO]
        
        colisiona = False
        
        if self.stage.mapa.mask.overlap(self.mask,(self.mapX + dx, self.mapY)) is not None:
            colisiona = True
        
        if self.stage.mapa.mask.overlap(self.mask,(self.mapX, self.mapY + dy)) is not None:
            colisiona = True
        
        for layer in layers:
            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
                    colisiona = self.colisiona(spr,dx,dy)
        for layer in layers:
            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
                if spr != self:
                    colisiona = self.colisiona(spr,dx,dy)
        for layer in layers:
            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_HERO):
                    colisiona = self.colisiona(spr,dx,dy)
        
        newPos = self.mapX + dx
        if newPos < 0 or newPos > self.stage.mapa.rect.w:
            if C.ANCHO > self.rect.x - dx  >=0:
                self.reubicar(-dx, 0)
                self.rect.x -= dx
                colisiona = True
                #dx *= -1
        
        newPos = self.mapY + dy
        if newPos < 0 or newPos > self.stage.mapa.rect.h:
            if C.ALTO > self.rect.y - dy  >=0:
                self.reubicar(0, -dy)
                self.rect.y -= dy
                colisiona = True
                #dy *= -1
        
        if colisiona == True:
            self.cambiar_direccion(self,modo=self.modo_colision)
        
            x,y = self.direcciones[self.direccion]
            dx,dy = x*self.velocidad,y*self.velocidad
        
        self.reubicar(dx, dy)

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
    
    def accion(self):
        actuar = False
        rango = 15
        for mob in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):                    
            if self.direccion == 'arriba':
                if self.colisiona(mob,0,-1*rango):
                    actuar = True
                    objetivo = mob
            elif self.direccion == 'abajo':
                if self.colisiona(mob,0,+1*rango):
                    actuar = True
                    objetivo = mob
            elif self.direccion == 'derecha':
                if self.colisiona(mob,+1*rango,0):
                    actuar = True
                    objetivo = mob
            elif self.direccion == 'izquierda':
                if self.colisiona(mob,-1*rango,0):
                    actuar = True
                    objetivo = mob
            
        if actuar == True:
            if isinstance(objetivo,Enemy):
                objetivo.morir()
        
            elif isinstance(objetivo,NPC):
                objetivo.interactuar()
    
    def atacar(self):
        pass

class NPC (Mob):
    def __init__(self,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
    
    def interactuar(self):
        texto = Dialog('hola, heroe!')
        texto.show()
        #print(texto.texto)

class Enemy (Mob):
    def __init__(self,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
    
    def morir(self):
        self.stage.contents.remove(self)
        print('Mob eliminado!')
  
class Inventory(object):
    # la mochila
    pass

class Items(object):
    #para cosas que van en el inventario
    pass
