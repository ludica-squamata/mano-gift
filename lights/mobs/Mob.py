import sys
from pygame import mask,time
from random import randint,choice
from misc import Resources as r, Util as U
from base import _giftSprite
from globs import World as W, Constants as C, Tiempo as T, MobGroup
from .Vision import area_vision
from .scripts import movimiento

class Mob (_giftSprite):
    '''Clase base para todos los Mobs'''
    velocidad = 1
    images = {} # incluye todas las imagenes del mob, arriba abajo izquierda y derecha
    death_img = None # sprite del mob muerto.
    dead = False
    direcciones = {'abajo':[0,1],'izquierda':[1,0],'arriba':[0,-1],'derecha':[-1,0],'ninguna':[0,0]}
    direccion = 'abajo'
    __key_anim = '' #para uso interno de animar_caminar
    ticks,mov_ticks = 0,0
    AI = None # determina cómo se va a mover el mob
    modo_colision = None# determina qué direccion tomará el mob al chocar con algo
    vision = None
    flee_counter = 0
    atacando = False
    show = {}
    hide = {}
    next_p = 0
    camino = []
    tipo = '' # determina si es una victima o un monstruo
    reversa = bool # indica si hay que dar media vuelta al llegar al final del camino, o no.
    
    equipo = {'yelmo':None,'aro 1':None,'aro 2':None,'cuello':None,'peto':None,
              'guardabrazos':None,'brazales':None,'faldar':None,'quijotes':None,
              'grebas':None,'mano buena':None,'mano mala':None,'botas':None,'capa':None,
              'cinto':None,'guantes':None,'anillo 1':None,'anillo 2':None}
    fuerza = 0 # capacidad del mob para empujar cosas.
    
    def __init__(self, ruta_img,stage,x=None,y=None,data = None,alpha = False):
        maskeys=['S'+'abajo','S'+'arriba','S'+'derecha','S'+'izquierda', # Standing
                 'I'+'abajo','I'+'arriba','I'+'derecha','I'+'izquierda', # paso Izquierdo
                 'D'+'abajo','D'+'arriba','D'+'derecha','D'+'izquierda'] # paso Derecho

        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {} # si no lo redefino, pasan cosas raras...
        self.mascaras = {}
        for e in self.equipo:
            self.equipo[e] = None
        if alpha:
            _mascaras = r.split_spritesheet(alpha)
            for key in maskeys:
                _alpha = _mascaras[maskeys.index(key)]
                self.mascaras[key] = mask.from_threshold(_alpha, C.COLOR_COLISION, (1,1,1,255))
            self.mask  = self.mascaras['Sabajo']
        self.camino = [] # si no lo redefino, pasan cosas raras...
        for key in maskeys:
            self.images[key] = spritesheet[maskeys.index(key)]
        self.image = self.images['Sabajo']
        if alpha:
            super().__init__(self.image,alpha=self.mask,stage=stage)
        else:
            super().__init__(self.image,stage=stage)

        if data != None:
            self.direccion = data['direccion']
            self.vision = area_vision(self.direccion)
            self.AI = data['AI']
            self.velocidad = data['velocidad']
            self.modo_colision = data['modo_colision']
            self.salud = data['salud']
            self.actitud = data['actitud']
            self.tipo = data['tipo']
            self.fuerza = data['fuerza']
            if 'solido' in data:
                self.solido = data['solido']
            #eliminar esto una vez que esté aplicado a todos los mobs
            if 'death' in data:
                self.death_img = r.cargar_imagen(data['death'])

        if x != None and y != None:
            self.ubicar(x*C.CUADRO,y*C.CUADRO)
            if self.AI == "wanderer":
                self.AI = movimiento.AI_wander # function alias!
                
            elif self.AI == "patrol":
                inicio = x,y
                self.reversa = data['reversa']
                for x,y in data['camino']:
                    destino = x,y
                    camino = movimiento.generar_camino(inicio,destino,self.stage.grilla)
                    ruta = movimiento.simplificar_camino(camino)
                    self.camino.extend(ruta)
                    inicio = x,y
                
                self.AI = movimiento.AI_patrol # function alias!
            
            self._AI = self.AI #copia de la AI original
            self._camino = self.camino
    
    def generar_rasgos(self):
        rasgos = r.abrir_json('scripts/rasgos.json')
        
        for car in rasgos['cars']:
            if rasgos['cars'][car]:
                if car == "Fuerza":
                    self.show[car] = {"tipo": "atributo", "nombre":car, "value": self.fuerza}
                else:
                    self.show[car] = {"tipo": "atributo", "nombre":car, "value": 0}
            else:
                self.hide[car] = {"tipo": "atributo", "nombre":car, "value": 0}
        
        for hab in rasgos['habs']:
            if rasgos['habs'][hab]:
                self.show[hab] = {"tipo": "habilidad", "nombre":hab, "value": 0}
            else:
                self.hide[hab] = {"tipo": "habilidad", "nombre":hab, "value": 0}
                
        #print(self.nombre)
        #for rasgo in self.show:
        #    if self.show[rasgo]['tipo'] == "atributo":
        #        print(self.show[rasgo]['nombre'],self.show[rasgo]["value"])
        #print()
        #for rasgo in self.show:
        #    if self.show[rasgo]['tipo'] == "habilidad":
        #        print(self.show[rasgo]['nombre'],self.show[rasgo]["value"])
        #print()
        pass # just a hook to fold the function
    
    def equipar_item(self,item):
        self.equipo[item.esEquipable] = item
        self.inventario.quitar(item.ID)
        
    def desequipar_item(self,item):
        self.equipo[item.esEquipable] = None
        self.inventario.agregar(item)
        
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
        
        key = self.__key_anim
        self.t_image = None
        
        self.timer_animacion += T.FPS.get_time()
        if self.timer_animacion >= self.frame_animacion:
            self.timer_animacion = 0
            if self.direccion != 'ninguna':
                if key == 'D'+self.direccion:
                    key = 'I'+self.direccion
                elif key == 'I'+self.direccion:
                    key = 'D'+self.direccion
                else:
                    key = 'D'+self.direccion
                self.t_image = self.images[key]
                self.calcular_sombra()
                self.__key_anim = key
                
    def calcular_sombra(self):
        image = U.crear_sombra(self.t_image)
        image.blit(self.t_image,[0,0])
        self.image = image
    
    def cargar_anims(self,ruta_imgs,seq,alpha=False):
        dicc = {}
        spritesheet = r.split_spritesheet(ruta_imgs)
        dires = ['abajo','arriba','derecha','izquierda']
        keys = []
        
        for L in seq:
            for D in dires:
                keys.append(L+D)
        
        for key in keys:
            if not alpha:
                dicc[key] = spritesheet[keys.index(key)]
            else:
                _alpha = mask.from_threshold(spritesheet[keys.index(key)], C.COLOR_COLISION, (1,1,1,255))
                dicc[key] = _alpha
        return dicc
    
    def empujar_props(self,dx=None,dy=None):
        rango = 12
        if dx == None and dy == None:
            dx,dy = self.direcciones[self.direccion]
        
        x,y = dx*rango,dy*rango
        for spr in self.stage.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if spr.solido and spr.es('empujable') and self.solido:
                if self.colisiona(spr,x,y):
                    spr.interaccion(x,y)
    
    def mover(self):
        direccion = self.AI(self)
        self.empujar_props()
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

            for spr in self.stage.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
                if self.colisiona(spr,dx,dy):
                    if spr.solido:
                        col_props = True
            
            for spr in self.stage.properties.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
                if spr.solido:
                    if self.colisiona(spr,dx,dy):
                        col_mobs = True
                        
        if self.colisiona(W.HERO,dx,dy):
            col_heroe = True

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
                self.stage.properties.remove(self)
            self.dead = True
            MobGroup.remove(self)
    
    def ver(self):
        for key in MobGroup:
            mob = MobGroup[key]
            if mob != self:
                v = self.vision
                if self.actitud == 'hostil' and mob.tipo == 'victima':
                    if v.mask.overlap(mob.mask,(mob.mapX - v.x(self),mob.mapY - v.y(self))):
                        self.AI = movimiento.AI_pursue # function alias!
                        self.next_p = 0
                        self.camino = movimiento.iniciar_persecucion(self,mob)
                    else:
                        self.AI = self._AI
                        self.camino = self._camino

                elif self.actitud == 'pasiva' and mob.tipo == 'monstruo':
                    if v.mask.overlap(mob.mask,(mob.mapX - v.x(self),mob.mapY - v.y(self))) \
                    or self.flee_counter < 200:
                        self.AI = movimiento.AI_flee
                    else:
                        self.AI = self._AI

                    
    def update(self):
        self.anim_counter += 1
        if self.anim_counter > self.anim_limit:
            self.anim_counter = 0
        if not W.onPause and not self.dead:
            #self.ver()
            self.mover()
