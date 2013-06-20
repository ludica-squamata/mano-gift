from pygame import mask,Surface,time
from random import randint,choice
from misc import Resources as r
from base import _giftSprite
from globs import World as W, Constants as C, Tiempo as T

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
            self.cambiar_direccion(data['direccion'])
            self.AI = data['AI']
            self.velocidad = data['velocidad']
            self.modo_colision = data['modo_colision']
            if 'solido' in data:
                self.solido = data['solido']

        if x != None and y != None:
            self.start_pos = x*C.CUADRO,y*C.CUADRO
            self.ubicar(*self.start_pos)

    def cambiar_direccion(self,arg):
        direccion = 'ninguna'

        if arg == 'random':
            lista = list(self.direcciones.keys())
            lista.remove(self.direccion)
            direccion = choice(lista)

        elif arg == 'contraria':
            if self.direccion == 'arriba':
                direccion = 'abajo'

            elif self.direccion == 'abajo':
                direccion = 'arriba'

            elif self.direccion == 'izquierda':
                direccion = 'derecha'

            elif self.direccion == 'derecha':
                direccion = 'izquierda'

        elif arg in self.direcciones:
            direccion = arg

        if direccion != 'ninguna':
            self.image = self.images[direccion]
            self.mask = mask.from_surface(self.image,1)
            #_rect_ = self.mask.get_bounding_rects()[0]
            #img = Surface((_rect_.w,_rect_.h))
            #self.image = img
        self.direccion = direccion

    def mover(self):
        if self.AI == "wanderer":
            self.ticks += 1
            self.mov_ticks += 1
            self._mover()
            if self.mov_ticks == 3:
                self.mov_ticks = 0
                pos = 10
                if randint(1,101) <= pos:
                    self.cambiar_direccion('random')
        
        elif type(self.AI) == dict:
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
                        self.cambiar_direccion(self.modo_colision)

                elif eje == 'y':
                    pA = START[1]-round(dist/2)
                    pB = START[1]+round(dist/2)

                    if CURR_Y - self.velocidad <= pA or CURR_Y + self.velocidad >= pB:
                        self.cambiar_direccion(self.modo_colision)

                self._mover()
        
        

    def _mover(self):
        x,y = self.direcciones[self.direccion]
        dx,dy = x*self.velocidad,y*self.velocidad

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
            self.cambiar_direccion(self.modo_colision)

            x,y = self.direcciones[self.direccion]
            dx,dy = x*self.velocidad,y*self.velocidad

        self.reubicar(dx, dy)

class PC (Mob):
    centroX = 0
    centroY = 0
    timer_animacion = 0
    frame_animacion = 1000/12
    inventario = {}
    interlocutor = None # para que el héroe sepa con quién está hablando, si lo está
    
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
        '''cambia la orientación del sprite y controla parte de la animación'''
        
        for key in self.images.keys():
            if self.image == self.images[key]:
                break
        self.timer_animacion += T.FPS.get_time()
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
        x,y = x*rango,y*rango

        for sprite in self.stage.contents:
            if sprite != self.stage.mapa:
                if self.colisiona(sprite,x,y):
                    if isinstance(sprite,Enemy):
                        self.atacar(sprite)

                    elif isinstance(sprite,Prop):
                        inst = self.interactuar(sprite,x,y)
                        if inst != None:
                            self.inventario.agregar(inst)

                    break

    def atacar(self,sprite):
        sprite.morir()

    def hablar(self):
        rango = 15

        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango

        for sprite in self.stage.contents:
            if sprite != self.stage.mapa:
                if self.colisiona(sprite,x,y):
                    if isinstance(sprite,NPC):
                        self.interlocutor = sprite
                        return self.interlocutor.hablar()
                    break
    
    def _interactuar(self,rango):
        #la idea sería que esta función discriminara con qué está interactuando
        #el heroe y que devolviera el método correspondiente.
        #sugiero esto porque hablar() y accion() comparten características redundantes.

        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango

        for sprite in self.stage.contents:
            if sprite != self.stage.mapa:
                if self.colisiona(sprite,x,y):
                    clase = sprite.__clase__
                    return clase # la idea es, luego, usar issubclass(clase,Mob) por ejemplo.
    
    def cambiar_opcion_dialogo(self,seleccion): #+1 ó -1
        dialog = self.stage.dialogs.get_sprite(0)

        mod = -seleccion
        
        return dialog.elegir_opcion(seleccion,mod)
    
    def confirmar_seleccion(self):
        dialog = self.stage.dialogs.get_sprite(0)
        self.interlocutor.hablar(dialog.sel)

    def interactuar(self,prop,x,y):
        return prop.interaccion(x=x,y=y)

    def ver_inventario(self):
        self.stage.setDialog(self.inventario.ver())
        return True

class NPC (Mob):
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.nombre = nombre
        self.dialogos = data['dialogo']
        self.pos_diag = -1

    def hablar(self, opcion=1):
        if not W.onSelect:
            self.pos_diag += 1
        
        if self.pos_diag >= len(self.dialogos):
            self.stage.endDialog()
            self.pos_diag = -1
            return False
        
        else:
            if type(self.dialogos[self.pos_diag]) != dict:
                texto = self.dialogos[self.pos_diag]
                W.onSelect = False
            
            else:
                if not W.onSelect:
                    texto = '\n'.join(self.dialogos[self.pos_diag])
                    W.onSelect = True
                    
                else:
                    sel = list(self.dialogos[self.pos_diag].keys())[opcion-1]
                    texto = self.dialogos[self.pos_diag][sel]
                    W.onSelect = False
                
            self.stage.setDialog(texto)
            return True
    
    def devolver_seleccion(self,sel):
        dialog = self.stage.dialogs.get_sprite(0)
        op = list(self.dialogos[self.pos_diag].keys())[dialog.sel-1]
        
        return self.dialogos[self.pos_diag][op]
        
    def mover(self):
        if self.pos_diag == -1:
            super().mover()

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
        self.contenido = []

    def ver (self):
        if len(self.contenido) < 1:
            texto = 'El inventario está vacío'
        else:
            toJoin = []
            existe = []
            for item in self.contenido:
                Item = str(item)
                if Item not in existe:
                    existe.append(Item)
                    toJoin.append(Item+' x'+str(self.contenido.count(item)))
            
            #toJoin = [str(item) for item in self.contenido]
            texto = ', '.join(toJoin)
        
        return texto

    def agregar(self,cosa):
        self.contenido.append(Item(cosa))

class Item:
    data = ''
    nombre = ''#el nombre para mostrar del ítem en cuestión
    def __init__(self,nombre):
        self.nombre = nombre
    
    def __str__(self):
        return self.nombre.capitalize()
    
    def __eq__(self,other):
        if type(self) == type(other):
            return True
    

    #para cosas que van en el inventario
