from engine.globs.event_dispatcher import EventDispatcher
from engine.libs.textrect import render_textrect
from engine.globs import CANVAS_BG, TEXT_FG
from engine.globs.mod_data import ModData
from pygame import font, draw, Surface
from pygame.sprite import LayeredUpdates
from ..widgets import BaseWidget, Boton
from .menu import Menu


class MenuAbility(Menu):
    current_counter = None
    current_idx = 0
    posicion_horizontal = 'izquierda'

    def __init__(self):
        super().__init__('Atributos', 'Atributos')

        chars = list(ModData.data['caracteristicas'].keys())
        self.counters = LayeredUpdates()

        fuente = font.SysFont('Verdana', 16, bold=True)
        for i, char in enumerate(chars):
            render = fuente.render(char, 1, TEXT_FG, CANVAS_BG)
            rect = render.get_rect(topleft=[6, 125 + i * 43])
            self.canvas.blit(render, rect)

        for i, char in enumerate(chars):
            self.counters.add(Counter(self, char, 200, 130 + i * 40, 58, 22))

        self.fin = Boton('Finalizar', 6, self.finalizar, [self.rect.centerx, self.rect.bottom-64])
        self.botones.add(self.fin)

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
            'arriba': lambda: self.elegir_uno(-1),
            'abajo': lambda: self.elegir_uno(+1),
            'izquierda': lambda: self.eleccion_horizontal('izquierda'),
            'derecha': lambda: self.eleccion_horizontal('derecha')
        })

    @property
    def valores(self):
        vs = {}
        for counter in self.counters.sprites():
            vs[counter.char] = counter.value

        return vs

    def elegir_uno(self, delta):
        for counter in self.counters:
            counter.deselegir()

        self.current_idx += delta
        if self.current_idx > len(self.counters) - 1:
            self.current_idx = 0
        elif self.current_idx < 0:
            self.current_idx = len(self.counters) - 1

        self.current_counter = self.counters.sprites()[self.current_idx]
        self.current_counter.elegir(self.posicion_horizontal)

    def eleccion_horizontal(self, direccion):
        if direccion == 'derecha':
            if self.posicion_horizontal == 'izquierda':
                self.current_counter.elegir_mas()
                self.posicion_horizontal = 'derecha'
            else:
                self.posicion_horizontal = 'ninguna'
                for counter in self.counters:
                    counter.deselegir()
                self.fin.ser_elegido()

        elif direccion == 'izquierda':
            if self.posicion_horizontal == 'derecha':
                self.current_counter.elegir_menos()
                self.posicion_horizontal = 'izquierda'
            elif self.posicion_horizontal == 'ninguna':
                self.fin.ser_deselegido()
                self.counters.sprites()[self.current_idx].elegir('derecha')
                self.posicion_horizontal = 'derecha'

    def modificar_valor(self):
        if any(counter.isSelected for counter in self.counters.sprites()):
            for counter in self.counters.sprites():
                if counter.isSelected:
                    self.current_counter.accion()
        else:
            self.fin.ser_presionado()

    def finalizar(self):
        self.deregister()
        EventDispatcher.trigger('CharacterCreation', self.nombre, {'atributos': self.valores, 'final': False})
        EventDispatcher.trigger('OpenMenu', self.nombre, {'value': 'Name'})

    def update(self):
        self.counters.update()
        self.counters.draw(self.canvas)
        self.botones.update()
        self.botones.draw(self.canvas)


class Counter(BaseWidget):
    value = 8
    char = ''

    def __init__(self, parent, char_name, x, y, w, h):
        self.parent = parent
        self.char = char_name
        self.fuente = font.SysFont('Verdana', 16)
        image = Surface((w, h))
        rect = image.get_rect()
        image.fill(CANVAS_BG)
        rect.topleft = x, y
        self.w, self.h = w, h
        self.boton_mas = Boton(self.char + '+', 1, self.incrementar, [rect.right, 0], texto='+')
        self.boton_mas.rect.centery = rect.centery
        self.boton_menos = Boton(self.char + '-', 1, self.decrementar, [rect.left - 40, 0], texto='-')
        self.boton_menos.rect.centery = rect.centery
        self.botones = LayeredUpdates(self.boton_mas, self.boton_menos)

        super().__init__(imagen=image, rect=rect, x=x, y=y)
        self.render_value()

    def accion(self):
        if self.boton_mas.isSelected:
            self.boton_mas.ser_presionado()
        elif self.boton_menos.isSelected:
            self.boton_menos.ser_presionado()

    def incrementar(self):
        self.value += 1
        self.render_value()

    def decrementar(self):
        self.value -= 1
        self.render_value()

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
