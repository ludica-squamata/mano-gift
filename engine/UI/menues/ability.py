from engine.globs.event_dispatcher import EventDispatcher
from engine.libs.textrect import render_textrect
from engine.globs import CANVAS_BG, TEXT_FG
from engine.globs.mod_data import ModData
from engine.globs.azoe_group import AzoeGroup
from pygame import font, draw, Surface
from pygame.sprite import LayeredUpdates
from ..widgets import BaseWidget, Boton
from random import choice
from .menu import Menu

memoria = {}


class MenuAbility(Menu):
    current_counter = None
    current_idx = 0
    posicion_horizontal = 'izquierda'

    def __init__(self, parent):
        super().__init__(parent, 'Atributos', 'Atributos')

        chars = list(ModData.data['caracteristicas'].keys())
        self.counters = AzoeGroup('Counters')

        self.properties = LayeredUpdates()
        fuente = font.SysFont('Verdana', 16, bold=True)
        for i, char in enumerate(chars):
            render = fuente.render(char, True, TEXT_FG, CANVAS_BG)
            rect = render.get_rect(topleft=[6, 125 + i * 43])
            centery = rect.centery
            self.canvas.blit(render, rect)

            counter = Counter(self, char, 200, centery, 58, 22)
            if char in memoria:
                counter.value = memoria[char]
                counter.render_value()
            self.counters.add(counter)
            self.properties.add(counter)

        self.puntos = PuntosDisponibles(self, 6, 50)
        self.fin = Boton(self, 'Finalizar', 6, self.finalizar, [self.rect.centerx, self.rect.bottom - 64])
        self.random = Boton(self, 'Aleatorio', 6, self.generate_random_values, [self.rect.centerx, self.rect.top + 110])
        self.properties.add(self.fin, self.puntos, self.random)

        self.elegir_uno(0)
        self.functions['tap'].update({
            'accion': self.modificar_valor,
            'arriba': lambda: self.elegir_uno(-1),
            'abajo': lambda: self.elegir_uno(+1),
            'izquierda': lambda: self.eleccion_horizontal('izquierda'),
            'derecha': lambda: self.eleccion_horizontal('derecha')
        })
        self.functions['hold'].update({
            'accion': self.modificar_valor,
            'izquierda': lambda: self.eleccion_horizontal('izquierda'),
            'derecha': lambda: self.eleccion_horizontal('derecha')
        })

    @property
    def valores(self):
        global memoria
        vs = {}
        for counter in self.counters.sprs():
            vs[counter.char] = counter.value
            memoria[counter.char] = counter.value

        return vs

    def elegir_uno(self, delta):
        if self.posicion_horizontal != 'ninguna':
            for counter in self.counters.sprs():
                counter.deselegir()

            self.current_idx += delta
            if self.current_idx > len(self.counters) - 1:
                self.current_idx = 0
            elif self.current_idx < 0:
                self.current_idx = len(self.counters) - 1

            self.current_counter = self.counters.sprs()[self.current_idx]
            self.current_counter.elegir(self.posicion_horizontal)

        elif self.fin.enabled and delta > 0:
            self.random.ser_deselegido()
            self.fin.ser_elegido()

        elif delta < 0:
            self.fin.ser_deselegido()
            self.random.ser_elegido()

    def eleccion_horizontal(self, direccion):
        if direccion == 'derecha':
            if self.posicion_horizontal == 'izquierda':
                self.current_counter.elegir_mas()
                self.posicion_horizontal = 'derecha'
            else:
                self.posicion_horizontal = 'ninguna'
                for counter in self.counters.sprs():
                    counter.deselegir()

                if self.fin.enabled:
                    self.fin.ser_elegido()

                elif self.random.enabled:
                    self.random.ser_elegido()

        elif direccion == 'izquierda':
            if self.posicion_horizontal == 'derecha':
                self.current_counter.elegir_menos()
                self.posicion_horizontal = 'izquierda'

            elif self.posicion_horizontal == 'ninguna':
                self.fin.ser_deselegido()
                self.random.ser_deselegido()
                self.counters.sprs()[self.current_idx].elegir('derecha')
                self.posicion_horizontal = 'derecha'

    def generate_random_values(self):
        counters = self.counters.sprs()
        self.puntos.reset()
        for counter in counters:
            counter.reset()

        for counter in counters:
            if self.puntos.update_value(-1):
                counter.value += 1
                counter.render_value()

        while self.puntos.update_value(-1):
            elegido = choice(counters)
            elegido.value += 1
            elegido.render_value()

    def modificar_valor(self):
        if any(counter.isSelected for counter in self.counters.sprs()):
            for counter in self.counters.sprs():
                if counter.isSelected:
                    self.current_counter.accion()
        elif self.fin.isSelected:
            self.fin.ser_presionado()

        elif self.random.isSelected:
            self.random.ser_presionado()

    def comprobar(self):
        valido = self.puntos.value == 0
        for counter in self.counters.sprs():
            valido = valido and counter.value > 0

        return valido

    def finalizar(self):
        self.deregister()
        EventDispatcher.trigger('CharacterCreation', self.nombre, {'atributos': self.valores, 'final': False})
        EventDispatcher.trigger('OpenMenu', self.nombre, {'value': 'Name'})

    def update(self):
        if not self.comprobar():
            self.fin.ser_deshabilitado()
        elif not self.fin.enabled:
            self.fin.ser_habilitado()
        self.canvas.fill(CANVAS_BG, [6, 30, 470, 50])
        self.properties.update()
        self.properties.draw(self.canvas)


class Counter(BaseWidget):
    value = 0
    char = ''

    def __init__(self, parent, char_name, x, y, w, h):
        self.char = char_name
        self.fuente = font.SysFont('Verdana', 16)
        image = Surface((w, h))
        rect = image.get_rect()
        image.fill(CANVAS_BG)
        rect.midleft = x, y
        self.w, self.h = w, h
        self.boton_mas = Boton(self, self.char + '+', 1, self.incrementar, [rect.right-25, 0], texto='+')
        self.boton_mas.rect.centery = rect.centery
        self.boton_menos = Boton(self, self.char + '-', 1, self.decrementar, [rect.left-70, 0], texto='-')
        self.boton_menos.rect.centery = rect.centery
        self.botones = LayeredUpdates(self.boton_mas, self.boton_menos)

        super().__init__(parent, imagen=image, rect=rect, x=x, y=y)
        self.render_value()

    def accion(self):
        if self.boton_mas.isSelected:
            self.boton_mas.ser_presionado()
        elif self.boton_menos.isSelected:
            self.boton_menos.ser_presionado()

    def incrementar(self):
        if self.parent.puntos.update_value(-1):
            self.value += 1
            self.render_value()

    def decrementar(self):
        if self.value - 1 >= 0:
            self.parent.puntos.update_value(+1)
            self.value -= 1
            self.render_value()

    def reset(self):
        self.value = 0

    def render_value(self):
        string = '{:+}'.format(self.value)
        render = render_textrect(string, self.fuente, self.rect, TEXT_FG, CANVAS_BG, 1)
        self.image.blit(render, (0, 0))

    def elegir(self, posicion):
        self.deselegir()
        if posicion == 'derecha':
            self.boton_mas.ser_elegido()
        elif posicion == 'izquierda':
            self.boton_menos.ser_elegido()
        self.isSelected = True

    def elegir_mas(self):
        self.boton_menos.ser_deselegido()
        self.boton_mas.ser_elegido()

    def elegir_menos(self):
        self.boton_mas.ser_deselegido()
        self.boton_menos.ser_elegido()

    def deselegir(self):
        self.isSelected = False
        self.boton_mas.ser_deselegido()
        self.boton_menos.ser_deselegido()

    def update(self):
        draw.aaline(self.image, TEXT_FG, [0, self.h - 1], [self.w, self.h - 1])
        self.botones.update()
        self.botones.draw(self.parent.canvas)

    def __repr__(self):
        return self.char


class PuntosDisponibles(BaseWidget):
    t = ''

    def __init__(self, parent, x, y):
        self.f = font.SysFont('Verdana', 16)
        self.pos = x, y
        self.value = 50 if not len(memoria) else 0
        image = self.f.render(self.t, True, TEXT_FG, CANVAS_BG)
        rect = image.get_rect(topleft=[x, y])
        super().__init__(parent, imagen=image, rect=rect, x=x, y=y)
        self.update_text()

    def update_value(self, mod):
        if 0 <= self.value + mod <= 50:
            self.value += mod
            return True
        return False

    def update_text(self):
        if self.value > 0:
            self.t = f'Tienes {str(self.value)} puntos para repartir entre tus {self.parent.nombre.lower()}.'
        else:
            self.t = f'No quedan más puntos para repartir entre tus {self.parent.nombre.lower()}.'

    def reset(self):
        self.value = 50
        self.update_text()

    def update(self):
        self.update_text()
        self.image = self.f.render(self.t, True, TEXT_FG, CANVAS_BG)
        self.rect = self.image.get_rect(topleft=self.pos)
