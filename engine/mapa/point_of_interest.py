from pygame import mask, font, Surface, SRCALPHA
from engine.mobs.scripts.a_star import Nodo
from engine.globs.renderer import Camara
from engine.base import AzoeSprite
from engine.globs import ModData
import sys


class PointOfInterest(AzoeSprite):
    tipo = 'nodo'
    prop_type = 'None'

    def __init__(self, parent, data):
        self.name = data['name']
        x, y, size = data['node']
        self.nodo = Nodo(x, y, tuple(parent.adress))
        imagen = self._create()
        rect = imagen.get_rect(center=[x, y])
        mascara = mask.Mask([size, size], fill=True)
        super().__init__(parent, imagen=imagen, x=rect.centerx, y=rect.centery, z=5000, alpha=mascara)
        self.id = data.get('id', ModData.next_id(data.get('prefix',"Salida")))
        if 'pydevd' in sys.modules:
            parent.add_property(self, 10000)

    @staticmethod
    def _create():
        fuente = font.Font('engine/libs/Verdanab.ttf', 30)
        render = fuente.render('!', True, (255, 215, 0))
        imagen = Surface([32,32], SRCALPHA)
        r_rect = render.get_rect(center=[16,14])
        imagen.blit(render, r_rect)
        return imagen

    def erase(self):
        self.kill()

    def __repr__(self):
        return f'PointOfInterest "{self.name}"'

    def on_elimination(self):
        super().on_elimination()
        Camara.remove_obj(self)
        self.parent = None