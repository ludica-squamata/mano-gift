from .CompoMob import Equipado, Combativo, Autonomo, Parlante
from engine.globs import Mob_Group, ModData
from engine.misc import cargar_imagen, split_spritesheet
from engine.base import ShadowSprite
from engine.globs.event_dispatcher import EventDispatcher


class Mob(Combativo, Equipado, Autonomo, Parlante, ShadowSprite):
    accionable = False
    character_name = ''
    has_hud = False  # by default, non-controlled mobs don't have a HUD.

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
                    self.death_img = cargar_imagen(ModData.graphs + imgs['death'])
                elif key == "diag_face":
                    self.diag_face = split_spritesheet(ModData.graphs + imgs['diag_face'], w=89, h=89)

        self.images = self.idle_walk_img
        self.nombre = data['nombre']
        self.estado = 'idle'
        image = self.images['S' + self.direccion]
        mask = self.mascaras['S' + self.direccion]
        super().__init__(data, imagen=image, x=x, y=y, alpha=mask, center=focus)

        if self.nombre not in Mob_Group:
            Mob_Group[self.nombre] = self

        EventDispatcher.register(self.rotate_and_pos, 'RotateMobs')

    def rotate_and_pos(self, event):
        x = event.data['x']
        y = event.data['y']

        self.mapRect.center = x, y

    def __repr__(self):
        return "Mob " + self.nombre
