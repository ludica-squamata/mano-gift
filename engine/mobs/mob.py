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
    mana = 0

    def __init__(self, ruta_img, stage, x, y, data):

        for e in self.equipo:
            self.equipo[e] = None
        dirs = ['S', 'I', 'D']
        self.images = self.cargar_anims(ruta_img, dirs)
        self.mascaras = {}
        self.camino = []
        self.image = self.images['Sabajo']
        super().__init__(self.image,stage=stage)
        self.calcular_sombra(self.image)

        self.direccion = data['direccion']
        self.velocidad = data['velocidad']
        self.modo_colision = data['modo_colision']
        self.salud = data['salud']
        #self.actitud = data['actitud'] #sin efectos
        self.tipo = data['tipo']
        self.fuerza = data['fuerza']

        if 'solido' in data:
            self.solido = data['solido']
        #eliminar esto una vez que esté aplicado a todos los mobs
        if 'death' in data:
            self.death_img = r.cargar_imagen(data['death'])
        if 'objetivo' in data:
            self.objetivo = MobGroup.get(data['objetivo'])

        self.ubicar(x,y)
        self.generar_rasgos()
        MobGroup.add(self)

    
    def PC__init__(self,ruta_img,stage,x,y,data,ruta_alpha):
        # esta función se utiliza solo porque hay diferencias entre
        # lo que hay producido para el Hero y lo que hay para los NPC
        # cuando las capacidades se hayan igualado, PC utilizará el __init__
        # normal, igual que el resto de los Mobs.

        dirs = ['S', 'I', 'D']

        self.images = self.cargar_anims(ruta_img, dirs)
        self.mascaras = self.cargar_anims(ruta_alpha, dirs, True)

        self.mask  = self.mascaras['Sabajo']
        self.image = self.images['Sabajo']

        for e in self.equipo:
            self.equipo[e] = None
        super().__init__(self.image,alpha=self.mask,stage=stage)
        
        self.tipo = data['tipo']
        self.fuerza = data['fuerza']
        self.salud = 10 #data['salud']#no hay salud establecida para el heroe
        self.mana = 10
        self.velocidad = 3 #data['velocidad']
        self.direccion = 'abajo' # sin efectos
        
        self.ubicar(x,y)
        MobGroup.add(self)
        

    def recibir_danio(self):
        self.salud -= 1
       
        if self.salud <= 0:
            if self.death_img != None:
                self.image = self.death_img
            else: # esto queda hasta que haga sprites 'muertos' de los npcs
                ED.RENDERER.delObj(self)
                self.stage.delProperty(self)
            self.dead = True
            MobGroup.remove(self)
    
    def update(self):
        self.anim_counter += 1
        if self.anim_counter > self.anim_limit:
            self.anim_counter = 0
        if not ED.onPause and not self.dead:
            self.determinar_accion(self.ver())
            return self.mover()

