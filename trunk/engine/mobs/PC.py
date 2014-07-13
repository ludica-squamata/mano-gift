from pygame import Surface,Rect,mask
from engine.globs import Constants as C, Tiempo as T, MobGroup, EngineData as ED
from engine.misc import Util as U
from engine.UI import Inventario_rapido
from .Inventory import Inventory, InventoryError
from .CompoMob import Parlante
from .scripts import Dialogo
from .mob import Mob

class PC(Mob,Parlante):
    cmb_pos_img = {} # combat position images.
    cmb_pos_alpha = {} # combat position images's alpha.
    cmb_walk_img = {} # combat walking images.
    cmb_walk_alpha = {} # combat walking images's alpha.
    idle_walk_img = {} #imagenes normales
    idle_walk_alpha = {}
    estado = '' #idle, o cmb. Indica si puede atacar desde esta posición, o no.
    
    alcance_cc = 0 #cuerpo a cuerpo.. 16 es la mitad de un cuadro.
    atk_counter = 0
    atk_img_index = -1
    
    dx,dy = 0,0
    def __init__(self,data,stage,x,y):
        imgs = data['imagenes']
        self.nombre = 'heroe' #key in MobGroup
        super().PC__init__(imgs['idle']['graph'],stage,x,y,data,imgs['idle']['alpha'])
        
        self.idle_walk_img = self.images
        self.idle_walk_alpha = self.mascaras
        
        self.cmb_walk_img = self.cargar_anims(imgs['cmb']['graph'],['S','I','D'])
        self.cmb_walk_alpha = self.cargar_anims(imgs['cmb']['alpha'],['S','I','D'],True)
        
        self.cmb_pos_img = self.cargar_anims(imgs['atk']['graph'],['A','B','C'])
        self.cmb_pos_alpha = self.cargar_anims(imgs['atk']['alpha'],['A','B','C'],True)
        
        self.alcance_cc = data['alcance_cc']
        self.inventario = Inventory(10,10+self.fuerza)
        self.estado = 'idle'        
        ED.RENDERER.camara.setFocus(self)
    
    def mover(self,dx,dy):
        
        self.animar_caminar()
        if dx == 1: self.cambiar_direccion('izquierda')
        elif dx == -1: self.cambiar_direccion('derecha')
        elif dy == -1: self.cambiar_direccion('arriba')
        else: self.cambiar_direccion('abajo')
        
        dx,dy = dx*self.velocidad,dy*self.velocidad
        if not self.detectar_colisiones(dx,0):
            self.reubicar(dx,0) # el heroe se mueve en el mapa, no en la camara
        if not self.detectar_colisiones(0,dy):
            self.reubicar(0,dy)

        
        # POR ACA DEBERIA DETECTAR LAS SALIDAS
        #for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_SALIDAS):
        #    if h.colisiona(spr,-dx,-dy):
        #        ED.setear_mapa(spr.dest,spr.link)
        #        dx,dy = 0,0
        self.dx,self.dy = -dx,-dy
        
    def accion(self):
        x,y = self.direcciones[self.direccion]
        
        if self.estado == 'cmb':
            # la animacion de ataque se hace siempre,
            # sino pareciera que no pasa nada
            self.atacando = True
            sprite = self._interactuar_mobs(self.alcance_cc)
            if issubclass(sprite.__class__,Mob):
                if self.estado == 'cmb':
                    x,y = x*self.fuerza,y*self.fuerza
                    self.atacar(sprite,x,y)
        else:
            sprite = self._interactuar_props(x,y)
            if hasattr(sprite,'accion'):
                if sprite.accion == 'agarrar':
                    try:
                        item = sprite()
                        self.inventario.agregar(item)
                        self.stage.delProperty(sprite)
                        ED.RENDERER.camara.delObj(sprite)
                    except InventoryError as Error:
                        print(Error)
                elif sprite.accion == 'operar':
                    sprite.operar()
    
    def atacar(self,sprite,x,y):
        sprite.reubicar(x,y)
        sprite.recibir_danio()

    def _anim_atk (self,limite):
        # construir la animación
        frames,alphas = [],[]
        for L in ['A','B','C']:
            frames.append(self.cmb_pos_img[L+self.direccion])
            alphas.append(self.cmb_pos_alpha[L+self.direccion])
            
        # iniciar la animación
        self.atk_counter += 1
        if self.atk_counter > limite:
            self.atk_counter = 0
            self.atk_img_index += 1
            if self.atk_img_index > len(frames)-1:
                self.atk_img_index = 0
                self.atacando = False
                self.mask = self.cmb_walk_alpha['S'+self.direccion]
            self.mask = alphas[self.atk_img_index]
            self.calcular_sombra(frames[self.atk_img_index])
    
    def hablar(self):
        sprite = self._interactuar_mobs(self.alcance_cc)
        if sprite != None:
            if sprite.hablante:
                self.interlocutor = sprite
                self.interlocutor.responder()
                ED.DIALOG = Dialogo(self,self.interlocutor)
                return True
    
        return False
    
    def _interactuar_mobs(self,rango):
        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango

        for mob in self.stage.properties.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
            if mob != self:
                if self.colisiona(mob,x,y):
                    return mob
    
    def _interactuar_props(self,x,y):
        "Utiliza una máscara propia para seleccionar mejor a los props"
        self_mask = mask.Mask((32,32))
        self_mask.fill()
        dx,dy = x*32,y*32
    
        for prop in self.stage.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            x = prop.mapX-(self.mapX+dx)
            y = prop.mapY-(self.mapY+dy)
            if prop.image != None:
                prop_mask = mask.from_surface(prop.image)
                if prop_mask.overlap(self_mask,(-x,-y)):
                    return prop

    def ver_inventario(self):
        ED.DIALOG = Inventario_rapido()
    
    def usar_item (self,item):
        if item.tipo == 'consumible':
            print('Used',item.nombre) #acá iria el efecto del item utilizado.
            return self.inventario.remover(item)
        return self.inventario.cantidad(item)
            
    def cambiar_estado(self):
        if self.estado == 'idle':
            self.images = self.cmb_walk_img
            self.mascaras = self.cmb_walk_alpha
            self.estado = 'cmb'
            
        elif self.estado == 'cmb':
            self.images = self.idle_walk_img
            self.mascaras = self.idle_walk_alpha
            self.estado = 'idle'
        
        t_image = self.images['S'+self.direccion]
        self.image = U.crear_sombra(t_image)
        self.image.blit(t_image,[0,0])
        self.mask = self.mascaras['S'+self.direccion]
            
        self.cambiar_direccion(self.direccion)
        self.animar_caminar()
    
    def update(self):
        if self.atacando:
            self._anim_atk(5)
        dx,dy = self.dx,self.dy
        self.dx,self.dy = 0,0
        self.dirty = 1
        return dx,dy
