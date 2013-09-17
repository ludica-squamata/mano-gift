import sys
from pygame import mask,time
from random import randint,choice
from misc import Resources as r
from base import _giftSprite
from globs import World as W, Constants as C, Tiempo as T
from .MobGroup import MobGroup
from .Vision import area_vision
from .scripts import movimiento

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 4
    images = {} #incluye todas las imagenes del mob, arriba abajo izquierda y derecha
    death_img = None #sprite del mob muerto.
    dead = False
    direcciones = {'abajo':[0,1],'izquierda':[1,0],'arriba':[0,-1],'derecha':[-1,0],'ninguna':[0,0]}
    direccion = 'abajo'
    ticks,mov_ticks = 0,0
    AI = None # determina cómo se va a mover el mob
    modo_colision = None# determina qué direccion tomará el mob al chocar con algo
    patrol_p = []
    next_p = 0
    vision = None
    show = {}
    hide = {}
    punto_inicio = []
    punto_destino = []
    
    def __init__(self, ruta_img,stage,x=None,y=None,data = None):
        maskeys=['S'+'abajo','S'+'arriba','S'+'derecha','S'+'izquierda',
                 'I'+'abajo','I'+'arriba','I'+'derecha','I'+'izquierda',
                 'D'+'abajo','D'+'arriba','D'+'derecha','D'+'izquierda']

        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {} # si no lo redefino, pasan cosas raras...
        self.patrol_p = []
        self.generar_rasgos()
        for key in maskeys:
            self.images[key] = spritesheet[maskeys.index(key)]
        self.image = self.images['Sabajo']
        super().__init__(self.image,stage)

        if data != None:
            self.direccion = data['direccion']
            self.vision = area_vision(self.direccion)
            self.AI = data['AI']
            self.velocidad = data['velocidad']
            self.modo_colision = data['modo_colision']
            self.salud = data['salud']
            self.actitud = data['actitud']
            if 'solido' in data:
                self.solido = data['solido']
            #eliminar esto una vez que esté aplicado a todos los mobs
            if 'death' in data:
                self.death_img = r.cargar_imagen(data['death'])

        if x != None and y != None:
            self.ubicar(x*C.CUADRO,y*C.CUADRO)
            if type(self.AI) == dict:
                if self.AI['seq'] == 'camino':
                    x,y = self.AI['puntos']['inicio']
                    self.punto_inicio = [x*C.CUADRO,y*C.CUADRO]
                    
                    x,y = self.AI['puntos']['destino']
                    self.punto_destino = [x*C.CUADRO,y*C.CUADRO]
                    
                    self.AI = movimiento.AI_caminar_por_ruta # function alias!
                    self.camino = movimiento.generar_camino(self)
                else:
                    for punto in self.AI['seq']:
                        dx,dy = self.AI['puntos'][punto]
                        dx += x*C.CUADRO
                        dy += y*C.CUADRO
                        self.patrol_p.append([dx,dy])
                    self.AI = movimiento.AI_patrol # function alias!
            else:
                self.AI = movimiento.AI_wander # function alias!
        
    def generar_rasgos(self):
        rasgos = r.abrir_json('scripts/rasgos.json')
        
        for car in rasgos['cars']:
            if rasgos['cars'][car]:
                self.show[car] = {"tipo": "atributo", "nombre":car, "value": 0}
            else:
                self.hide[car] = {"tipo": "atributo", "nombre":car, "value": 0}
        
        for hab in rasgos['habs']:
            if rasgos['habs'][hab]:
                self.show[hab] = {"tipo": "habilidad", "nombre":hab, "value": 0}
            else:
                self.hide[hab] = {"tipo": "habilidad", "nombre":hab, "value": 0}
                
        #print(self.nombre)
        #for car in self.cars:
        #    if self.cars[car]['show']:
        #        print(car, self.cars[car]["value"])
        #for hab in self.habs:
        #    if self.habs[hab]['show']:
        #        print(hab, self.habs[hab]["value"])
        #print()
        
        pass # just a hook to fold the function

    def cambiar_direccion(self,arg):
        direccion = 'ninguna'
    
        if arg == 'contraria':
            if self.direccion == 'arriba': direccion = 'abajo'
            elif self.direccion == 'abajo': direccion = 'arriba'
            elif self.direccion == 'izquierda': direccion = 'derecha'
            elif self.direccion == 'derecha': direccion = 'izquierda'
    
        elif arg in self.direcciones:
            direccion = arg
            
        self.direccion = direccion
        return direccion
        
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
        direccion = self.AI(self)
        self.vision.cambiar_direccion(direccion)
        self.cambiar_direccion(direccion)
        self._mover()
                
    def _mover(self):
        x,y = self.direcciones[self.direccion]
        dx,dy = x*self.velocidad,y*self.velocidad

        col_bordes = False #colision contra los bordes de la pantalla
        col_mobs = False #colision contra otros mobs
        col_heroe = False #colision contra el héroe
        col_props = False # colision contra los props
        col_mapa = False # colision contra las cajas de colision del propio mapa

        if self.solido:
            if self.stage.mapa.mask.overlap(self.mask,(self.mapX + dx, self.mapY)) is not None:
                col_mapa = True

            if self.stage.mapa.mask.overlap(self.mask,(self.mapX, self.mapY + dy)) is not None:
                col_mapa = True

            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
                if self.colisiona(spr,dx,dy):
                    col_props = True
            
            for spr in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
                if spr.solido:
                    if self.colisiona(spr,dx,dy):
                        col_mobs = True
                        
        if self.colisiona(W.HERO,dx,dy):
            col_heroe = True
            if self.actitud == 'hostil':
                self.atacar()

        newPos = self.mapX + dx
        if newPos < 0 or newPos > self.stage.mapa.rect.w-32:
            if C.ANCHO > self.rect.x - dx  >=0:
                col_bordes = True

        newPos = self.mapY + dy
        if newPos < 0 or newPos > self.stage.mapa.rect.h-32:
            if C.ALTO > self.rect.y - dy  >=0:
                col_bordes = True

        colisiones = [col_bordes,col_mobs,col_props,col_mapa,col_heroe]
        if any(colisiones):
            self.cambiar_direccion(self.modo_colision)

            x,y = self.direcciones[self.direccion]
            dx,dy = x*self.velocidad,y*self.velocidad
        
        self.animar_caminar()
        self.reubicar(dx, dy)
    
    def recibir_danio(self):
        self.salud -= 1
        
        if self.salud <= 0:
            if self.death_img != None:
                self.image = self.death_img
            else: # esto queda hasta que haga sprites 'muertos' de los npcs
                self.stage.contents.remove(self)
            self.dead = True
            MobGroup.removeMob(self)
    
    def ver(self):
        for spr in MobGroup.mobs:
            if MobGroup.mobs[spr] != self:
                spr = MobGroup.mobs[spr]
                v = self.vision
                if v.mask.overlap(spr.mask,(spr.mapX - v.x(self),
                                            spr.mapY - v.y(self))):
                                        
                    #print(self.nombre,'ve a',spr.nombre)
                    #self.cambiar_direccion('contraria')
                    
                    return spr # devuelve el mob a la vista.
                    
    def update(self):
        self.anim_counter += 1
        if self.anim_counter > self.anim_limit:
            self.anim_counter = 0
        if not W.onPause and not self.dead:
            self.ver()
            self.mover()