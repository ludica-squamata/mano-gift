from engine.globs import GRUPO_ITEMS, GRUPO_MOBS
from engine.scenery.props import Movible
from ._atribuido import Atribuido


class Movil(Atribuido):
    moviendose = False

    def __init__(self, *args, **kwargs):
        print('movil')
        super().__init__(*args, **kwargs)
        if hasattr(self, 'functions'):
            self.functions['tap'].update({
                'arriba': lambda: self.cambiar_direccion('arriba'),
                'abajo': lambda: self.cambiar_direccion('abajo'),
                'izquierda': lambda: self.cambiar_direccion('izquierda'),
                'derecha': lambda: self.cambiar_direccion('derecha')
            })
            self.functions['hold'].update({
                'arriba': lambda: self.mover('arriba'),
                'abajo': lambda: self.mover('abajo'),
                'izquierda': lambda: self.mover('izquierda'),
                'derecha': lambda: self.mover('derecha')
            })
            self.functions['release'].update({
                'arriba': self.detener_movimiento,
                'abajo': self.detener_movimiento,
                'izquierda': self.detener_movimiento,
                'derecha': self.detener_movimiento
            })

    def cambiar_direccion(self, direccion=None):
        self.direccion = direccion
        self.image = self.images['S' + self.direccion]

    # noinspection PyMethodOverriding
    def mover(self):
        self.moviendose = True
        dx, dy = super().mover(*self.direcciones[self.direccion])
        self.reubicar(dx, dy)

    def atacar(self):
        if not self.moviendose:
            return True
        else:
            return False

    def detectar_colisiones(self):
        dx, dy = super().mover(*self.direcciones[self.direccion])
        col_bordes = False  # colision contra los bordes de la pantalla
        col_mobs = False  # colision contra otros mobs
        col_props = False  # colision contra los props
        col_mapa = False  # colision contra las cajas de colision del propio mapa

        if self.solido:
            if self.stage.mapa.mask.overlap(self.mask, (self.mapRect.x + dx, self.mapRect.y)) is not None:
                col_mapa = True

            if self.stage.mapa.mask.overlap(self.mask, (self.mapRect.x, self.mapRect.y + dy)) is not None:
                col_mapa = True

            for spr in self.stage.properties.get_sprites_from_layer(GRUPO_ITEMS):
                if self.colisiona(spr, dx, dy):
                    if spr.solido:
                        if isinstance(spr, Movible):
                            if not spr.mover(dx, dy):
                                col_props = True
                        else:
                            col_props = True

            for spr in self.stage.properties.get_sprites_from_layer(GRUPO_MOBS):
                if spr.solido and self is not spr:
                    if self.colisiona(spr, dx, dy):
                        col_mobs = True

        # new_posX = self.stageX+dx
        # new_posY = self.stageY+dy
        # w = self.stage.rect.w-self.rect.w
        # h = self.stage.rect.h-self.rect.h
        #
        # if 0 > new_posX or new_posX > w or 0 > new_posY or new_posY > h:
        #     col_bordes = True

        return any([col_bordes, col_mobs, col_props, col_mapa])

    def detener_movimiento(self):
        self.moviendose = False
