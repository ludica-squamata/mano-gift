from . import Equipado,Atribuido,Animado,Sensitivo,Inteligente,Movil
from base import _giftSprite
from misc import Resources as r
from globs import Constants as C, World as W
from mobs.scripts import movimiento
from pygame import mask

class Mob(Equipado,Atribuido,Animado,Sensitivo,Inteligente,Movil,_giftSprite):
    images = {}
    mascaras = {}
    camino = []
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
    
    def update(self):
        self.anim_counter += 1
        if self.anim_counter > self.anim_limit:
            self.anim_counter = 0
        if not W.onPause and not self.dead:
            self.determinar_accion(self.ver())
            return self.mover()