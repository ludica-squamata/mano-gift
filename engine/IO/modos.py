from engine.globs import EngineData as Ed, ModData as Md
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from engine.globs import TAP, HOLD, RELEASE, TECLAS, CAPA_OVERLAYS_MENUS
from engine.misc import Util
from .taphold import get_taphold_events
from pygame import KEYDOWN, QUIT, K_ESCAPE
from engine.UI.menues import *
from engine.UI import QuickCircularMenu


class Modo:
    dx, dy = 0, 0
    newMenu = False
    previo = False
    setKey = False

    @classmethod
    def juego(cls, events):
        for event in events:
            if event.type == QUIT:
                Util.salir()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Util.salir()

        EventDispatcher.process()

    @classmethod
    def aventura(cls, events, fondo):
        Ed.HUD.update()
        dx, dy = cls.dx, cls.dy
        for event in get_taphold_events(events):
            EventDispatcher.trigger('key', 'Modo.Aventura', event.__dict__)

            if event.type == HOLD:
                if event.key == TECLAS.IZQUIERDA:
                    dx = -1
                elif event.key == TECLAS.DERECHA:
                    dx = +1
                elif event.key == TECLAS.ARRIBA:
                    dy = -1
                elif event.key == TECLAS.ABAJO:
                    dy = +1

            elif event.type == RELEASE:
                if event.key == TECLAS.IZQUIERDA or event.key == TECLAS.DERECHA:
                    dx = 0
                elif event.key == TECLAS.ABAJO or event.key == TECLAS.ARRIBA:
                    dy = 0

        if dx != 0 or dy != 0:
            Ed.HERO.mover(dx, dy)
        cls.dx, cls.dy = dx, dy
        Ed.MAPA_ACTUAL.update()
        return Renderer.update(fondo)

    @staticmethod
    def dialogo(events, fondo):
        for event in get_taphold_events(events):
            EventDispatcher.trigger('key', 'Modo.Dialogo', event.__dict__)

        if Ed.DIALOG is not None:
            Ed.DIALOG.update()
        else:
            Ed.MODO = "Aventura"

        return Renderer.update(fondo)

    @classmethod
    def menu(cls, events, fondo):
        for event in get_taphold_events(events):
            EventDispatcher.trigger('key', 'Modo.Menu', event.__dict__)
            if (event.type == TAP or event.type == RELEASE) and Ed.setKey:
                Ed.menu_actual.cambiar_tecla(event.key)
                EventDispatcher.trigger('ToggleSetKey', 'Modo.Menu', {'value': False})

        if cls.newMenu:
            cls.pop_menu()

        Ed.menu_actual.update()
        return Renderer.update(fondo)

    @classmethod
    def change_menu(cls, event):
        """
        :param event:
        :type event:AzoeEvent
        :return:
        """

        if event.data['mode'] == 'NewMenu':
            cls.newMenu = event.data['value']
        elif event.data['mode'] == 'Previous':
            cls.newMenu = True
            cls.previo = True

    @classmethod
    def toggle_mode(cls, event):
        nombre = event.data.get('nom', None)
        if Ed.MODO == 'Aventura':
            if nombre == 'menu':
                Ed.MODO = 'Menu'
                EventDispatcher.trigger('SetMode', 'Modos', {'mode': 'NewMenu', 'value': 'Pausa'})

            elif nombre == 'contextual':
                Ed.MODO = 'Dialogo'
                Ed.DIALOG = QuickCircularMenu(Ed.current_qcm_idx, Md.QMC)
                Ed.DIALOG.show()

    @classmethod
    def pop_menu(cls, titulo=None):
        if titulo is None:
            titulo = cls.newMenu

        if cls.previo:
            del Ed.acceso_menues[-1]
            titulo = Ed.acceso_menues[-1]
        else:
            Ed.acceso_menues.append(titulo)

        if titulo not in Ed.MENUS:
            try:
                menu = eval('Menu' + titulo + '()')
            except Exception as Description:
                print('No se pudo abrir el menu porque:', Description)
                menu = Menu(titulo)
        else:
            menu = Ed.MENUS[titulo]
            menu.reset()

        cls.newMenu = False
        cls.previo = False
        Ed.MODO = 'Menu'
        Ed.onPause = True
        Ed.menu_actual = menu
        Ed.menu_actual.register()
        if Ed.HUD is not None:
            Ed.HUD.hide()
        Renderer.add_overlay(menu, CAPA_OVERLAYS_MENUS)
        Renderer.overlays.move_to_front(menu)

EventDispatcher.register(Modo.change_menu, 'SetMode')
EventDispatcher.register(Modo.toggle_mode, 'key')
