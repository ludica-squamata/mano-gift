from engine.globs import EngineData, FEATURE_MENUS_ADICIONALES, ModData
from engine.globs.event_dispatcher import EventDispatcher
from .menu import Menu


class MenuPausa(Menu):
    nombres = None

    def __init__(self, parent):
        super().__init__(parent, "Pausa")
        self.timer_animacion = 0
        self.frame_animacion = 1000 / 6

        x = self.rect.centerx - (32 * 3) - 10

        names = []
        from . import pause_menus
        for menu_name in pause_menus + (list(ModData.custommenus.keys())):
            # los menúes por default, más los menúes custom declarados en mod.json
            button_name = menu_name[4:]
            if button_name not in names:
                names.append(button_name)

        a, b = 'arriba', 'abajo'
        # expandí un poco las keys para hacer el array más legible
        buttons = []
        for j, nombre in enumerate(names):
            buttons.append({'nombre': nombre, 'direcciones': {a: names[j - 1], b: names[j - (len(names) - 1)]}})

        if FEATURE_MENUS_ADICIONALES:
            buttons[1]['direcciones'][b] = 'Grupo'
            buttons.insert(2, {'nombre': "Grupo", 'direcciones': {a: "Status", b: "Opciones"}})
            buttons[3]['direcciones'][a] = "Grupo"

        for i in range(len(buttons)):
            buttons[i]['pos'] = [x, 50 * i + 120]
            buttons[i]['comando'] = self.new_menu

        self.establecer_botones(buttons, 6)

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

    def cancelar(self):
        EngineData.acceso_menues.clear()
        self.deregister()
        EventDispatcher.trigger('EndDialog', self, {'layer': self.layer})

    def new_menu(self):
        self.deregister()
        EventDispatcher.trigger('OpenMenu', self.nombre, {'value': self.current.nombre})

    def reset(self, **kwargs):
        """Reseta el presionado de todos los botones, y deja seleccionado el que haya sido elegido anteriormente."""
        self.on_reset()

    def update(self):
        self.botones.update()
        self.botones.draw(self.canvas)
