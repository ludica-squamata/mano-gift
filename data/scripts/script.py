# script.py

from engine.globs import ModState
from engine.globs.eventDispatcher import EventDispatcher


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
