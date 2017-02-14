from .CompoMob import Equipado, Interactivo, Combativo
from engine.globs import MobGroup
from engine.misc import Resources as Rs
from engine.base import ShadowSprite
from engine.globs.eventDispatcher import EventDispatcher


class Mob(Interactivo, Equipado, ShadowSprite, Combativo):
    hablante = False
    mana = 1

    def __init__(self, data, x, y, focus=False):
        self.tipo = "Mob"
        self.images = {}
        self.mascaras = {}
        self.data = data

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

        self.estado = 'idle'
        image = self.images['S'+self.direccion]
        mask = self.mascaras['S'+self.direccion]
        super().__init__(imagen=image, alpha=mask, x=x, y=y, center=focus)

        if self.nombre not in MobGroup:
            MobGroup[self.nombre] = self

        EventDispatcher.register(self.rotate_and_pos, 'Rotar_mobs')

    def rotate_and_pos(self, event):
        x = event.data['x']
        y = event.data['y']

        self.mapRect.center = x, y
