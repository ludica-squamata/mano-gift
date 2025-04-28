from engine.misc import cargar_imagen, split_spritesheet, cargar_head_anims
from .CompoMob import Combativo, Autonomo, Parlante, Comerciante
from engine.globs import Mob_Group, ModData
from engine.base import ShadowSprite


class Mob(Combativo, Autonomo, Parlante, Comerciante, ShadowSprite):
    accionable = False
    character_name = ''  # issue-156: this is only for the hero and should be eliminated.
    has_hud = False  # by default, non-controlled mobs don't have a HUD.
    race = None  # for now, "human" or "blob". This tag allow the engine to select a mob by it's "class".

    def __init__(self, parent, x, y, data, focus=False):
        self.tipo = "Mob"
        self.images = {}
        self.mascaras = {}
        self.data = data

        dirs, atk = ['S', 'L', 'R'], ['A', 'B', 'C']
        imgs = data['imagenes']
        g = ModData.graphs
        heads = g + imgs.pop('heads') if 'heads' in imgs else None
        for key in imgs:
            method, params = None, []
            if imgs[key] is not None and heads is not None:  # este framento es para los mobs con cabeza.
                method = cargar_head_anims
                params = [heads, g + imgs[key], dirs if key != 'atk' else atk]
            elif heads is None:  # este otro es para los mobs que no diferencian su cueerpo de su cabeza.
                method = self.cargar_anims
                params = imgs[key], dirs if key != 'atk' else atk
            if method is not None and len(params):
                if key == 'idle':
                    self.idle_walk_img = method(*params)  # request='front'
                    self.idle_left_img = method(*params, request='left')
                    self.idle_right_img = method(*params, request='right')
                    self.mascaras = self.cargar_alpha(data['alpha'], dirs)
                elif key == 'atk':
                    self.cmb_atk_img = method(*params)
                    self.atk_left_img = method(*params, request='left')
                    self.atk_right_img = method(*params, request='right')
                elif key == 'cmb':
                    self.cmb_walk_img = method(*params)
                    self.cmb_left_img = method(*params, request='left')
                    self.cmb_right_img = method(*params, request='right')
                elif key == 'death':
                    self.death_img = cargar_imagen(g + imgs['death'])
                elif key == "diag_face":
                    self.diag_face = split_spritesheet(g + imgs['diag_face'], w=89, h=89)

        self.images = self.idle_walk_img
        self.heads = {'front': self.idle_walk_img,
                      'right': self.idle_left_img,
                      'left': self.idle_right_img}
        self.nombre = data['nombre']  # issue-156
        self.estado = 'idle'
        image = self.images['S' + self.direccion]
        mask = self.mascaras['S' + self.direccion]
        super().__init__(parent, data, imagen=image, x=x, y=y, alpha=mask, center=focus, id=data.get('id', None))
        self['nombre'] = data['nombre']  # nombre y raza se añaden al mob vía Caracterizado.__setitem__()
        self['raza'] = data.get('raza', 'human')
        self.chunk_adresses = {self.parent.parent.nombre: self.parent.adress.center}
        if self.id not in Mob_Group:
            Mob_Group[self.id] = self
        if 'occupation' in data:
            self['occupation'] = data['occupation']  # issue-156

    def __repr__(self):
        return f"Mob {self['nombre']}"  # issue-156

    def __str__(self):
        return self.nombre  # issue-156
