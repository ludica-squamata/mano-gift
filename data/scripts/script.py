# script.py
from importlib import import_module
from engine.globs import GameState, ModData
from engine.globs.event_dispatcher import EventDispatcher


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
    data = {"mapa": "prueba",
            "entrada": "centre",
            "tiempo": [0, 0, 0],
            "focus": "heroe"}

    if 'savegame' in event.data:
        data.update(event.data['savegame'])

    EventDispatcher.trigger('LoadGame', 'Script', data)


def init_system(event):
    if event.data['intro']:
        module = import_module('data.scripts.intro', ModData.fd_scripts)

        # se supone que el modder sabe cómo se llama la función
        getattr(module, 'creditos_introduccion')()
    EventDispatcher.trigger('OpenMenu', 'Script', {'value': 'Principal'})


EventDispatcher.register(init_system, 'InitSystem')
EventDispatcher.register(init_game, 'NewGame')
