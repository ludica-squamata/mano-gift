from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import GRUPO_MOVIBLES, GRUPO_MOBS, Item_Group
from engine.scenery.props import Movible
from ._caracterizado import Caracterizado


class Movil(Caracterizado):
    moviendose = False

    def cambiar_direccion(self, direccion=None):
        self.direccion = direccion
        self.image = self.images['S' + self.direccion]

    # noinspection PyMethodOverriding
    def mover(self):
        self.moviendose = True
        dx, dy = super().mover(*self.direcciones[self.direccion])
        self.reubicar(dx, dy)
        EventDispatcher.trigger('SoundEvent', self, {'type': 'movement', 'volume': 1})

    def atacar(self, sprite):
        # 'sprite' es agregado para mantener la firma
        # cuestiones de PyCharm.
        return not self.moviendose

    def detectar_colisiones(self):
        dx, dy = super().mover(*self.direcciones[self.direccion])
        col_mobs = False  # colision contra otros mobs
        col_props = False  # colision contra los props
        col_mapa = False  # colision contra las cajas de colision del propio mapa

        if self.solido:
            if self.stage.mask.overlap(self.mask, (self.mapRect.x + dx, self.mapRect.y)) is not None:
                col_mapa = True

            if self.stage.mask.overlap(self.mask, (self.mapRect.x, self.mapRect.y + dy)) is not None:
                col_mapa = True

            for spr in Item_Group.get_from_layer(GRUPO_MOVIBLES):
                if self.colisiona(spr, dx, dy):
                    if spr.solido:
                        if isinstance(spr, Movible):
                            if not spr.mover(dx, dy):
                                col_props = True
                        else:
                            col_props = True

            for spr in self.mapa_actual.properties.get_sprites_from_layer(GRUPO_MOBS):
                if spr.solido and self is not spr:
                    if self.colisiona(spr, dx, dy):
                        col_mobs = True

        if self.stage.mascara_salidas.overlap(self.mask, (self.mapRect.x + dx, self.mapRect.y + dy)) is not None:
            r, g, b, a = self.stage.imagen_salidas.get_at((self.mapRect.x + dx, self.mapRect.y + dy))
            self.stage.salidas[b * 255 + g].trigger(self)

        return any([col_mobs, col_props, col_mapa])

    def detener_movimiento(self):
        self.moviendose = False
