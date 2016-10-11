from engine.globs import EngineData as Ed, ModData as Md, CAPA_OVERLAYS_MENUS
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from engine.misc import Util
from .taphold import get_taphold_events
from pygame import KEYDOWN, QUIT, K_ESCAPE
from engine.UI.menues import *
from engine.UI import QuickCircularMenu


class Modo:
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
        for event in get_taphold_events(events):
            EventDispatcher.trigger('key', 'Modo.Aventura', event.__dict__)

        Ed.MAPA_ACTUAL.update()
        return Renderer.update(fondo)

    @staticmethod
    def dialogo(events, fondo):
        for event in get_taphold_events(events):
            EventDispatcher.trigger('key', 'Modo.Dialogo', event.__dict__)

        Ed.DIALOG.update()
        return Renderer.update(fondo)

    @classmethod
    def menu(cls, events, fondo):
        for event in get_taphold_events(events):
            EventDispatcher.trigger('key', 'Modo.Menu', event.__dict__)

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
        tipo = event.data.get('type', None)
        if Ed.MODO == 'Aventura':
            if nombre == 'menu':
                Ed.MODO = 'Menu'
                Ed.HERO.deregister()
                EventDispatcher.trigger('SetMode', 'Modos', {'mode': 'NewMenu', 'value': 'Pausa'})

            elif nombre == 'contextual' and tipo == 'tap':
                Ed.MODO = 'Dialogo'
                Ed.HERO.deregister()
                Ed.DIALOG = QuickCircularMenu(Ed.current_qcm_idx, Md.QMC)
                Ed.DIALOG.show()

        elif Ed.MODO == 'Dialogo':
            if nombre == 'contextual':
                Ed.HERO.register()

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
