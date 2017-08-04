from engine.globs import EngineData as Ed, ModData as Md, CAPA_OVERLAYS_MENUS
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from engine.misc import salir
from .taphold import get_taphold_events
from pygame import KEYDOWN, QUIT, K_ESCAPE
from engine.UI.menues import *
from engine.UI import QuickCircularMenu


class Modo:
    setKey = False

    @classmethod
    def juego(cls, events):
        for event in events:
            if event.type == QUIT:
                salir()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    salir()

        EventDispatcher.process()

    @staticmethod
    def update(events):
        modo = Ed.MODO
        for event in get_taphold_events(events):
            EventDispatcher.trigger('Key', 'Modo.'+modo, event.__dict__)

        if modo == 'Aventura':
            Ed.MAPA_ACTUAL.update()
        elif modo == 'Menu':
            Ed.menu_actual.update()
        elif modo == 'Dialogo':
            Ed.DIALOG.update()

        return Renderer.update()

    @classmethod
    def change_menu(cls, event):
        """
        :param event:
        :type event:AzoeEvent
        :return:
        """

        cls.pop_menu(titulo=event.data['value'])

    @classmethod
    def toggle_mode(cls, event):
        nombre = event.data.get('nom', None)
        tipo = event.data.get('type', None)
        if tipo == 'tap':
            if Ed.MODO == 'Aventura':
                if nombre == 'menu':
                    Ed.MODO = 'Menu'
                    Ed.HERO.deregister()
                    EventDispatcher.trigger('OpenMenu', 'Modo.Aventura', {'value': 'Pausa'})

                elif nombre == 'contextual':
                    Ed.HERO.detener_movimiento()
                    Ed.HERO.deregister()
                    QuickCircularMenu(Ed.current_qcm_idx, Md.QMC)

    @classmethod
    def pop_menu(cls, titulo=None):
        if titulo == 'Previous':
            del Ed.acceso_menues[-1]
            titulo = Ed.acceso_menues[-1]
        else:
            Ed.acceso_menues.append(titulo)

        if titulo not in Ed.MENUS:
            name = 'Menu' + titulo
            try:
                if name in Md.custommenus:
                    menu = Md.custommenus[name]()
                else:
                    # from globals()
                    menu = eval(name + '()')

            except Exception as Description:
                print('No se pudo abrir el menu porque:', Description)
                menu = Menu(titulo)
        else:
            menu = Ed.MENUS[titulo]
            menu.reset()

        Ed.MODO = 'Menu'
        EventDispatcher.trigger('TogglePause', 'Modos', {'value': True})
        Ed.menu_actual = menu
        Ed.menu_actual.register()
        if Ed.HUD is not None:
            Ed.HUD.hide()
        Renderer.add_overlay(menu, CAPA_OVERLAYS_MENUS)
        Renderer.overlays.move_to_front(menu)

EventDispatcher.register(Modo.change_menu, 'OpenMenu')
EventDispatcher.register(Modo.toggle_mode, 'Key')
