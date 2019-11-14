from engine.globs import EngineData, CANVAS_BG, TEXT_FG
from engine.globs.event_dispatcher import EventDispatcher
from engine.UI.widgets import Boton
from pygame import font, Rect
from engine.libs import render_textrect
from .menu import Menu

from .name import MenuName
from .model import MenuModel
from .char_c_attrs import AttrsScreen


class MenuNuevo(Menu):
    foco = 'nombre'
    curr_scr_idx = 0

    def __init__(self):
        super().__init__('Personaje')
        w, h = self.canvas.get_size()
        self.screens = [MenuName(self), MenuModel(self), AttrsScreen(self)]
        self.screens[2].toggle_hidden()
        self.current_screen = self.screens[self.curr_scr_idx]
        self.f_ins = font.SysFont('Verdana', 14, italic=True)

        # generar botones
        n, c, d, a, b = 'nombre', 'cmd', 'direcciones', 'arriba', 'abajo'
        botones = [
            {n: 'Nombre', c: lambda: None, d: {a: 'Aceptar', b: 'Atributos'}},
            {n: 'Atributos', c: lambda: None, d: {a: 'Nombre', b: 'Modelo'}},
            {n: 'Modelo', c: lambda: None, d: {a: 'Atributos', b: 'Aceptar'}},
            {n: 'Aceptar', c: self.aceptar, d: {a: 'Modelo', b: 'Nombre'}},
        ]
        for i, btn in enumerate(reversed(botones)):
            boton = Boton(btn[n], 3, btn[c], (w - 105, h - 43 - (40 * i)))
            for direccion in ['arriba', 'abajo', 'izquierda', 'derecha']:
                if direccion in btn['direcciones']:
                    boton.direcciones[direccion] = btn['direcciones'][direccion]
            self.botones.add(boton)
        self.cur_btn = 3
        self.select_one(3)

        # dibujos estáticos
        self.print_instructions('nombre')

        # determinar qué tecla activa qué función.
        self.functions = {  # obsérvese que es dict.update()
            'tap': {
                'accion': self.press_button,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo'),

            },
            'hold': {
                'accion': self.mantener_presion,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo'),
            },
            'release': {
                'accion': self.liberar_presion
            }
        }

    def print_instructions(self, foco):
        if foco == 'nombre':
            s = "Escriba a continuación el nombre del personaje. Puede usar los caracteres provistos abajo"
        elif foco == 'modelo':
            s = 'Esto es un ejemplo para el modo Modelo'
        elif foco == 'atributos':
            s = 'Y esto otro son  las instrucciones para los Atributos'
        else:
            s = ''
        fuente = font.SysFont('Verdana', 14, italic=True)
        rect = Rect(10, 32, 600, 64)
        render = render_textrect(s, fuente, rect, TEXT_FG, CANVAS_BG)
        self.canvas.blit(render, rect)

    def use_function(self, mode, key):
        """Determina qué grupo de funciones se van a usar según el foco actual.
        :param mode: string,
        :param key: string
        """
        if self.foco != 'menu':
            self.current_screen.use_funcion(mode, key)
        else:
            super().use_function(mode, key)

    def cambiar_foco(self, foco):
        """Cambia el foco de selección de un grupo a otro."""
        # for screen in self.screens:
        #     screen.toggle_hidden()

        if foco == 'menu':
            self.foco = 'menu'
            self.current = self.botones.get_sprite(3)
            self.current.ser_elegido()

        elif foco == 'nombre':
            self.movercursor(-1, 0)
            self.deselect_all(self.botones)
            self.foco = 'nombre'

    def cancelar(self):
        if self.foco == 'nombre':
            if not len(self.area_input):
                super().cancelar()
            self.erase_character()
        else:
            self.cambiar_foco('nombre')

    def aceptar(self):
        EngineData.new_game(''.join([spr.key for spr in self.area_input]))
        EventDispatcher.trigger('EndDialog', self, {'layer': self.layer})

    def update(self):
        for screen in self.screens:
            screen.update()

        self.botones.update()
        self.draw()

    def draw(self):
        self.botones.draw(self.canvas)
