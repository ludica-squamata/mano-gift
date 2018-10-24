from engine.globs import EngineData, TECLADO, GAMEPAD
from engine.globs.event_dispatcher import EventDispatcher
from engine.misc import Config
from pygame import event, joystick
from pygame.key import get_pressed
from pygame import KEYDOWN, KEYUP, K_ESCAPE, QUIT
from pygame import JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, JOYAXISMOTION
from .teclas import Teclas

pressed_keys = []


def init():
    event.set_blocked([1, 4, 5, 6, 17])  # all mouse- and video-related events
    for idx in range(joystick.get_count()):
        joystick.Joystick(idx).init()


def filtrar_eventos_teclado(events):
    teclas = Teclas.key_dict
    global pressed_keys

    for _event in events:
        if _event.type == KEYDOWN:
            if _event.key in teclas and not EngineData.setKey:
                teclas[_event.key]['pressed'] = True
                pressed_keys.append(_event.key)

        elif _event.type == KEYUP:
            if EngineData.setKey:
                EventDispatcher.trigger('SetNewKey', 'System', {'device': 'teclado', 'key': _event.key})

            elif _event.key in teclas:
                key = teclas[_event.key]
                key['pressed'] = False
                if _event.key in pressed_keys:
                    pressed_keys.remove(_event.key)

                if not key['hold']:
                    key['tap'] = True
                else:
                    key['release'] = True
            else:
                EventDispatcher.trigger('WrongKey', 'System', {'key': _event.key})

    # este bloque previene el salteo del KEYUP en un momento de lag.
    _keys = get_pressed()
    for _key in pressed_keys:
        if not _keys[_key]:
            key = teclas[_key]
            key['pressed'] = False
            pressed_keys.remove(_key)
            if not key['hold']:
                key['tap'] = True
            else:
                key['release'] = True

    return teclas


def filtrar_eventos_gamepad(events):
    teclas = Teclas.key_dict.copy()
    # acá pongo "constantes" para las flechas
    flecha_derecha = 10
    flecha_izquierda = 11
    flecha_abajo = 12
    flecha_arriba = 13
    # aunque no es correcto porque el usuario puede querer cambiar
    # el uso de las teclas (invertirlas por ejemplo), y estas constantes
    # previenen eso.

    for _event in events:
        if _event.type == JOYBUTTONDOWN:
            # si recuerdo bien, 10 y 11 son los botones de start y select
            if _event.button not in (10, 11):
                b = _event.button
            else:
                b = _event.button - 2

            if b in teclas:
                teclas[b]['pressed'] = True

        elif _event.type == JOYBUTTONUP:
            if _event.button not in (10, 11):
                b = _event.button
            else:
                b = _event.button - 2

            if EngineData.setKey:
                EventDispatcher.trigger('SetNewKey', 'System', {'device': 'gamepad', 'key': b})

            elif b in teclas:
                teclas[b]['pressed'] = False
                if not teclas[b]['hold']:
                    teclas[b]['tap'] = True
                else:
                    teclas[b]['release'] = True

        elif _event.type == JOYHATMOTION:
            # las flechas del gamepad
            x, y = _event.value
            b = 0
            if x > 0:
                b = flecha_derecha
            elif x < 0:
                b = flecha_izquierda
            elif y > 0:
                b = flecha_abajo
            elif y < 0:
                b = flecha_arriba

            if b:
                teclas[b]['pressed'] = True
            else:  # button up
                if teclas[b]['pressed']:
                    teclas[b]['pressed'] = False
                    if teclas[b]['hold']:
                        teclas[b]['release'] = True
                    else:
                        teclas[b]['tap'] = True

        elif _event.type == JOYAXISMOTION:
            # los axis son los controles analógicos, las "palancas"
            # que están en los gamepads de PlayStation 2, por ejemplo.
            value = round(_event.value, 2)
            axis = _event.axis

            b = 0
            # en este engine no hacemos distincion entre las palancas y
            # las flechas (ver arriba). Por eso tienen los mismos números.

            if axis == 0:  # axis 0 es la palanca de la derecha, a izquierda y derecha
                if value > 0:
                    b = flecha_derecha
                elif value < 0:
                    b = flecha_izquierda

            elif axis == 1:  # axis 1 es la palanca de la derecha, arriba y abajo
                if value > 0:
                    b = flecha_abajo
                elif value < 0:
                    b = flecha_arriba

            # hay también otros dos axis 2 y 3, que representan los ejes x e y
            # de la palanca analógica de la izquierda. En este engine no tienen
            # uso.
            if b:
                teclas[b]['pressed'] = True
            else:
                if teclas[b]['pressed']:
                    teclas[b]['pressed'] = False
                    if teclas[b]['hold']:
                        teclas[b]['release'] = True
                    else:
                        teclas[b]['tap'] = True
    return teclas


def get_events(holding=100):
    input_device = Config.dato('metodo_de_entrada')
    teclas = None

    events = event.get()
    if input_device == TECLADO:
        teclas = filtrar_eventos_teclado(events)
    elif input_device == GAMEPAD:
        teclas = filtrar_eventos_gamepad(events)

    for _event in events:
        if _event.type == QUIT:
            EventDispatcher.trigger('QUIT', 'System', {'status': 'normal'})

        elif _event.type == KEYDOWN:
            if _event.key == K_ESCAPE:
                EventDispatcher.trigger('QUIT', 'System', {'status': 'normal'})

    event.clear([KEYDOWN, KEYUP])
    # por si fueran a provocar errores

    for tcl in teclas:
        key = teclas[tcl]
        if key.get('pressed', False):
            key['holding'] += 10
            key['held'] += 10
        else:
            key['hold'] = False
            key['holding'] = 0
            if not key.get('release', False):
                key['held'] = 0

        if key['holding'] > holding:
            key['hold'] = True
            key['tap'] = False

        if key.get('hold', False):
            data = {'nom': key['nom'], 'type': 'hold', 'value': key['holding']}
            EventDispatcher.trigger('Key', 'Modo.' + EngineData.MODO, data)

        elif key.get('tap', False):
            data = {'nom': key['nom'], 'type': 'tap'}
            EventDispatcher.trigger('Key', 'Modo.' + EngineData.MODO, data)
            key['tap'] = False

        elif key.get('release', False):
            data = {'nom': key['nom'], 'type': 'release', 'value': key['held']}
            EventDispatcher.trigger('Key', 'Modo.' + EngineData.MODO, data)
            key['release'] = False
            key['held'] = 0
