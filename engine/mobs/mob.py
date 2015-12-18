from .CompoMob import Equipado, Animado, Movil, Interactivo
from engine.globs import MobGroup
from engine.misc import Resources as Rs
from engine.base import ShadowSprite


class Mob(Interactivo, Equipado, Animado, Movil, ShadowSprite):  # Movil es Atribuido para tener .velocidad
    tipo = "Mob"
    mascaras = None  # {}
    camino = None  # []
    centroX, centroY = 0, 0
    hablante = False
    mana = 1
    cmb_pos_img = {}  # combat position images.
    cmb_pos_alpha = {}  # combat position images's alpha.
    cmb_walk_img = {}  # combat walking images.
    cmb_walk_alpha = {}  # combat walking images's alpha.
    idle_walk_img = {}  # imagenes normales
    idle_walk_alpha = {}
    estado = ''  # idle, o cmb. Indica si puede atacar desde esta posición, o no.
    
    moviendose = False
    def __init__(self, data, x, y, focus = False):
        self.images = {}
        self.mascaras = {}
        self.data = data

        dirs = ['S', 'I', 'D']
        imgs = data['imagenes']
        alpha = data['alphas']
        for key in imgs:
            if imgs[key] is not None:
                if key == 'idle':
                    self.idle_walk_img = self.cargar_anims(imgs['idle'], dirs)
                    self.idle_walk_alpha = self.cargar_anims(alpha['idle'], dirs, True)
                elif key == 'atk':
                    self.cmb_atk_img = self.cargar_anims(imgs['atk'], ['A', 'B', 'C'])
                    self.cmb_atk_alpha = self.cargar_anims(alpha['atk'], ['A', 'B', 'C'], True)
                elif key == 'cmb':
                    self.cmb_walk_img = self.cargar_anims(imgs['cmb'], dirs)
                    self.cmb_walk_alpha = self.cargar_anims(alpha['cmb'], dirs, True)
                elif key == 'death':
                    self.death_img = Rs.cargar_imagen(imgs['death'])
                elif key == "diag_face":
                    self.diag_face = Rs.cargar_imagen(imgs["diag_face"])


        self.images = self.idle_walk_img
        self.mascaras = self.idle_walk_alpha
        self.image = self.images['Sabajo']
        self.mask = self.mascaras['Sabajo']

        self.ID = data['ID']
        self.nombre = data['nombre']
        self.direccion = 'abajo'

        if 'solido' in data['propiedades']:
            self.solido = data['solido']

        if 'hostil' in data['propiedades']:
            self.actitud = 'hostil'
        elif 'pasiva' in data['propiedades']:
            self.actitud = 'pasiva'
        else:
            self.actitud = ''

        if 'objetivo' in data:
            self.objetivo = MobGroup[data['objetivo']]

        self.establecer_estado('idle')
        super().__init__(imagen = self.image, alpha = self.mask, x = x, y = y, center = focus)

        if self.nombre not in MobGroup:
            MobGroup[self.nombre] = self

        self._sprSombra = None  # dumyval

    def establecer_estado(self, estado):
        self.estado = estado
        if estado == 'idle':
            self.images = self.idle_walk_img
            self.mascaras = self.idle_walk_alpha

        elif estado == 'cmb':
            self.images = self.cmb_walk_img
            self.mascaras = self.cmb_walk_alpha

    def recibir_danio(self, danio):
        self.salud_act -= danio

        if self.salud_act <= 0:
            if self.death_img is not None:
                self.image = self.death_img
            else:
                # esto queda hasta que haga sprites 'muertos' de los npcs
                # pero necesito más resolución para hacerlos...
                self.stage.del_property(self)
                self.stage.del_property(self._sprSombra)
            self.dead = True
            del MobGroup[self.nombre]
