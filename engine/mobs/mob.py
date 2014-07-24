from .CompoMob import Equipado,Atribuido,Animado,Movil
from engine.base import _giftSprite
from engine.misc import Resources as r
from engine.globs import Constants as C, EngineData as ED, MobGroup
from pygame import mask

class Mob(Equipado, Atribuido, Animado, Movil, _giftSprite):
    mascaras = None  # {}
    camino = None  # []
    centroX, centroY = 0, 0
    hablante = False
    mana = 1
    cmb_pos_img = {} # combat position images.
    cmb_pos_alpha = {} # combat position images's alpha.
    cmb_walk_img = {} # combat walking images.
    cmb_walk_alpha = {} # combat walking images's alpha.
    idle_walk_img = {} #imagenes normales
    idle_walk_alpha = {}
    estado = '' #idle, o cmb. Indica si puede atacar desde esta posición, o no.

    def __init__(self,data,x,y,):
        self.images = {}
        self.mascaras = {}
        
        dirs = ['S','I','D']
        imgs = data['imagenes']
        alpha = data['alphas']
        for key in imgs:
            if imgs[key] != None:
                if key == 'idle':
                    self.idle_walk_img = self.cargar_anims(imgs['idle'],dirs)
                    self.idle_walk_alpha = self.cargar_anims(alpha['idle'],dirs,True)
                elif key == 'atk':
                    self.cmb_atk_img = self.cargar_anims(imgs['atk'],['A','B','C'])
                    self.cmb_atk_alpha = self.cargar_anims(alpha['atk'],['A','B','C'],True)
                elif key == 'cmb':
                    self.cmb_walk_img = self.cargar_anims(imgs['cmb'],dirs)
                    self.cmb_walk_alpha = self.cargar_anims(alpha['cmb'],dirs,True)
                elif key == 'death':
                    self.death_img = r.cargar_imagen(imgs['death'])
        
        #self.camino = []
        self.images = self.idle_walk_img
        self.mascaras = self.idle_walk_alpha
        self.image = self.images['Sabajo']
        self.mask = self.mascaras['Sabajo']
        
        #self.calcular_sombra(self.image)
        
        self.ID = data['ID']
        self.nombre = data['nombre']
        self.direccion = 'abajo'
        self.velocidad = data['velocidad']
        self.fuerza = data['fuerza']
        self.salud = data['salud']
        

        if 'solido' in data['propiedades']:
            self.solido = data['solido']
        
        if 'hostil' in data['propiedades']:
            self.actitud = 'hostil'
        elif 'pasiva' in data['propiedades']:
            self.actitud = 'pasiva'
        else:
            self.actitud = ''
            
        #if 'objetivo' in data:
        #    self.objetivo = MobGroup.get(data['objetivo'])
        
        self.establecer_estado('idle')
        super().__init__(imagen=self.image,alpha=self.mask)
        self.ubicar(x,y)
        self.generar_rasgos()
        if self.nombre not in MobGroup:
            MobGroup[self.nombre] = self
        
    def establecer_estado(self,estado):
        self.estado = estado
        if estado == 'idle':
            self.images = self.idle_walk_img
            self.mascaras = self.idle_walk_alpha
            
        elif estado == 'cmb':
            self.images = self.cmb_walk_img
            self.mascaras = self.cmb_walk_alpha
            
    def recibir_danio(self):
        self.salud -= 1
       
        if self.salud <= 0:
            if self.death_img != None:
                self.image = self.death_img
            else: # esto queda hasta que haga sprites 'muertos' de los npcs
                  # pero necesito más resolución para hacerlos...
                ED.RENDERER.delObj(self)
                self.stage.delProperty(self)
            self.dead = True
            del MobGroup[self.nombre]
    
    def update(self):
        self.anim_counter += 1
        if self.anim_counter > self.anim_limit:
            self.anim_counter = 0
        if not ED.onPause and not self.dead:
            self.determinar_accion(self.ver())
            return self.mover()

