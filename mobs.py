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
        maskeys=['S'+'abajo','S'+'arriba','S'+'derecha','S'+'izquierda',
                 'I'+'abajo','I'+'arriba','I'+'derecha','I'+'izquierda',
                 'D'+'abajo','D'+'arriba','D'+'derecha','D'+'izquierda']

        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {} # si no lo redefino, pasan cosas raras...
        for key in maskeys:
            self.images[key] = spritesheet[maskeys.index(key)]
        self.image = self.images['Sabajo']
        super().__init__(self.image,stage)

        if data != None:
            self.cambiar_direccion(data['direccion'])
            self.AI = data['AI']
            self.velocidad = data['velocidad']
            self.modo_colision = data['modo_colision']
            self.salud = data['salud']
            self.actitud = data['actitud']
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
        self.direccion = direccion
        
    def animar_caminar(self):
        '''cambia la orientación del sprite y controla parte de la animación'''
        
        for key in self.images.keys():
            if self.image == self.images[key]:
                break
        self.timer_animacion += T.FPS.get_time()
        if self.timer_animacion >= self.frame_animacion:
            self.timer_animacion = 0
            if key == 'D'+self.direccion:
                self.image = self.images['I'+self.direccion]
            elif key == 'I'+self.direccion:
                self.image = self.images['D'+self.direccion]
            elif self.direccion == 'ninguna':
                pass
            else:
                self.image = self.images['D'+self.direccion]
    
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
                if self.colisiona(spr,dx,dy):
                    col_items = True
                    #print(self.nombre+' colisiona con '+str(spr.nombre))
            
            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
                if self.colisiona(spr,dx,dy):
                    col_mobs = True
                    #print(self.nombre+' colisiona con '+str(spr.nombre))
            
        if self.colisiona(W.HERO,dx,dy):
            col_heroe = True
            if self.actitud == 'hostil':
                self.atacar()
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
        
        self.animar_caminar ()
        self.reubicar(dx, dy)
    
    def recibir_danio(self):
        self.salud -= 1
        
        if self.salud <= 0:
            self.stage.contents.remove(self)
            print('Mob '+self.nombre+' eliminado!')
        else:
            print('Mob '+self.nombre+' ha recibido 1 daño, quedan '+str(self.salud))
    
    def update(self):
        self.anim_counter += 1
        if self.anim_counter > self.anim_limit:
            self.anim_counter = 0
        if not W.onPause:
            self.mover()
    
class PC (Mob):
    centroX = 0
    centroY = 0
    inventario = {}
    interlocutor = None # para que el héroe sepa con quién está hablando, si lo está
    cmb_pos_img = {} # combat position images.
    cmb_walk_img = {} # combat walking images.
    estado = '' #idle, o cmb. Indica si puede atacar desde esta posición, o no.
    
    fuerza = 15
    alcance_cc = 16 #cuerpo a cuerpo.. 16 es la mitad de un cuadro.
    atk_counter = 0
    atk_img_index = -1
    atacando = False
    
    def __init__(self,nombre,ruta_imgs,stage):
        super().__init__(ruta_imgs,stage)
        self.cargar_anims('mobs/heroe_cmb_walk.png',self.cmb_walk_img,['S','I','D'])
        self.cargar_anims('mobs/heroe_cmb_atk.png',self.cmb_pos_img,['A','B','C'])
        self.nombre = nombre
        self.timer_animacion = 0
        self.inventario = Inventory()
        self.estado = 'idle'
    
    def cargar_anims(self,ruta_imgs,dict_dest,seq):
        spritesheet = r.split_spritesheet(ruta_imgs)
        dires = ['abajo','arriba','derecha','izquierda']
        keys = []
        
        for L in seq:
            for D in dires:
                keys.append(L+D)
            
        for key in keys:
            dict_dest[key] = spritesheet[keys.index(key)]
                
    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de cuadros'''
        self.mapX += dx
        self.mapY += dy
        self.dirty = 1

    def cambiar_direccion(self,direccion):
        '''cambia la orientación del sprite y controla parte de la animación'''
        if self.estado == 'idle':
            for key in self.images.keys():
                if self.image == self.images[key]:
                    break
        
        elif self.estado == 'cmb':
            for key in self.cmb_walk_img.keys():
                if self.image == self.cmb_walk_img[key]:
                    break
                
        self.timer_animacion += T.FPS.get_time()
        if self.timer_animacion >= self.frame_animacion:
            self.timer_animacion = 0
            if key == 'D'+direccion: img_dir = 'I'+direccion
            elif key == 'I'+direccion: img_dir = 'D'+direccion
            else: img_dir = 'D'+direccion
            
            if self.estado == 'idle':
                self.image = self.images[img_dir]
            elif self.estado == 'cmb':
                self.image = self.cmb_walk_img[img_dir]
                
        self.direccion = direccion
    
    def mover(self,dx,dy):
        rango = 12
        x,y = dx*rango,dy*rango
        
        for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if spr.solido and spr._eval_prop('empujable'):
                if self.colisiona(spr,x,y):
                    spr.interaccion(x,y)
    
    def accion(self):
        from mapa import Prop
        x,y = self.direcciones[self.direccion]
        
        sprite = self._interactuar(self.fuerza)
        if  issubclass(sprite.__class__,Mob):
            if self.estado == 'cmb':
                x,y = x*self.fuerza,y*self.fuerza
                self.atacar(sprite,x,y)

        elif isinstance(sprite,Prop):
            x,y = x*self.fuerza*2,y*self.fuerza*2
            if sprite.interaccion(x,y) != None:
                self.inventario.agregar(sprite.nombre)

    def atacar(self,sprite,x,y):
        self.atacando = True
        sprite.reubicar(x,y)
        sprite.recibir_danio()
    
    def _anim_atk (self,limite):
        # construir la animación
        frames = []
        for L in ['A','B','C']:
            frame = self.cmb_pos_img[L+self.direccion]
            frames.append(frame)
        
        # iniciar la animación
        self.atk_counter += 1
        if self.atk_counter > limite:
            self.atk_counter = 0
            self.atk_img_index += 1
            if self.atk_img_index > len(frames)-1:
                self.atk_img_index = 0
                self.atacando = False
            
            self.image = frames[self.atk_img_index]
            self.dirty = 1

    def hablar(self):
        rango = 15
        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango
        
        sprite = self._interactuar(rango)
        if isinstance(sprite,NPC):
            self.interlocutor = sprite
            return self.interlocutor.hablar()
    
    def _interactuar(self,rango):
        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango

        for sprite in self.stage.contents:
            if sprite != self.stage.mapa:
                if self.colisiona(sprite,x,y):
                    return sprite
    
    def cambiar_opcion_dialogo(self,seleccion): #+1 ó -1
        dialog = self.stage.dialogs.get_sprite(0)

        mod = -seleccion
        
        return dialog.elegir_opcion(seleccion,mod)
    
    def confirmar_seleccion(self):
        dialog = self.stage.dialogs.get_sprite(0)
        self.interlocutor.hablar(dialog.sel)

    def ver_inventario(self):
        self.stage.setDialog(self.inventario.ver())
        return True
    
    def cambiar_estado(self):
        if self.estado == 'idle':
            self.image = self.cmb_walk_img['S'+self.direccion]
            self.estado = 'cmb'
            
        elif self.estado == 'cmb':
            self.image = self.images['S'+self.direccion]
            self.estado = 'idle'
    
    def update(self):
        if self.atacando:
            self._anim_atk(5)
            
    
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
        
    def atacar(self):
        rango = 15

        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango

        for sprite in self.stage.contents:
            if sprite == W.HERO:
                if self.colisiona(sprite,x,y):
                    print('Mob '+self.nombre+' ataca al héroe!')

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
    '''Para cosas que van en el inventario'''
    
    data = ''
    nombre = ''#el nombre para mostrar del ítem en cuestión
    def __init__(self,nombre):
        self.nombre = nombre
    
    def __str__(self):
        return self.nombre.capitalize()
    
    def __eq__(self,other):
        if type(self) == type(other):
            return True
