from .menu import Menu
from engine.globs.eventDispatcher import EventDispatcher
from engine.misc.config import Config as Cfg


class MenuPrincipal(Menu):
    def __init__(self):
        super().__init__('Principal', "Azoe's Gifts")

        x = self.rect.centerx - (32 * 3) - 10

        m, k, c = 'nombre', 'direcciones', 'comando'
        a, b = 'arriba', 'abajo'

        botones = [
            {m: "Nuevo", k: {a: "Opciones", b: "Cargar"}, c: lambda: self.new_menu('Personaje')},
            {m: "Cargar", k: {a: "Nuevo", b: "Opciones"}, c: lambda: self.new_menu('Cargar')},
            {m: "Opciones", k: {a: "Cargar", b: "Nuevo"}, c: lambda: self.new_menu('Opciones')},
        ]
        for i in range(len(botones)):
            botones[i]['pos'] = [x, 50 * i + 120],

        self.establecer_botones(botones, 6)

        self.functions.update({
            'tap': {
                'accion': self.press_button,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo')
            },
            'hold': {
                'accion': self.mantener_presion,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo')
            },
            'release': {
                'accion': self.liberar_presion,
            }
        })

    def new_menu(self, titulo):
        EventDispatcher.trigger('SetMode', self.nombre, {'mode': 'NewMenu', 'value': titulo})

    def cancelar(self):
        pass

    def reset(self):
        """Reseta el presionado de todos los botones, y deja seleccionado
        el que haya sido elegido anteriormente."""
        self.deselect_all(self.botones)
        if not Cfg.dato("recordar_menus"):
            self.cur_btn = 0
        selected = self.botones.get_sprite(self.cur_btn)
        selected.ser_elegido()
        self.current = selected

        self.active = True

    def update(self):
        self.botones.update()
        self.botones.draw(self.canvas)
