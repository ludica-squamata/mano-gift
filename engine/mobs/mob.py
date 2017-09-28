from .CompoMob import Equipado, Combativo, Autonomo, Parlante
from engine.globs import Mob_Group
from engine.misc import cargar_imagen
from engine.base import ShadowSprite
from engine.globs.eventDispatcher import EventDispatcher


class Mob(Combativo, Equipado, Autonomo, Parlante, ShadowSprite):

    def __init__(self, x, y, data, focus=False):
        self.tipo = "Mob"
        self.images = {}
        self.mascaras = {}
        self.data = data

        dirs = ['S', 'L', 'R']
        imgs = data['imagenes']
        for key in imgs:
            if imgs[key] is not None:
                if key == 'idle':
                    self.idle_walk_img = self.cargar_anims(imgs['idle'], dirs)
                    self.mascaras = self.cargar_anims(data['alpha'], dirs, True)
                elif key == 'atk':
                    self.cmb_atk_img = self.cargar_anims(imgs['atk'], ['A', 'B', 'C'])
                elif key == 'cmb':
                    self.cmb_walk_img = self.cargar_anims(imgs['cmb'], dirs)
                elif key == 'death':
                    self.death_img = cargar_imagen(imgs['death'])
                elif key == "diag_face":
                    self.diag_face = cargar_imagen(imgs["diag_face"])

        self.images = self.idle_walk_img
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
        super().__init__(data, imagen=image, x=x, y=y, alpha=mask, center=focus)

        if self.nombre not in Mob_Group:
            Mob_Group[self.nombre] = self

        EventDispatcher.register(self.rotate_and_pos, 'RotateMobs')

    def rotate_and_pos(self, event):
        x = event.data['x']
        y = event.data['y']

        self.mapRect.center = x, y
