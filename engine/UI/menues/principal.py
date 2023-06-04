from .menu import Menu
from engine.globs.event_dispatcher import EventDispatcher


class MenuPrincipal(Menu):
    def __init__(self, parent):
        super().__init__(parent, 'Principal', "Azoe's Gifts")
        x = self.rect.centerx - (32 * 3) - 10

        nombres = []
        from . import inital_menus
        # acá hacemos un truco similar al que se hace en Pausa,
        # pero tiene menos efecto porque no hay menus custom en Principal.
        for name in inital_menus:
            m = name[4:]
            if m not in nombres:
                nombres.append(m)
        nombres.append('Salir')

        botones = []
        a, b = 'arriba', 'abajo'
        # expandí un poco las keys para hacer el array más legible
        for j, nombre in enumerate(nombres):
            botones.append({'nombre': nombre, 'direcciones': {a: nombres[j - 1], b: nombres[j - (len(nombres) - 1)]},
                            'comando': self.new_menu, 'pos': [x, 50 * j + 120]})

        botones[-1]['comando'] = lambda: EventDispatcher.trigger('QUIT', self, {'status': 'normal'})
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

    def reset(self, **kwargs):
        """Reseta el presionado de todos los botones, y deja seleccionado el que haya sido elegido anteriormente."""
        self.on_reset()

    def update(self):
        self.botones.update()
        self.botones.draw(self.canvas)
