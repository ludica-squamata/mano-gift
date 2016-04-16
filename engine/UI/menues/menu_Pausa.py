from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import CUADRO
from engine.misc import Config as Cfg
from engine.UI.widgets import Boton
from .menu import Menu


class MenuPausa(Menu):
    def __init__(self):
        super().__init__("Pausa")
        x = self.canvas.get_width() - (CUADRO * 6) - 14  # 460-192-14 = 254
        m, k, p, c = 'nombre', 'direcciones', 'pos', 'comando'
        a, b, i, d = 'arriba', 'abajo', 'izquierda', 'derecha'

        botones = [
            {m: "Items", p: [x, 93], k: {a: "Personaje", b: "Equipo"}, c: self.new_menu},
            {m: "Equipo", p: [x, 132], k: {a: "Items", b: "Status"}, c: self.new_menu},
            {m: "Status", p: [x, 171], k: {a: "Equipo", b: "Grupo"}, c: self.new_menu},
            {m: "Grupo", p: [x, 210], k: {a: "Status", b: "Opciones"}, c: self.new_menu},
            {m: "Opciones", p: [x, 249], k: {a: "Grupo", b: "Debug"}, c: self.new_menu},
            {m: "Debug", p: [x, 288], k: {a: 'Opciones', b: "Personaje"}, c: self.new_menu},
            {m: "Personaje", p: [x, 327], k: {a: 'Debug', b: "Items"}, c: self.new_menu}
        ]

        self.establecer_botones(botones, 6)

        self.functions.update({
            'tap': {
                'hablar': self.press_button,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo')
            },
            'hold': {
                'hablar': self.mantener_presion,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo')
            },
            'release': {
                'hablar': self.liberar_presion,
            }
        })

    def establecer_botones(self, botones, ancho_mod):
        for btn in botones:
            boton = Boton(btn['nombre'], ancho_mod, btn['comando'], btn['pos'])
            for direccion in ['arriba', 'abajo', 'izquierda', 'derecha']:
                if direccion in btn['direcciones']:
                    boton.direcciones[direccion] = btn['direcciones'][direccion]

            self.botones.add(boton)

        self.cur_btn = 0
        self.reset()

    def select_one(self, direccion):
        self.deselect_all(self.botones)
        if len(self.botones) > 0:
            current = self.botones.get_sprite(self.cur_btn)
            if direccion in current.direcciones:
                selected = current.direcciones[direccion]
            else:
                selected = current.nombre

            for i in range(len(self.botones)):
                boton = self.botones.get_sprite(i)
                if boton.nombre == selected:
                    boton.ser_elegido()
                    self.mover_cursor(boton)
                    break

            self.botones.draw(self.canvas)

    def cancelar(self):
        return False

    def new_menu(self):
        EventDispatcher.trigger('SetMode', self.nombre, {'mode': 'NewMenu', 'value': self.current.nombre})

    def reset(self):
        """Reseta el presionado de todos los botones, y deja seleccionado
        el que haya sido elegido anteriormente."""
        self.deselect_all(self.botones)
        if not Cfg.dato("recordar_menus"):
            self.cur_btn = 0
        selected = self.botones.get_sprite(self.cur_btn)
        selected.ser_elegido()
        self.current = selected
        self.botones.draw(self.canvas)
        self.active = True

    def update(self):
        self.botones.update()
        self.botones.draw(self.canvas)
