from pygame.sprite import Sprite, LayeredUpdates
# noinspection PyUnresolvedReferences
from math import sin, cos, radians
from engine.globs.event_aware import EventAware


class BaseElement(Sprite):
    selected = False
    in_place = False
    delta = 0
    puntos = None
    stop = False
    cascada = []
    angle = 0
    image = None
    rect = None
    img_uns = None
    img_sel = None
    rect_sel = None
    rect_uns = None

    def __init__(self, parent, nombre):
        self.cascada = []
        super().__init__()
        self.parent = parent
        self.nombre = nombre
        self.check_placement()

    def __repr__(self):
        return self.nombre

    def change_angle(self, angle, centerx, centery):
        self.angle = angle
        self.rect.center = centerx, centery

    def check_placement(self):
        if self.angle == 0:
            self.in_place = True
        else:
            self.in_place = False

        return self.in_place

    def circular(self, delta):
        self.angle += delta
        if self.angle > 359:
            self.angle = 0
        elif self.angle < 0:
            self.angle += 360

    def select(self):
        self.image = self.img_sel
        self.rect = self.rect_sel
        self.selected = True

    def deselect(self):
        self.image = self.img_uns
        self.rect = self.rect_uns
        self.selected = False

    def do_action(self):
        pass

    def update(self):
        self.circular(self.delta)
        self.rect_sel.center = self.parent.puntos[self.angle]
        self.rect_uns.center = self.parent.puntos[self.angle]

        if self.check_placement():
            self.parent.actual = self
            if self.stop:
                self.select()
                self.parent.stop_everything(self)
                self.stop = False
        else:
            self.deselect()


class CircularMenu (EventAware):
    cubos = None  # cascada actualmente visible
    cascadaActual = 'inicial'
    cascadaAnterior = ''
    stopped = True
    hold = False
    actual = None
    radius = 8
    cascadas = {}
    puntos = None
    center = 0, 0

    def __init__(self, cascadas, centerx, centery):
        self.cubos = LayeredUpdates()
        self.cascadas = {}
        self.center = centerx, centery
        self.puntos = None

        for key in cascadas:
            grupo = cascadas[key]
            if len(grupo) > 0:
                radius = self.radius * (len(grupo) + 1)
                puntos = [self.get_xy(a, radius, centerx, centery) for a in range(-90, 270)]
                separacion = 360 // len(grupo)
                angle = -separacion
                for item in grupo:
                    angle += separacion
                    item.change_angle(angle, *puntos[angle])
                    # item.puntos = puntos
                self.cascadas[key] = {'items': cascadas[key], 'radius': radius, 'puntos': puntos}

        self.cubos.add(*self.cascadas['inicial']['items'])
        self.change_radius(self.radius)

        super().__init__()
        self.functions['tap'].update({
            'accion': self.accept,
            'contextual': self.back,
            'izquierda': self.stop,
            'derecha': self.stop})

        self.functions['hold'].update({
            'izquierda': lambda: self.turn(-1),
            'derecha': lambda: self.turn(+1)})

        self.functions['release'].update({
            'izquierda': self.stop,
            'derecha': self.stop})

    def change_radius(self, x):
        radius = x * (len(self.cascadas[self.cascadaActual]) + 1)
        self.puntos = [self.get_xy(a, radius, *self.center) for a in range(-90, 270)]

    @staticmethod
    def get_xy(angle, radius, centerx, centery):
        x = round(centerx + radius * cos(radians(angle)))
        y = round(centery + radius * sin(radians(angle)))
        return x, y

    def turn(self, delta):  # +1 o -1
        for cubo in self.cubos:
            cubo.stop = False
            cubo.delta = delta * 3
            # cubo.puntos = self.cascadas[self.cascadaActual]['puntos']
        self.stopped = False

    def stop(self):
        for cubo in self.cubos:
            cubo.stop = True

    def stop_everything(self, on_spot):
        cubos = self.cubos.sprites()
        angle = 360 // len(cubos)  # base

        i = -1
        for cubo in sorted(cubos, key=lambda c: c.angle):
            i += 1
            if cubo is not on_spot:
                cubo.angle = angle * i
            cubo.delta = 0
        self.stopped = True

    def accept(self):
        if self.stopped:
            if self.actual.nombre in self.cascadas:
                self.cascadaAnterior = self.cascadaActual
                self.cascadaActual = self.actual.nombre
                self._change_cube_list()

            elif not self.actual.do_action():
                self.supress_one()
                self.actual = None

                if not len(self.cascadas[self.cascadaActual]['items']):
                    del self.cascadas[self.cascadaActual]
                    self.back()
                else:
                    self._modify_cube_list()

    def back(self):
        if self.stopped and self.cascadaAnterior != '':
            self.cascadaActual = self.cascadaAnterior
            self.cascadaAnterior = ''
            self._change_cube_list()

    def add_element(self, cascada, item):
        if cascada in self.cascadas:
            self.cascadas[cascada]['items'].append(item)
        else:
            raise NotImplementedError('No se pueden agregar nuevas cascadas de momento')

        self._change_cube_list()
        self._modify_cube_list()

    def supress_one(self):
        self.cubos.remove(self.actual)
        self.cascadas[self.cascadaActual]['items'].remove(self.actual)

    def supress_all(self):
        self.cubos.empty()
        self.cascadas[self.cascadaActual]['items'].clear()

    def _change_cube_list(self):
        self.cubos.empty()
        self.cubos.add(*self.cascadas[self.cascadaActual]['items'])

    def _modify_cube_list(self):
        self.change_radius(self.radius)
        separacion = 360 // len(self.cubos)
        angulo = -separacion  # 0°
        for cuadro in self.cubos:
            angulo += separacion
            cuadro.change_angle(angulo, *self.puntos[angulo])

    def check_on_spot(self):
        for cuadro in self.cubos:
            if cuadro.in_place:
                return cuadro
