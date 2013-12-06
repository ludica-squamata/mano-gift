from misc import Resources as r
from .Mob import Mob
from .NPC import NPC
from .Inventory import Inventory
from .Item import Item
from globs import World as W, Constants as C, Tiempo as T
from UI import Inventario_rapido
from pygame import Surface,Rect

class PC (Mob):
    centroX = 0
    centroY = 0
    inventario = {}
    interlocutor = None # para que el héroe sepa con quién está hablando, si lo está
    cmb_pos_img = {} # combat position images.
    cmb_pos_alpha = {} # combat position images's alpha.
    cmb_walk_img = {} # combat walking images.
    cmb_walk_alpha = {} # combat walking images's alpha.
    estado = '' #idle, o cmb. Indica si puede atacar desde esta posición, o no.
    
    alcance_cc = 0 #cuerpo a cuerpo.. 16 es la mitad de un cuadro.
    atk_counter = 0
    atk_img_index = -1
    
    def __init__(self,nombre,data,stage):
        imgs = data['imagenes']
        super().__init__(imgs['idle']['graph'],stage,alpha=imgs['idle']['alpha'])
        
        self.cmb_walk_img = self.cargar_anims(imgs['cmb']['graph'],['S','I','D'])
        self.cmb_walk_alpha = self.cargar_anims(imgs['cmb']['alpha'],['S','I','D'],True)
        
        self.cmb_pos_img = self.cargar_anims(imgs['atk']['graph'],['A','B','C'])
        self.cmb_pos_alpha = self.cargar_anims(imgs['atk']['alpha'],['A','B','C'],True)
        
        self.fuerza = data['fuerza']
        self.alcance_cc = data['alcance_cc']
        self.tipo = data['tipo']
        self.velocidad = 3
        
        self.nombre = nombre
        self.timer_animacion = 0
        self.inventario = Inventory(10)
        self.estado = 'idle'
        self.generar_rasgos()
        
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
                self.mask = self.mascaras[img_dir]
            elif self.estado == 'cmb':
                self.image = self.cmb_walk_img[img_dir]
                self.mask = self.cmb_walk_alpha[img_dir]
                
        self.direccion = direccion
    
    def mover(self,dx,dy):
        self.empujar_props(dx,dy)
    
        d = 'abajo'
        if dx == 1:
            d = 'izquierda'
        elif dx == -1:
            d = 'derecha'
        elif dy == -1:
            d = 'arriba'
        self.cambiar_direccion(d)
      
    def accion(self):
        from mapa import Prop
        x,y = self.direcciones[self.direccion]
        
        if self.estado == 'cmb':
            # la animacion de ataque se hace siempre,
            # sino pareciera que no pasa nada
            self.atacando = True
            
        sprite = self._interactuar(self.alcance_cc)
        if issubclass(sprite.__class__,Mob):
            if self.estado == 'cmb':
                x,y = x*self.fuerza,y*self.fuerza
                self.atacar(sprite,x,y)

        elif isinstance(sprite,Prop):
            if not self.atacando:
                x,y = x*self.fuerza*2,y*self.fuerza*2
                if sprite.interaccion(x,y):
                    item = Item(sprite.nombre,sprite.es('stackable'),sprite.image)
                    if self.inventario.agregar(item):
                        self.stage.contents.remove(sprite)
                        self.stage.properties.remove(sprite)
                
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
            
            self.image = frames[self.atk_img_index]
            self.mask = alphas[self.atk_img_index]
            self.dirty = 1

    def hablar(self,onSelect):
        rango = 15
        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango
        
        sprite = self._interactuar(rango)
        if isinstance(sprite,NPC):
            self.interlocutor = sprite
            return self.interlocutor.hablar(onSelect)
        else:
            W.MODO = 'Aventura'
    
    def _interactuar(self,rango):
        x,y = self.direcciones[self.direccion]
        x,y = x*rango,y*rango

        for sprite in self.stage.properties:
            if sprite != self and sprite != self.stage.mapa:
                if self.colisiona(sprite,x,y):
                    return sprite
    
    def confirmar_seleccion(self):
        self.interlocutor.hablar(W.DIALOG.sel)

    def ver_inventario(self):
        W.DIALOG = Inventario_rapido()
    
    def usar_item (self,item):
        if not item.esEquipable:
            print('Used',item.nombre) #acá iria el efecto del item utilizado.
            return self.inventario.quitar(item.ID)
        return item.cantidad
            
    def cambiar_estado(self):
        if self.estado == 'idle':
            self.image = self.cmb_walk_img['S'+self.direccion]
            self.mask = self.cmb_walk_alpha['S'+self.direccion]
            self.estado = 'cmb'
            
        elif self.estado == 'cmb':
            self.image = self.images['S'+self.direccion]
            self.mask = self.mascaras['S'+self.direccion]
            self.estado = 'idle'
        self.cambiar_direccion(self.direccion)
        self.dirty = 1
    
    def update(self):
        if self.atacando:
            self._anim_atk(5)
