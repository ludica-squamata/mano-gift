from engine.globs import Constants as C
from engine.scenery.props import Movible
from ._atribuido import Atribuido


class Movil(Atribuido):
    modo_colision = None  # determina qué direccion tomará el mob al chocar con algo

    def cambiar_direccion(self, arg, img=False):
        direccion = 'ninguna'

        if arg == 'contraria':
            if self.direccion == 'arriba':
                direccion = 'abajo'
            elif self.direccion == 'abajo':
                direccion = 'arriba'
            elif self.direccion == 'izquierda':
                direccion = 'derecha'
            elif self.direccion == 'derecha':
                direccion = 'izquierda'

        elif arg in self.direcciones:
            direccion = arg

        self.direccion = direccion
        if img:  # solo vale para el héroe...
            self.image = self.images['S' + self.direccion]
            if direccion == self.direccion:
                self.mover(*self.direcciones[direccion])

        return direccion

    def mover(self, x, y):
        dx, dy = x * self.velocidad, y * self.velocidad

        if self.detectar_colisiones(dx, dy):
            #en realidad, esto es territorio de la AI, asi que debería hacer super()
            self.cambiar_direccion(self.modo_colision)
            x, y = self.direcciones[self.direccion]
            dx, dy = x * self.velocidad, y * self.velocidad

        self.reubicar(dx, dy)

    def detectar_colisiones(self, dx, dy):
        col_bordes = False  # colision contra los bordes de la pantalla
        col_mobs = False  # colision contra otros mobs
        col_props = False  # colision contra los props
        col_mapa = False  # colision contra las cajas de colision del propio mapa

        if self.solido:
            if self.stage.mapa.mask.overlap(self.mask, (self.mapX + dx, self.mapY)) is not None:
                col_mapa = True

            if self.stage.mapa.mask.overlap(self.mask, (self.mapX, self.mapY + dy)) is not None:
                col_mapa = True

            for spr in self.stage.properties.get_sprites_from_layer(C.GRUPO_ITEMS):
                if self.colisiona(spr, dx, dy):
                    if spr.solido:
                        if isinstance(spr,Movible):
                            spr.reubicar(dx, dy)
                        else:
                            col_props = True

            for spr in self.stage.properties.get_sprites_from_layer(C.GRUPO_MOBS):
                if spr.solido and self is not spr:                        
                    if self.colisiona(spr, dx, dy):
                        col_mobs = True
        
        new_posX = self.stageX+dx
        new_posY = self.stageY+dy
        w = self.stage.rect.w-self.rect.w
        h = self.stage.rect.h-self.rect.h
        
        if 0 > new_posX or new_posX > w or 0 > new_posY or new_posY > h:
            col_bordes = True
        
        return any([col_bordes, col_mobs, col_props, col_mapa])
