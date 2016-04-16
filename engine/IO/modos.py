from engine.globs import EngineData as Ed
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from engine.globs import TAP, HOLD, RELEASE, TECLAS, CAPA_OVERLAYS_MENUS
from engine.misc import Util
from .taphold import get_taphold_events
from pygame import KEYDOWN, QUIT, K_ESCAPE, K_F1, K_F2, K_F3, K_F4
from engine.UI.menues import *
from engine.UI import QuickCircularMenu


class Modo:
    dx, dy = 0, 0
    newMenu = False
    setKey = False

    @classmethod
    def juego(cls, events):
        for event in events:
            if event.type == QUIT:
                Util.salir()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Util.salir()

                elif event.key == K_F1:
                    Ed.HERO.z += 1

                elif event.key == K_F2:
                    Ed.HERO.z -= 1

                elif event.key == K_F3:
                    Ed.HERO.z += 10

                elif event.key == K_F4:
                    Ed.HERO.z -= 10

        EventDispatcher.process()

    @classmethod
    def aventura(cls, events, fondo):
        Ed.HUD.update()
        dx, dy = cls.dx, cls.dy
        for event in get_taphold_events(events):
            if event.type == TAP:
                if event.key == TECLAS.HABLAR:
                    if Ed.HERO.iniciar_dialogo():
                        Ed.MODO = 'Dialogo'
                    else:
                        Ed.MODO = 'Aventura'

                elif event.key == TECLAS.MENU_RAPIDO:
                    Ed.MODO = 'Dialogo'
                    if Ed.MENU_RAPIDO is None:
                        Ed.MENU_RAPIDO = QuickCircularMenu()

                    Ed.DIALOG = Ed.MENU_RAPIDO
                    Ed.DIALOG.show()

                elif event.key == TECLAS.ACCION:
                    Ed.HERO.accion()

                elif event.key == TECLAS.MENU:
                    cls.pop_menu('Pausa')

                elif event.key == TECLAS.IZQUIERDA:
                    Ed.HERO.cambiar_direccion('izquierda', True)
                elif event.key == TECLAS.DERECHA:
                    Ed.HERO.cambiar_direccion('derecha', True)
                elif event.key == TECLAS.ARRIBA:
                    Ed.HERO.cambiar_direccion('arriba', True)
                elif event.key == TECLAS.ABAJO:
                    Ed.HERO.cambiar_direccion('abajo', True)

            elif event.type == HOLD:
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
            if event.type == TAP:
                if event.key == TECLAS.ARRIBA:
                    Ed.DIALOG.use_function('tap', 'arriba')

                elif event.key == TECLAS.ABAJO:
                    Ed.DIALOG.use_function('tap', 'abajo')

                elif event.key == TECLAS.IZQUIERDA:
                    Ed.DIALOG.use_function('tap', 'izquierda')

                elif event.key == TECLAS.DERECHA:
                    Ed.DIALOG.use_function('tap', 'derecha')

                elif event.key == TECLAS.HABLAR:
                    Ed.DIALOG.use_function('tap', 'hablar')

                elif event.key == TECLAS.MENU_RAPIDO:
                    Ed.DIALOG.use_function('tap', 'inventario')

                elif event.key == TECLAS.CANCELAR_DIALOGO:
                    Ed.DIALOG.use_function('tap', 'cancelar')

            elif event.type == HOLD:
                if event.key == TECLAS.IZQUIERDA:
                    Ed.DIALOG.use_function('hold', 'izquierda')

                elif event.key == TECLAS.DERECHA:
                    Ed.DIALOG.use_function('hold', 'derecha')

                elif event.key == TECLAS.ARRIBA:
                    Ed.DIALOG.use_function('hold', 'arriba')

                elif event.key == TECLAS.ABAJO:
                    Ed.DIALOG.use_function('hold', 'abajo')

            elif event.type == RELEASE:
                if event.key == TECLAS.IZQUIERDA:
                    Ed.DIALOG.use_function('release', 'izquierda')

                elif event.key == TECLAS.DERECHA:
                    Ed.DIALOG.use_function('release', 'derecha')

                elif event.key == TECLAS.ARRIBA:
                    Ed.DIALOG.use_function('release', 'arriba')

                elif event.key == TECLAS.ABAJO:
                    Ed.DIALOG.use_function('release', 'abajo')

        if Ed.DIALOG is None:
            Ed.MODO = "Aventura"

        return Renderer.update(fondo)

    @classmethod
    def menu(cls, events, fondo):
        for event in get_taphold_events(events):
            if event.type == TAP:
                if Ed.setKey:
                    Ed.menu_actual.cambiar_tecla(event.key)
                    Ed.setKey = False

                elif event.key == TECLAS.IZQUIERDA:
                    Ed.menu_actual.use_function('tap', 'izquierda')

                elif event.key == TECLAS.DERECHA:
                    Ed.menu_actual.use_function('tap', 'derecha')

                elif event.key == TECLAS.ARRIBA:
                    Ed.menu_actual.use_function('tap', 'arriba')

                elif event.key == TECLAS.ABAJO:
                    Ed.menu_actual.use_function('tap', 'abajo')

                elif event.key == TECLAS.HABLAR:
                    Ed.menu_actual.use_function('tap', 'hablar')

                elif event.key == TECLAS.CANCELAR_DIALOGO:
                    previo = Ed.menu_actual.cancelar()  # podría ser usar_funcion
                    if previo:
                        cls.pop_menu(Ed.menu_previo)
                    elif previo is not None:
                        cls.end_dialog(CAPA_OVERLAYS_MENUS)

            elif event.type == HOLD:
                if event.key == TECLAS.HABLAR:
                    Ed.menu_actual.use_function('hold', 'hablar')

                elif event.key == TECLAS.IZQUIERDA:
                    Ed.menu_actual.use_function('hold', 'izquierda')

                elif event.key == TECLAS.DERECHA:
                    Ed.menu_actual.use_function('hold', 'derecha')

                elif event.key == TECLAS.ARRIBA:
                    Ed.menu_actual.use_function('hold', 'arriba')

                elif event.key == TECLAS.ABAJO:
                    Ed.menu_actual.use_function('hold', 'abajo')

            elif event.type == RELEASE:
                if event.key == TECLAS.HABLAR:
                    Ed.menu_actual.use_function('release', 'hablar')

        if cls.newMenu:
            cls.pop_menu()

        Ed.menu_actual.update()
        return Renderer.update(fondo)

    @classmethod
    def toggle_mode(cls, event):
        """
        :param event:
        :type event:AzoeEvent
        :return:
        """
        value = event.data['value']
        if event.data['mode'] == 'NewMenu':
            cls.newMenu = value

    @classmethod
    def pop_menu(cls, titulo=None):
        if titulo is None:
            titulo = cls.newMenu

        if Ed.menu_previo == '' and Ed.menu_previo != titulo:
            Ed.menu_previo = titulo

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
        Ed.MODO = 'Menu'
        Ed.onPause = True
        Ed.menu_actual = menu
        Renderer.add_overlay(menu, CAPA_OVERLAYS_MENUS)
        Renderer.overlays.move_to_front(menu)

    @staticmethod
    def end_dialog(layer):
        Renderer.clear_overlays_from_layer(layer)
        Ed.DIALOG = None
        Ed.MODO = 'Aventura'
        Ed.onPause = False


EventDispatcher.register(Modo.toggle_mode, 'SetMode')
