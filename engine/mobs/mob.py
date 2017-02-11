from .CompoMob import Equipado, Animado, Interactivo
from engine.globs import MobGroup
from engine.misc import Resources as Rs
from engine.base import ShadowSprite
from engine.globs.eventDispatcher import EventDispatcher


class Mob(Interactivo, Equipado, ShadowSprite, Animado):  # Movil es Atribuido para tener .velocidad
    hablante = False
    mana = 1

    idle_walk_img = {}  # imagenes normales
    idle_walk_alpha = {}

    def __init__(self, data, x, y, focus=False):
        self.tipo = "Mob"
        self.images = {}
        self.mascaras = {}
        self.data = data

        self.functions = {
            'tap': {},
            'hold': {},
            'release': {}
        }

        dirs = ['S', 'L', 'R']
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
        self.ID = data['ID']
        self.nombre = data['nombre']

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
        image = self.images['S'+self.direccion]
        mask = self.mascaras['S'+self.direccion]
        super().__init__(imagen=image, alpha=mask, x=x, y=y, center=focus)

        if self.nombre not in MobGroup:
            MobGroup[self.nombre] = self

        EventDispatcher.register(self.rotate_and_pos, 'Rotar_mobs')

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
        EventDispatcher.trigger('MobHerido', self.tipo, {'mob': self})

        if self.salud_act <= 0:
            if self.death_img is not None:
                self.image = self.death_img
                # esto queda hasta que haga sprites 'muertos' de los npcs
                # pero necesito más resolución para hacerlos...
            self.dead = True
            EventDispatcher.trigger('MobMuerto', self.tipo, {'obj': self})

    def rotate_and_pos(self, event):
        x = event.data['x']
        y = event.data['y']

        self.mapRect.center = x, y
