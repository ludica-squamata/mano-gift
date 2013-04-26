from pygame import mask,Surface,time
from random import randint,choice
from misc import Resources as r
from base import _giftSprite
from globs import World as W, Constants as C,FPS
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
        keys = 'abajo,arriba,derecha,izquierda'.split(',')
        maskeys=['S'+'abajo','S'+'arriba','S'+'derecha','S'+'izquierda',
                 'I'+'abajo','I'+'arriba','I'+'derecha','I'+'izquierda',
                 'D'+'abajo','D'+'arriba','D'+'derecha','D'+'izquierda']
        

        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {} # si no lo redefino, pasan cosas raras...
        if len(spritesheet) > 4:
            for key in maskeys:
                self.images[key] = spritesheet[maskeys.index(key)]
            self.image = self.images['Sabajo']
        else:
            for key in keys:
                self.images[key] = spritesheet[keys.index(key)]
            self.image = self.images[self.direccion]
        super().__init__(self.image,stage)
        
        if data != None:
            self.cambiar_direccion(directo=data['direccion'])
            self.AI = data['AI']
            self.velocidad = data['velocidad']
            self.modo_colision = data['modo_colision']
            self.solido = data['solido']
        
        if x != None and y != None:
            self.start_pos = x*C.CUADRO,y*C.CUADRO
            self.ubicar(*self.start_pos)
        
    def cambiar_direccion(self, directo = None, modo = 'usuario'):
        direccion = 'ninguna'
        
        if modo == 'random':
            lista = list(self.direcciones.keys())
            lista.remove(self.direccion)
            direccion = choice(lista)
        
        elif modo == 'contraria':
            if self.direccion == 'arriba':
                direccion = 'abajo'
            
            elif self.direccion == 'abajo':
                direccion = 'arriba'
            
            elif self.direccion == 'izquierda':
                direccion = 'derecha'
            
            elif self.direccion == 'derecha':
                direccion = 'izquierda'
        
        elif modo == 'usuario' and directo != None:
            direccion = directo
         
        if direccion != 'ninguna':
            self.image = self.images[direccion]
            self.mask = mask.from_surface(self.image,1)
            #_rect_ = self.mask.get_bounding_rects()[0]
            #img = Surface((_rect_.w,_rect_.h))
            #self.image = img
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

                    if CURR_X - self.velocidad <= pA or CURR_X + self.velocidad >= pB:
                        self.cambiar_direccion(self, modo=self.modo_colision)

                elif eje == 'y':
                    pA = START[1]-round(dist/2)
                    pB = START[1]+round(dist/2)
                    
                    if CURR_Y - self.velocidad <= pA or CURR_Y + self.velocidad >= pB:
                        self.cambiar_direccion(self, modo=self.modo_colision)
                    
                self._mover()
                                
    def _mover(self):
        x,y = self.direcciones[self.direccion]
        dx,dy = x*self.velocidad,y*self.velocidad
        layers = [C.CAPA_GROUND_ITEMS,C.CAPA_GROUND_MOBS,C.CAPA_HERO]
        
        col_bordes = False #colision contra los bordes de la pantalla
        col_mobs = False #colision contra otros mobs
        col_heroe = False #colision contra el héroe
        col_items = False # colision contra los props
        col_mapa = False # colision contra las cajas de colision del propio mapa
        
        if self.solido:
            if self.stage.mapa.mask.overlap(self.mask,(self.mapX + dx, self.mapY)) is not None:
                col_mapa = True
                #print(self.nombre+' colisiona con el mapa en X')
            
            if self.stage.mapa.mask.overlap(self.mask,(self.mapX, self.mapY + dy)) is not None:
                col_mapa = True
                #print(self.nombre+' colisiona con el mapa en Y')
            
            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
                if self.colisiona(spr,dx,dy) == True:
                    col_items = True
                    #print(self.nombre+' colisiona con '+str(spr.nombre))
                    
            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
                if self.colisiona(spr,dx,dy) == True:
                    col_mobs = True
                    #print(self.nombre+' colisiona con '+str(spr.nombre))
                    
            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_HERO):
                if self.colisiona(spr,dx,dy) == True:
                    col_heroe = True
                    #print(self.nombre+' colisiona con '+str(spr.nombre))
        
        newPos = self.mapX + dx
        if newPos < 0 or newPos > self.stage.mapa.rect.w:
            if C.ANCHO > self.rect.x - dx  >=0:
                col_bordes = True
                #print(self.nombre+' colisiona con borde horizontal')
        
        newPos = self.mapY + dy
        if newPos < 0 or newPos > self.stage.mapa.rect.h:
            if C.ALTO > self.rect.y - dy  >=0:
                col_bordes = True
                #print(self.nombre+' colisiona con borde vertical')
        
        colisiones = [col_bordes,col_mobs,col_items,col_mapa,col_heroe]
        if any(colisiones):
            self.cambiar_direccion(self,modo=self.modo_colision)
        
            x,y = self.direcciones[self.direccion]
            dx,dy = x*self.velocidad,y*self.velocidad
        
        self.reubicar(dx, dy)

class PC (Mob):
    centroX = 0
    centroY = 0
    timer_animacion = 0
    frame_animacion = 1000/12
    inventario = {}
    
    def __init__(self,nombre,ruta_imgs,stage):
        super().__init__(ruta_imgs,stage)
        self.nombre = nombre
        self.timer_animacion = 0
        self.inventario = Inventory()
        
    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de cuadros'''
        self.mapX += dx
        self.mapY += dy
        self.dirty = 1
        
    def cambiar_direccion(self,direccion):
        for key in self.images.keys():
            if self.image == self.images[key]:
                break
        self.timer_animacion += FPS.get_time()
        if self.timer_animacion >= self.frame_animacion:
            self.timer_animacion = 0
            if key == 'D'+direccion:
                self.image = self.images['I'+direccion]
            elif key == 'I'+direccion:
                self.image = self.images['D'+direccion]
            else:
                self.image = self.images['D'+direccion]

        self.direccion = direccion
    
    def accion(self):
        from mapa import Prop
        rango = 15
        
        x,y = self.direcciones[self.direccion]
        x *= rango
        y *= rango
        
        for sprite in self.stage.contents:
            if sprite != self.stage.mapa:
                if self.colisiona(sprite,x,y):
                    if isinstance(sprite,Enemy):
                        self.atacar(sprite)
                        
                    elif isinstance(sprite,NPC):
                        self.hablar(sprite)
                    
                    elif isinstance(sprite,Prop):
                        inst = self.interactuar(sprite)
                        if inst != None:
                            self.inventario.agregar(inst)
                        
                    break
    
    def atacar(self,sprite):
        sprite.morir()
    
    def hablar(self,sprite):
        sprite.hablar()
    
    def interactuar(self,prop):
        return prop.interaccion()

    def ver_inventario(self):
        self.inventario.ver()
    
      
class NPC (Mob):
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.nombre = nombre
    
    def hablar(self):
        texto = Dialog('hola, heroe!')
        self.stage.dialogs.add(texto, layer=texto.layer)

class Enemy (Mob):
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.nombre = nombre
    
    def morir(self):
        self.stage.contents.remove(self)
        print('Mob '+self.nombre+' eliminado!')
  
class Inventory:
    contenido = {}
    # la mochila
    def __init__ (self):
        self.contenido = {}
    
    def ver (self):
        if len(self.contenido) < 1:
            print ('El inventario está vacío')
        else:
            print(', '.join(self.contenido.keys()))
    
    def agregar(self,cosa):
        self.contenido[cosa] = Item(cosa)
    
class Item:
    data = ''
    def __init__(self,data):
        self.data = data
    
    #para cosas que van en el inventario