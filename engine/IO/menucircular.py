﻿from pygame.sprite import Sprite, LayeredUpdates
from math import sin, cos, radians


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
        self.check_placement()
        if self.angle > 359:
            self.angle = 0
        elif self.angle < 0:
            self.angle += 359

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
        self.rect_sel.center = self.puntos[self.angle]
        self.rect_uns.center = self.puntos[self.angle]

        if self.check_placement():
            self.select()
            self.parent.actual = self
            if self.stop:
                self.parent.stop_everything(self)
        else:
            self.deselect()


class CircularMenu:
    cubos = None  # cascada actualmente visible
    cascadaActual = 'inicial'
    cascadaAnterior = ''
    stopped = True
    hold = False
    actual = None
    di = 0
    radius = 8
    cascadas = {}

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
                    item.puntos = puntos
                self.cascadas[key] = {'items': cascadas[key], 'radius': radius, 'puntos': puntos}

        self.cubos.add(*self.cascadas['inicial']['items'])
        self.change_radius(self.radius)

        self.functions = {
            'on_keydown': {
                'izquierda': lambda: self.turn(-1),
                'derecha': lambda: self.turn(+1),
                'hablar': self.accept,
                'cancelar': self.back
            },
            'on_keyup': {
                'izquierda': self.stop,
                'derecha': self.stop
            }
        }

    def use_keydown_func(self, key):
        self.use_function('on_keydown', key)

    def use_keyup_func(self, key):
        self.use_function('on_keyup', key)

    def use_function(self, mode, key):
        if key in self.functions[mode]:
            self.functions[mode][key]()

    def change_radius(self, x):
        radius = x * (len(self.cascadas[self.cascadaActual]) + 1)
        self.puntos = [self.get_xy(a, radius, *self.center) for a in range(-90, 270)]

    @staticmethod
    def get_xy(a, radius, centerx, centery):
        x = round(centerx + radius * cos(radians(a)))
        y = round(centery + radius * sin(radians(a)))
        return x, y

    def turn(self, delta):  # +1 o -1
        for cubo in self.cubos:
            cubo.stop = False
            cubo.delta = delta * 3
            cubo.puntos = self.cascadas[self.cascadaActual]['puntos']
        self.stopped = False

    def stop(self):
        for cubo in self.cubos:
            cubo.stop = True

    def stop_everything(self, on_spot):
        for cubo in self.cubos:
            if cubo is not on_spot:
                cubo.angle = 360 // len(self.cubos)
            cubo.delta = 0
        self.stopped = True

    def accept(self):
        if self.stopped:
            if self.actual.nombre in self.cascadas:
                self.cascadaAnterior = self.cascadaActual
                self.cascadaActual = self.actual.nombre
                self._change_cube_list()

            elif not self.actual.do_action():
                self.supress()
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

    def supress(self):
        self.cubos.remove(self.actual)
        self.cascadas[self.cascadaActual]['items'].remove(self.actual)

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
