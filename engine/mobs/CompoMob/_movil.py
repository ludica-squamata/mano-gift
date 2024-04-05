from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import GRUPO_MOBS, Tagged_Items
from engine.scenery.props import Movible
from engine.globs.renderer import Camara
from ._caracterizado import Caracterizado


class Movil(Caracterizado):
    moviendose = False

    def cambiar_direccion(self, direccion=None):
        self.direccion = direccion

    def mover(self, dx=0, dy=0):
        # 'dx' y 'dy' son agregados para mantener la firma
        # cuestiones de PyCharm.
        self.moviendose = True
        dx, dy = super().mover(dx, dy)
        self.reubicar(dx, dy)
        EventDispatcher.trigger('SoundEvent', self, {'type': 'movement', 'intensity': 40})

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
            if Camara.current_map.mask.overlap(self.mask, (self.x + dx, self.y)) is not None:
                col_mapa = True

            if Camara.current_map.mask.overlap(self.mask, (self.x, self.y + dy)) is not None:
                col_mapa = True

            for spr in Tagged_Items.intersect('movibles', 'solido'):
                if self.colisiona(spr, dx, dy):
                    if spr.solido:
                        col_props = True
                        if isinstance(spr, Movible):
                            if spr.mover(dx, dy):
                                col_props = False

            for spr in Camara.current_map.properties.get_sprites_from_layer(GRUPO_MOBS):
                if spr.solido and self is not spr:
                    if self.colisiona(spr, dx, dy):
                        col_mobs = True

        if Camara.current_map.mascara_salidas.overlap(self.mask, (self.rel_x + dx, self.rel_y + dy)) is not None:
            r, g, b, a = Camara.current_map.imagen_salidas.get_at((self.rel_x + dx, self.rel_y + dy))
            Camara.current_map.salidas[b * 255 + g].trigger(self)

        return any([col_mobs, col_props, col_mapa])

    def detener_movimiento(self):
        self.moviendose = False
