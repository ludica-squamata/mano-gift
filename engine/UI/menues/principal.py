from .menu import Menu
from engine.globs.event_dispatcher import EventDispatcher
from engine.misc.config import Config as Cfg


class MenuPrincipal(Menu):
    def __init__(self):
        super().__init__('Principal', "Azoe's Gifts")
        x = self.rect.centerx - (32 * 3) - 10

        nombres = []
        from . import inital_menus
        # acá hacemos un truco similar al que se hace en Pausa,
        # pero tiene menos efecto porque no hay menus custom en Principal.
        for name in inital_menus:
            m = name[4:]
            if m not in nombres:
                nombres.append(m)

        botones = []
        a, b = 'arriba', 'abajo'
        # expandí un poco las keys para hacer el array más legible
        for j, nombre in enumerate(nombres):
            botones.append({'nombre': nombre, 'direcciones': {a: nombres[j-1], b: nombres[j-(len(nombres)-1)]},
                            'comando': self.new_menu, 'pos': [x, 50 * j + 120]})

        self.establecer_botones(botones, 6)

        self.functions['tap'].update({
            'accion': self.press_button,
            'arriba': lambda: self.select_one('arriba'),
            'abajo': lambda: self.select_one('abajo')})
        self.functions['hold'].update({
            'accion': self.mantener_presion,
            'arriba': lambda: self.select_one('arriba'),
            'abajo': lambda: self.select_one('abajo')})
        self.functions['release'].update({
            'accion': self.liberar_presion})

    def new_menu(self):
        self.deregister()
        titulo = self.current.nombre
        EventDispatcher.trigger('OpenMenu', self.nombre, {'value': titulo})

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
