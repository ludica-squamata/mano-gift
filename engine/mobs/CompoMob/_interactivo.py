from engine.globs import Mob_Group
from ._atribuido import Atribuido
from pygame import Rect


class Interactivo(Atribuido):
    idx_quadrant = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._vertical = Rect((0, 0), (32, 16))
        self._horizontal = Rect((0, 0), (16, 32))
        self._interaction_rect = None

    def _aling_interaction_rect(self, x, y):
        """Alinea el rect de interacción. Función simplificada."""
        if x != 0:
            self._interaction_rect = self._horizontal.copy()
        elif y != 0:
            self._interaction_rect = self._vertical.copy()

        if x < 0:
            self._interaction_rect.right = self.mapRect.centerx
        elif x > 0:
            self._interaction_rect.left = self.mapRect.centerx
        else:
            self._interaction_rect.x = self.mapRect.x

        if y < 0:
            self._interaction_rect.bottom = self.mapRect.top
        elif y > 0:
            self._interaction_rect.top = self.mapRect.bottom
        else:
            self._interaction_rect.y = self.mapRect.y

    @staticmethod
    def _interact_with_props(item):
        """Selecciona a un prop utilizando el rect de interacción"""
        if item.image is not None:
            return item

    @staticmethod
    def _interact_with_mobs(item):
        """Selecciona a un mob utilizando el rect de interacción"""
        if item in Mob_Group:
            return item

    def sprite_interaction(self):
        x, y = self.direcciones[self.direccion]
        self._aling_interaction_rect(x, y)
        lista = self.stage.properties.sprites()
        idx = lista.index(self)
        for item in lista[0:idx]+lista[idx+1:]:
            if self._interaction_rect.colliderect(item.mapRect):
                if item.tipo == 'Mob':
                    return self._interact_with_mobs(item)
                else:
                    return self._interact_with_props(item)
