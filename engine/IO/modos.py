from engine.globs import EngineData as Ed, ModData as Md, CAPA_OVERLAYS_MENUS
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from .taphold import get_taphold_events
from engine.UI.menues import *
from engine.UI import QuickCircularMenu


def update(events):
    EventDispatcher.process()
    for event in get_taphold_events(events):
        EventDispatcher.trigger('Key', 'Modo.'+Ed.MODO, event.__dict__)

    return Renderer.update()


def toggle_mode(event):
    nombre = event.data.get('nom', None)
    tipo = event.data.get('type', None)
    origin = event.origin

    if tipo == 'tap' and origin == 'Modo.Aventura':
        if nombre == 'menu':
            EventDispatcher.trigger('OpenMenu', origin, {'value': 'Pausa'})

        elif nombre == 'contextual':
            Ed.HERO.detener_movimiento()
            QuickCircularMenu(Ed.current_qcm_idx, Md.QMC)


def pop_menu(event):
    titulo = event.data['value']
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
    menu.register()
    Renderer.add_overlay(menu, CAPA_OVERLAYS_MENUS)
    Renderer.overlays.move_to_front(menu)


EventDispatcher.register(pop_menu, 'OpenMenu')
EventDispatcher.register(toggle_mode, 'Key')
