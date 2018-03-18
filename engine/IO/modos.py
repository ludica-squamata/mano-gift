from engine.globs import EngineData, ModData as Md, CAPA_OVERLAYS_MENUS
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from .taphold import get_taphold_events
from engine.UI.menues import default_menus
from engine.UI import QuickCircularMenu


def update(events):
    EventDispatcher.process()
    for event in get_taphold_events(events):
        EventDispatcher.trigger('Key', 'Modo.' + EngineData.MODO, event.__dict__)

    return Renderer.update()


def toggle_mode(event):
    nombre = event.data.get('nom', None)
    tipo = event.data.get('type', None)
    origin = event.origin

    if tipo == 'tap' and origin == 'Modo.Aventura':
        if nombre == 'menu':
            EventDispatcher.trigger('OpenMenu', origin, {'value': 'Pausa'})

        elif nombre == 'contextual':
            EngineData.HERO.detener_movimiento()
            QuickCircularMenu(EngineData.current_qcm_idx, Md.QMC)


def pop_menu(event):
    titulo = event.data['value']
    if titulo == 'Previous':
        del EngineData.acceso_menues[-1]
        titulo = EngineData.acceso_menues[-1]
    else:
        EngineData.acceso_menues.append(titulo)

    if titulo not in EngineData.MENUS:
        name = 'Menu' + titulo
        if name in Md.custommenus:
            menu = Md.custommenus[name]()
        elif name in default_menus:
            menu = default_menus[name]()
        else:
            raise NotImplementedError('El menu "{}" no existe'.format(titulo))
    else:
        menu = EngineData.MENUS[titulo]
        menu.reset()

    menu.register()
    EngineData.MODO = 'Menu'
    if not EngineData.onPause:
        EventDispatcher.trigger('TogglePause', 'Modos', {'value': True})
    Renderer.add_overlay(menu, CAPA_OVERLAYS_MENUS)
    Renderer.overlays.move_to_front(menu)


EventDispatcher.register(pop_menu, 'OpenMenu')
EventDispatcher.register(toggle_mode, 'Key')
