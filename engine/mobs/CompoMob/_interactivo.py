from engine.globs import MobGroup, ItemGroup
from ._atribuido import Atribuido
from pygame import Rect


class Interactivo(Atribuido):
    # el nombre no es del todo correcto, pero no existe palabra en castellano
    # para lo que sería un interactuante. Al menos, el dRAE dice que no existe.
    idx_quadrant = 0

    def __init__(self, *args, **kwargs):
        self._interaction_rect = Rect((0, 0), (32, 32))
        super().__init__(*args, **kwargs)

    def _aling_interaction_rect(self, x, y):
        """Alinea el rect de interacción. Función simplificada."""

        if x < 0:
            self._interaction_rect.right = self.mapRect.centerx
        elif x > 0:
            self._interaction_rect.left = self.mapRect.centerx
        else:
            self._interaction_rect.x = self.mapRect.x

        if y < 0:
            self._interaction_rect.bottom = self.mapRect.centery
        elif y > 0:
            self._interaction_rect.top = self.mapRect.centery
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
        if item in MobGroup:
            return item

    def quadrant_interaction(self, x, y):
        self._aling_interaction_rect(x, y)
        cuadrante = self.stage.cuadrantes[self.idx_quadrant]
        # if not cuadrante.rect.contains(self._interaction_rect):
        #     dx, dy = self.idx_quadrant // 2, self.idx_quadrant % 2
        #     idx = (dy + y) * 2 + (dx + x)
        #     cdr = self.stage.cuadrantes[idx]
        #     print('contains2', cdr.rect.colliderect(self._interaction_rect), idx)
        #     if self.direccion == 'arriba':
        #         print('topleft', cdr.rect.collidepoint(self._interaction_rect.topleft))
        #         print('topright', cdr.rect.collidepoint(self._interaction_rect.topright))
        #     elif self.direccion == 'abajo':
        #         print('bottomleft', cdr.rect.collidepoint(self._interaction_rect.bottomleft))
        #         print('bottomright', cdr.rect.collidepoint(self._interaction_rect.bottomright))
        #     elif self.direccion == 'derecha':
        #         print('topleft', cdr.rect.collidepoint(self._interaction_rect.topleft))
        #         print('bottomleft', cdr.rect.collidepoint(self._interaction_rect.bottomleft))
        #     elif self.direccion == 'izquierda':
        #         print('topright', cdr.rect.collidepoint(self._interaction_rect.topright))
        #         print('bottomright', cdr.rect.collidepoint(self._interaction_rect.bottomright))
        for item in cuadrante:
            if item is not self:

                # los sprites deberian tener un "mapRect" completo.
                if self._interaction_rect.colliderect(item.mapRect):
                    if item.tipo == 'Mob':
                        return self._interact_with_mobs(item)
                    else:
                        return self._interact_with_props(item)
