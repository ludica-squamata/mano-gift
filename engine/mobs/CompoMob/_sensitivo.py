from math import tan, radians
from pygame import Surface, draw, mask, transform
from engine.globs import Mob_Group
from ._atribuido import Atribuido


class Sensitivo(Atribuido):
    vision = None  # triangulo o circulo de la visión.
    audicion = None
    vx, vy = 0, 0  # posicion de la visión, puesta acá por si el mob no se mueve
    ultima_direccion = ''
    vis_mask = None

    # mover_vis = None #algoritmo para desplazar la visión junto al mob

    def __init__(self, data, **kwargs):
        print('sensitivo')
        super().__init__(data, **kwargs)
        self.tri_vis = self._generar_cono(32 * 5)  # (data[vision])
        self.cir_vis = self._generar_circulo_sensorioal(32 * 6)  # (data[vision])
        self.audicion = self._generar_circulo_sensorioal(32 * 6)  # cheat
        self.vision = 'cono'
        self._mover_vis = self._mover_triangulo_visual

    @staticmethod
    def _generar_cono(largo):
        """Crea el triangulo de la visión (fg azul, bg transparente).

        Devuelve un surface."""

        def _ancho(_largo):
            an = radians(40)
            return round(_largo * round(tan(an), 2))

        ancho = _ancho(largo)

        megasurf = Surface((ancho * 2, largo))
        draw.polygon(megasurf, (0, 0, 255), [[0, 0], [ancho, largo], [ancho * 2, 0]])
        megasurf.set_colorkey((0, 0, 0))

        return megasurf

    @staticmethod
    def _generar_circulo_sensorioal(radio):
        """crea un circulo sensorioal, que se usa para que el mob
        detecte otros mobs y objetos"""

        surf = Surface((radio * 2, radio * 2))
        draw.circle(surf, (0, 0, 255), [radio, radio], radio, 0)
        surf.set_colorkey((0, 0, 0))
        return surf

    def _mover_triangulo_visual(self, direccion):
        """Gira el triangulo de la visión.

        Devuelve el surface del triangulo rotado, y la posicion en x e y"""
        tx, ty, tw, th = self.mapRect
        img = self.tri_vis
        if direccion == 'abajo':
            surf = transform.flip(img, False, True)
            w, h = surf.get_size()
            y = ty + th
            x = tx + (tw / 2) - w / 2
        elif direccion == 'derecha':
            surf = transform.rotate(img, -90.0)
            w, h = surf.get_size()
            x = tx + tw
            y = ty + (th / 2) - h / 2
        elif direccion == 'izquierda':
            surf = transform.rotate(img, +90.0)
            w, h = surf.get_size()
            x = tx - w
            y = ty + (th / 2) - h / 2
        else:
            surf = img
            w, h = surf.get_size()
            y = ty - h
            x = tx + (tw / 2) - w / 2

        self.vx, self.vy = int(x), int(y)
        self.vis_mask = mask.from_surface(surf)

    def _mover_circulo_visual(self, dummy=None):
        if self.vision == 'cono':
            self._mover_triangulo_visual(dummy)
        elif self.vision == 'circulo':
            self._mover_circulo_sensorial(self.cir_vis)

    def _mover_circulo_sensorial(self, sentido):
        """Si la visión es circular, entonces se usa esta función
        para moverla. El argumento dummy viene a ser la direccion,
        pero como no hay que girar el circulo, es indistinta."""

        tx, ty, tw, th = self.mapRect
        w, h = sentido.get_size()
        x = int(tx + (tw / 2) - (w / 2))
        y = int(ty + (th / 2) - (h / 2))

        self.vx, self.vy = x, y
        self.vis_mask = mask.from_surface(sentido)

    def ver(self):
        """Realiza detecciones con la visión del mob"""
        detected = []
        direccion = self.direccion
        if direccion == 'ninguna':
            direccion = self.ultima_direccion
        else:
            self.ultima_direccion = self.direccion

        self._mover_vis(direccion)
        mob = None
        for mob in Mob_Group:
            if mob != self:
                x, y = self.vx - mob.mapX, self.vy - mob.mapY
                if mob.mask.overlap(self.vis_mask, (x, y)):
                    detected.append(mob)

        for obj in self.stage.interactives:
            x, y = self.vx - obj.mapX, self.vy - obj.mapY
            if mob.mask.overlap(self.vis_mask, (x, y)):
                detected.append(obj)

        return detected

    def oir(self):
        detected = []
        self._mover_circulo_sensorial(self.audicion)
        for mob in Mob_Group:
            if mob != self:
                x, y = self.vx - mob.mapX, self.vy - mob.mapY
                if mob.mask.overlap(self.vis_mask, (x, y)) and mob.moviendose:
                    detected.append(mob)

                    # for obj in self.stage.interactives:
                    # x,y = self.vx-obj.mapX, self.vy-obj.mapY
                    # if mob.mask.overlap(self.vis_mask,(x,y)):
                    # detected.append(obj)

        return detected
