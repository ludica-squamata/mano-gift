from engine.globs import Constants as Cs, EngineData as Ed
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from engine.misc import Util
from .taphold import get_taphold_events
from pygame import KEYDOWN, QUIT, K_ESCAPE
from engine.UI.menues import *


class Modo:
    dx, dy = 0, 0
    newMenu = False
    setKey = False

    @staticmethod
    def juego(events):
        for event in events:
            if event.type == QUIT:
                Util.salir()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    Util.salir()

                elif event.key == Cs.TECLAS.DEBUG:
                    pass

    @staticmethod
    def aventura(events, fondo):
        Ed.HUD.update()
        dx, dy = Modo.dx, Modo.dy
        for event in get_taphold_events(events):
            if event.type == Cs.TAP:
                if event.key == Cs.TECLAS.HABLAR:
                    if Ed.HERO.iniciar_dialogo():
                        Ed.MODO = 'Dialogo'
                    else:
                        Ed.MODO = 'Aventura'

                elif event.key == Cs.TECLAS.INVENTARIO:
                    Ed.MODO = 'Dialogo'
                    Ed.HUD.Inventory.SelectCuadro()
                    Ed.DIALOG = Ed.HUD

                elif event.key == Cs.TECLAS.POSICION_COMBATE:
                    Ed.HERO.cambiar_estado()

                elif event.key == Cs.TECLAS.ACCION:
                    Ed.HERO.accion()

                elif event.key == Cs.TECLAS.MENU:
                    Modo.pop_menu('Pausa')

                elif event.key == Cs.TECLAS.IZQUIERDA:
                    Ed.HERO.cambiar_direccion('izquierda', True)
                elif event.key == Cs.TECLAS.DERECHA:
                    Ed.HERO.cambiar_direccion('derecha', True)
                elif event.key == Cs.TECLAS.ARRIBA:
                    Ed.HERO.cambiar_direccion('arriba', True)
                elif event.key == Cs.TECLAS.ABAJO:
                    Ed.HERO.cambiar_direccion('abajo', True)

            elif event.type == Cs.HOLD:
                if event.key == Cs.TECLAS.IZQUIERDA:
                    dx = -1
                elif event.key == Cs.TECLAS.DERECHA:
                    dx = +1
                elif event.key == Cs.TECLAS.ARRIBA:
                    dy = -1
                elif event.key == Cs.TECLAS.ABAJO:
                    dy = +1

            elif event.type == Cs.RELEASE:
                if event.key == Cs.TECLAS.IZQUIERDA or event.key == Cs.TECLAS.DERECHA:
                    dx = 0
                elif event.key == Cs.TECLAS.ABAJO or event.key == Cs.TECLAS.ARRIBA:
                    dy = 0

        if dx != 0 or dy != 0:
            Ed.HERO.mover(dx, dy)
        Modo.dx, Modo.dy = dx, dy
        EventDispatcher.process()
        Ed.MAPA_ACTUAL.update()
        return Renderer.update(fondo)

    @staticmethod
    def dialogo(events, fondo):
        for event in get_taphold_events(events):
            if event.type == Cs.TAP:
                if event.key == Cs.TECLAS.ARRIBA:
                    Ed.DIALOG.usar_funcion('arriba')

                elif event.key == Cs.TECLAS.ABAJO:
                    Ed.DIALOG.usar_funcion('abajo')

                elif event.key == Cs.TECLAS.IZQUIERDA:
                    Ed.DIALOG.usar_funcion('izquierda')

                elif event.key == Cs.TECLAS.DERECHA:
                    Ed.DIALOG.usar_funcion('derecha')

                elif event.key == Cs.TECLAS.HABLAR:
                    Ed.DIALOG.usar_funcion('hablar')

                elif event.key == Cs.TECLAS.INVENTARIO:
                    Ed.DIALOG.usar_funcion('inventario')

                elif event.key == Cs.TECLAS.CANCELAR_DIALOGO:
                    Ed.DIALOG.usar_funcion('cancelar')

        if Ed.DIALOG is None:
            Ed.MODO = "Aventura"

        return Renderer.update(fondo)

    @staticmethod
    def menu(events, fondo):
        for event in get_taphold_events(events):

            if event.type == Cs.TAP:
                if Modo.setKey:
                    Ed.menu_actual.cambiar_tecla(event.key)
                    Modo.setKey = False

                elif event.key == Cs.TECLAS.IZQUIERDA:
                    Ed.menu_actual.usar_funcion('izquierda')

                elif event.key == Cs.TECLAS.DERECHA:
                    Ed.menu_actual.usar_funcion('derecha')

                elif event.key == Cs.TECLAS.ARRIBA:
                    Ed.menu_actual.usar_funcion('arriba')

                elif event.key == Cs.TECLAS.ABAJO:
                    Ed.menu_actual.usar_funcion('abajo')

                elif event.key == Cs.TECLAS.HABLAR:
                    Ed.menu_actual.usar_funcion('hablar')

                elif event.key == Cs.TECLAS.CANCELAR_DIALOGO:
                    previo = Ed.menu_actual.cancelar()  # podría ser usar_funcion
                    if previo:
                        Modo.pop_menu(Ed.menu_previo)
                    elif previo is not None:
                        Modo.end_dialog(Cs.CAPA_OVERLAYS_MENUS)

            elif event.type == Cs.HOLD:
                if event.key == Cs.TECLAS.HABLAR:
                    Ed.menu_actual.current.mantener_presion()

                elif event.key == Cs.TECLAS.IZQUIERDA:
                    Ed.menu_actual.usar_funcion('izquierda')

                elif event.key == Cs.TECLAS.DERECHA:
                    Ed.menu_actual.usar_funcion('derecha')

                elif event.key == Cs.TECLAS.ARRIBA:
                    Ed.menu_actual.usar_funcion('arriba')

                elif event.key == Cs.TECLAS.ABAJO:
                    Ed.menu_actual.usar_funcion('abajo')

            elif event.type == Cs.RELEASE:
                if event.key == Cs.TECLAS.HABLAR:
                    Ed.menu_actual.current.liberar_presion()

        if Modo.newMenu:
            Modo.pop_menu(Ed.menu_actual.current.nombre)
            Modo.newMenu = False

        Ed.menu_actual.update()
        return Renderer.update(fondo)

    @staticmethod
    def pop_menu(titulo):
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

        Ed.MODO = 'Menu'
        Ed.onPause = True

        Ed.menu_actual = menu
        Renderer.add_overlay(menu, Cs.CAPA_OVERLAYS_MENUS)
        Renderer.overlays.move_to_front(menu)

    @staticmethod
    def end_dialog(layer):
        Renderer.overlays.remove_sprites_of_layer(layer)
        Ed.DIALOG = None
        Ed.MODO = 'Aventura'
        Ed.onPause = False
