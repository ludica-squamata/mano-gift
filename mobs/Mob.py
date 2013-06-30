from pygame import mask,time
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
            self.stage.quest.actualizar(self.nombre)
        else:
            print('Mob '+self.nombre+' ha recibido 1 daño, quedan '+str(self.salud))
    
    def update(self):
        self.anim_counter += 1
        if self.anim_counter > self.anim_limit:
            self.anim_counter = 0
        if not W.onPause:
            self.mover()