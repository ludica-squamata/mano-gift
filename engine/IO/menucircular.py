from engine.globs.azoegroup import AzoeGroup, AzoeBaseSprite
from engine.globs.event_aware import EventAware
from math import sin, cos, radians


class BaseElement(EventAware, AzoeBaseSprite):
    selected = False
    delta = 0
    stop = True
    parent = None
    command = None
    angle = 0

    img_uns = None
    img_sel = None
    rect_sel = None
    rect_uns = None

    def __init__(self, parent, nombre):
        super().__init__(parent, nombre)
        self.functions['tap'].update({
            'accion': self.do_action
        })
        self.deregister()

    def __repr__(self):
        return 'Elemento ' + self.nombre

    def check_placement(self) -> bool:
        return self.angle == 0

    def circular(self, delta: int) -> None:
        self.angle += delta
        if self.angle > 359:
            self.angle = 0
        if self.angle < 0:
            self.angle += 360

    def select(self):
        self.register()
        self.image = self.img_sel
        self.rect = self.rect_sel
        self.selected = True

    def deselect(self):
        self.deregister()
        self.image = self.img_uns
        self.rect = self.rect_uns
        self.selected = False

    def do_action(self):
        if self.command is None:
            self.parent.foward()
        elif self.check_placement():
            self.command()

    def update(self):
        self.circular(self.delta)
        self.rect_sel.center = self.parent.set_xy(self.angle)
        self.rect_uns.center = self.parent.set_xy(self.angle)

        if self.check_placement():
            self.parent.actual = self
            if self.stop:
                self.select()
                self.parent.stop_everything(self)
                self.stop = False
        else:
            self.deselect()


class CircularMenu(EventAware):
    cuadros = None
    cascadaActual = None
    stopped = True
    actual = None
    base_radius = 16
    cascadas = None
    acceso_cascadas = None
    center = 0, 0
    change_radius = True

    def __init__(self, cascadas: dict, centerx: int, centery: int):
        self.cuadros = AzoeGroup('Cuadros')
        self.cascadas = {}
        self.center = centerx, centery
        self.cascadaActual = 'inicial'
        self.acceso_cascadas = [self.cascadaActual]

        self.add_cascades(cascadas)
        if self.change_radius:
            self.radius = self.base_radius * (len(self.cascadas['inicial']) + 1)
        self.cuadros.add(*self.cascadas['inicial'])

        super().__init__()
        self.functions['tap'].update({
            'contextual': self.backward,
            'izquierda': self.stop,
            'derecha': self.stop})

        self.functions['hold'].update({
            'izquierda': lambda: self.turn(-1),
            'derecha': lambda: self.turn(+1)})

        self.functions['release'].update({
            'izquierda': self.stop,
            'derecha': self.stop})

    def set_xy(self, angle: int):
        x = round(self.center[0] + self.radius * cos(radians(angle - 90)))
        y = round(self.center[1] + self.radius * sin(radians(angle - 90)))
        return x, y

    def turn(self, delta: int):
        for cuadro in self.cuadros:
            cuadro.stop = False
            cuadro.delta = delta * 3
        self.stopped = False

    def stop(self):
        for cubo in self.cuadros:
            cubo.stop = True

    def stop_everything(self, on_spot):
        cuadros = self.cuadros.sprites()
        angle = 360 // len(cuadros)  # base

        for i, cuadro in enumerate(sorted(cuadros, key=lambda c: c.angle)):
            if cuadro is not on_spot:
                cuadro.angle = angle * i
            cuadro.delta = 0
        self.stopped = True

    def foward(self):
        if self.actual.nombre in self.cascadas and len(self.cascadas[self.actual.nombre]):
            self.cascadaActual = self.actual.nombre
            self.acceso_cascadas.append(self.cascadaActual)
            self.switch_cascades()

    def backward(self):
        if len(self.acceso_cascadas) > 1:
            del self.acceso_cascadas[-1]
            self.cascadaActual = self.acceso_cascadas[-1]
            self.switch_cascades()

    def supress_all(self):
        self.cuadros.empty()
        self.cascadas[self.cascadaActual].clear()

    def switch_cascades(self):
        for cuadro in self.cuadros:
            cuadro.deregister()
        self.cuadros.empty()
        self.cuadros.add(*self.cascadas[self.cascadaActual])

    def check_on_spot(self):
        if len(self.cuadros.sprites()):
            return min(self.cuadros.sprites(), key=lambda cuadro: cuadro.angle)

    def add_cascades(self, cascades: dict):
        for key in cascades:
            group = cascades[key]
            if key not in self.cascadas:
                self.cascadas[key] = []
            else:
                # por alguna razón no funciona con list comprehension
                for item in self.cascadas[key]:
                    if item in group:
                        group.remove(item)
                if not len(group):
                    return
                group += self.cascadas[key]
                self.cascadas[key].clear()

            if len(group):
                separation = 360 // len(group)
                angle = 0
                for e in sorted(group, key=lambda c: c.idx):
                    e.angle = angle
                    e.parent = self
                    self.cascadas[key].append(e)
                    angle += separation

    def del_cascade(self, cascade: str):
        if cascade in self.cascadas:
            del self.cascadas[cascade]

    def del_tree_recursively(self, csc: str):
        for cascade in reversed(self.acceso_cascadas[self.acceso_cascadas.index(csc):]):
            self.backward()
            self.del_cascade(cascade)
            self.del_item_from_cascade(cascade, self.acceso_cascadas[-1])  # me preocupa ese [-1]
        self.stop_everything(self.actual)

    def add_item_to_cascade(self, item, cascade: str):
        new = {cascade: [item]}
        self.add_cascades(new)
        self.radius = self.base_radius * (len(self.cascadas[cascade]) + 1)
        self.switch_cascades()

    def del_item_from_cascade(self, item_name: str, cascade: str):
        for item in self.cascadas[cascade]:
            if item_name == item.nombre:
                self.cascadas[cascade].remove(item)
                self.switch_cascades()
                break

    def __repr__(self):
        return 'Menu Circular'
