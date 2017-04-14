# script.py

from engine.globs import ModState
from engine.globs.eventDispatcher import EventDispatcher
from engine.misc import Resources


def boton_step(nombre, data):
    ModState.set(nombre + '.pressed', data['pressed'])
    EventDispatcher.trigger('button_activated', 'boton', {})


def door_activate(puerta, event):
    del event  # es irrelevante, pero EventDispatcher llama la funcion con dos argumentos.
    btn1_activo = ModState.get('boton_azul.pressed')
    btn2_activo = ModState.get('boton_verde.pressed')
    if btn1_activo and btn2_activo:
        puerta.operar(1)
    else:
        puerta.operar(0)
    ModState.set('puerta.open', btn1_activo and btn2_activo)
    # este valor lo puede usar la rutina de load game para setear el estado correcto del objeto


def init_game(event):
    # event tendria data de si el juego es nuevo o es un savegame.
    from engine.globs import EngineData

    if 'savegame' in event.data:
        data = event.data['savegame']

        mapa = data['mapa']
        entrada = data['link']
        dia, hora, minutos = data.get('tiempo', [0, 9, 54])
        focus = data.get('focus', 'heroe')

    else:  # esta data estaba en la scene
        # datos por default
        mapa = "prueba"
        entrada = "bottomright"
        dia, hora, minutos = 0, 0, 0
        focus = 'heroe'

    EventDispatcher.deregister(init_game, 'NewGame')
    EngineData.cargar_juego(mapa, entrada, dia, hora, minutos, focus)


def init_system(event):
    if event.data['intro']:
        _module = Resources.load_module_from_script('intro')

        # se supone que el modder sabe cómo se llama la función
        getattr(_module, 'creditos_introduccion')()
    EventDispatcher.trigger('OpenMenu', 'Script', {'value': 'Principal'})

EventDispatcher.register(init_system, 'InitSystem')
EventDispatcher.register(init_game, 'NewGame')
