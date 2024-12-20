from engine.misc import cargar_imagen, split_spritesheet, cargar_head_anims
from .CompoMob import Combativo, Autonomo, Parlante, Comerciante
from engine.globs import Mob_Group, ModData
from engine.base import ShadowSprite


class Mob(Combativo, Autonomo, Parlante, Comerciante, ShadowSprite):
    accionable = False
    character_name = ''
    has_hud = False  # by default, non-controlled mobs don't have a HUD.

    def __init__(self, parent, x, y, data, focus=False):
        self.tipo = "Mob"
        self.images = {}
        self.mascaras = {}
        self.data = data

        dirs, atk = ['S', 'L', 'R'], ['A', 'B', 'C']
        imgs = data['imagenes']
        g = ModData.graphs
        heads = g + imgs.pop('heads')
        for key in imgs:
            if imgs[key] is not None:
                if key == 'idle':
                    self.idle_walk_img = cargar_head_anims(heads, g + imgs[key], dirs)  # request='front'
                    self.idle_left_img = cargar_head_anims(heads, g + imgs[key], dirs, request='left')
                    self.idle_right_img = cargar_head_anims(heads, g + imgs[key], dirs, request='right')
                    self.mascaras = self.cargar_alpha(data['alpha'], dirs)
                elif key == 'atk':
                    self.cmb_atk_img = cargar_head_anims(heads, g + imgs[key], atk)
                    self.atk_left_img = cargar_head_anims(heads, g + imgs[key], atk, request='left')
                    self.atk_right_img = cargar_head_anims(heads, g + imgs[key], atk, request='right')
                elif key == 'cmb':
                    self.cmb_walk_img = cargar_head_anims(heads, g + imgs[key], dirs)
                    self.cmb_left_img = cargar_head_anims(heads, g + imgs[key], dirs, request='left')
                    self.cmb_right_img = cargar_head_anims(heads, g + imgs[key], dirs, request='right')
                elif key == 'death':
                    self.death_img = cargar_imagen(g + imgs['death'])
                elif key == "diag_face":
                    self.diag_face = split_spritesheet(g + imgs['diag_face'], w=89, h=89)

        self.images = self.idle_walk_img
        self.heads = {'front': self.idle_walk_img,
                      'right': self.idle_left_img,
                      'left': self.idle_right_img}
        self.nombre = data['nombre']
        self.estado = 'idle'
        image = self.images['S' + self.direccion]
        mask = self.mascaras['S' + self.direccion]
        super().__init__(parent, data, imagen=image, x=x, y=y, alpha=mask, center=focus, id=data.get('id', None))
        self.chunk_adresses = {self.parent.parent.nombre: self.parent.adress.center}
        if self.id not in Mob_Group:
            Mob_Group[self.id] = self

    def __repr__(self):
        return "Mob " + self.nombre

    def __str__(self):
        return self.nombre
