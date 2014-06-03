from .CompoMob import Equipado,Atribuido,Animado,Movil
from engine.base import _giftSprite
from engine.misc import Resources as r
from engine.globs import Constants as C, World as W
from .scripts import movimiento
from pygame import mask

class Mob(Equipado,Atribuido,Animado,Movil,_giftSprite):
    images = {}
    mascaras = {}
    camino = []
    centroX,centroY = 0,0
    def __init__(self,ruta_img,stage,x,y,data):
        maskeys=['S'+'abajo','S'+'arriba','S'+'derecha','S'+'izquierda', # Standing
                 'I'+'abajo','I'+'arriba','I'+'derecha','I'+'izquierda', # paso Izquierdo
                 'D'+'abajo','D'+'arriba','D'+'derecha','D'+'izquierda'] # paso Derecho

        spritesheet = r.split_spritesheet(ruta_img)
        self.images = {} # si no lo redefino, pasan cosas raras...
        self.mascaras = {}
        for e in self.equipo:
            self.equipo[e] = None        
        self.camino = [] # si no lo redefino, pasan cosas raras...
        for key in maskeys:
            self.images[key] = spritesheet[maskeys.index(key)]
        self.image = self.images['Sabajo']
        super().__init__(self.image,stage=stage)
        
        self.direccion = data['direccion']
        self.AI = data['AI']
        self.velocidad = data['velocidad']
        self.modo_colision = data['modo_colision']
        self.salud = data['salud']
        self.actitud = data['actitud']
        self.tipo = data['tipo']
        self.fuerza = data['fuerza']
        self.tri_vis = self.generar_tri_vision(32*5) #(data[vision])
        self.cir_vis = self.generar_cir_vision(32*6) #(data[vision])
        self.vision = self.tri_vis
        self.mover_vis = self.mover_tri_vis
        if 'solido' in data:
            self.solido = data['solido']
        #eliminar esto una vez que esté aplicado a todos los mobs
        if 'death' in data:
            self.death_img = r.cargar_imagen(data['death'])
        if 'objetivo' in data:
            self.objetivo = MobGroup.get(data['objetivo'])
            
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
    
    def PC__init__(self,ruta_img,stage,ruta_alpha):
        # esta función se utiliza solo porque hay diferencias entre
        # lo que hay producido para el Hero y lo que hay para los NPC
        # cuando las capacidades se hayan igualado, PC utilizará el __init__
        # normal, igual que el resto de los Mobs.
        maskeys=['S'+'abajo','S'+'arriba','S'+'derecha','S'+'izquierda', # Standing
        'I'+'abajo','I'+'arriba','I'+'derecha','I'+'izquierda', # paso Izquierdo
        'D'+'abajo','D'+'arriba','D'+'derecha','D'+'izquierda'] # paso Derecho

        _images = r.split_spritesheet(ruta_img)
        _mascaras = r.split_spritesheet(ruta_alpha)
        self.images = {} # si no lo redefino, pasan cosas raras...
        self.mascaras = {}       
        
        for key in maskeys:
            _alpha = _mascaras[maskeys.index(key)]
            self.mascaras[key] = mask.from_threshold(_alpha, C.COLOR_COLISION, (1,1,1,255))
            self.images[key] = _images[maskeys.index(key)]
        self.mask  = self.mascaras['Sabajo']
        self.image = self.images['Sabajo']
        
        for e in self.equipo:
            self.equipo[e] = None
        super().__init__(self.image,alpha=self.mask,stage=stage)

    def update(self):
        self.anim_counter += 1
        if self.anim_counter > self.anim_limit:
            self.anim_counter = 0
        if not W.onPause and not self.dead:
            self.determinar_accion(self.ver())
            return self.mover()