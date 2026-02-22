from engine.mobs.scripts.a_star import Nodo
from engine.base import AzoeSprite
from pygame import mask, font


class PointOfInterest(AzoeSprite):
    tipo = 'nodo'
    prop_type = 'None'

    def __init__(self, parent, data):
        self.name = data['name']
        x, y, size = data['node']
        self.nodo = Nodo(x, y, size)
        mascara = mask.Mask([size, size], fill=True)
        super().__init__(parent, imagen=self._create(), x=x, y=y, z=5000, alpha=mascara)

    @staticmethod
    def _create():
        fuente = font.SysFont('Verdanab', 30)
        render = fuente.render('!', True, (255, 215, 0))
        return render

    def erase(self):
        self.kill()

    def __repr__(self):
        return f'PointOfInterest "{self.name}"'