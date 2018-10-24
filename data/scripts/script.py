# script.py

from engine.globs import GameState
from engine.globs.event_dispatcher import EventDispatcher
from engine.misc.resources import load_module_from_script


def boton_step(nombre, data):
    GameState.set(nombre + '.pressed', data['pressed'])
    EventDispatcher.trigger('button_activated', 'boton', {})


def door_activate(puerta, event):
    del event  # es irrelevante, pero EventDispatcher llama la funcion con dos argumentos.
    btn1_activo = GameState.get('boton_azul.pressed')
    btn2_activo = GameState.get('boton_verde.pressed')
    if btn1_activo and btn2_activo:
        puerta.operar(1)
    else:
        puerta.operar(0)
    GameState.set('puerta.open', btn1_activo and btn2_activo)
    # este valor lo puede usar la rutina de load game para setear el estado correcto del objeto


def init_game(event):
    # event tendria data de si el juego es nuevo o es un savegame.
    from engine.globs import EngineData

    data = {"mapa": "prueba",
            "entrada": "bottomright",
            "tiempo": [0, 0, 0],
            "focus": "heroe"}

    if 'savegame' in event.data:
        data.update(event.data['savegame'])

    EngineData.cargar_juego(data)


def init_system(event):
    if event.data['intro']:
        _module = load_module_from_script('intro')

        # se supone que el modder sabe cómo se llama la función
        getattr(_module, 'creditos_introduccion')()
    EventDispatcher.trigger('OpenMenu', 'Script', {'value': 'Principal'})


EventDispatcher.register(init_system, 'InitSystem')
EventDispatcher.register(init_game, 'NewGame')
