from engine.globs import EngineData as Ed, TAP, HOLD, RELEASE, TECLAS
from engine.misc import Config
from pygame import event
from pygame.key import get_pressed
from pygame import KEYDOWN, KEYUP
from pygame import JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, JOYAXISMOTION

pressed_keys = []

def filtrar_eventos_teclado(events):
    teclas = TECLAS.devolver()
    global pressed_keys
    
    for _event in events:
        if _event.type == KEYDOWN:
            if _event.key in teclas:
                teclas[_event.key]['pressed'] = True
                pressed_keys.append(_event.key)
            elif Ed.setKey:
                event.post(event.Event(TAP, {'key': _event.key, 'type': 'tap'}))
            
        elif _event.type == KEYUP:
            if _event.key in teclas:
                key = teclas[_event.key]
                key['pressed'] = False
                if _event.key in pressed_keys:
                    pressed_keys.remove(_event.key)
                
                if not key['hold']:
                    key['tap'] = True
                else:
                    key['release'] = True
    
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
    teclas = TECLAS.devolver()
    for _event in events:
        if _event.type == JOYBUTTONDOWN:
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

            if b in teclas:
                teclas[b]['pressed'] = False
                if not teclas[b]['hold']:
                    teclas[b]['tap'] = True
                else:
                    teclas[b]['release'] = True

        elif _event.type == JOYHATMOTION:
            x, y = _event.value
            if x > 0:
                teclas[10]['pressed'] = True
            elif x < 0:
                teclas[11]['pressed'] = True
            else:  # button up
                if teclas[10]['pressed']:
                    teclas[10]['pressed'] = False
                    if teclas[10]['hold']:
                        teclas[10]['release'] = True
                    else:
                        teclas[10]['tap'] = True

                if teclas[11]['pressed']:
                    teclas[11]['pressed'] = False
                    if teclas[11]['hold']:
                        teclas[11]['release'] = True
                    else:
                        teclas[11]['tap'] = True

            if y > 0:
                teclas[12]['pressed'] = True
            elif y < 0:
                teclas[13]['pressed'] = True
            else:  # button up
                if teclas[12]['pressed']:
                    teclas[12]['pressed'] = False
                    if teclas[12]['hold']:
                        teclas[12]['release'] = True
                    else:
                        teclas[12]['tap'] = True

                if teclas[13]['pressed']:
                    teclas[13]['pressed'] = False
                    if teclas[13]['hold']:
                        teclas[13]['release'] = True
                    else:
                        teclas[13]['tap'] = True

        elif _event.type == JOYAXISMOTION:
            value = round(_event.value, 2)
            axis = _event.axis

            if axis == 0:  # x
                if value > 0:
                    teclas[10]['pressed'] = True
                elif value < 0:
                    teclas[11]['pressed'] = True
                else:
                    if teclas[10]['pressed']:
                        teclas[10]['pressed'] = False
                        if teclas[10]['hold']:
                            teclas[10]['release'] = True
                        else:
                            teclas[10]['tap'] = True

                    if teclas[11]['pressed']:
                        teclas[11]['pressed'] = False
                        if teclas[11]['hold']:
                            teclas[11]['release'] = True
                        else:
                            teclas[11]['tap'] = True
            elif axis == 1:  # y
                if value < 0:
                    teclas[12]['pressed'] = True
                elif value > 0:
                    teclas[13]['pressed'] = True
                else:
                    if teclas[12]['pressed']:
                        teclas[12]['pressed'] = False
                        if teclas[12]['hold']:
                            teclas[12]['release'] = True
                        else:
                            teclas[12]['tap'] = True

                    if teclas[13]['pressed']:
                        teclas[13]['pressed'] = False
                        if teclas[13]['hold']:
                            teclas[13]['release'] = True
                        else:
                            teclas[13]['tap'] = True
            elif axis == 2:
                pass
            elif axis == 3:
                pass
    return teclas


def get_taphold_events(events, holding=100):
    input_device = Config.dato('metodo_de_entrada')
    teclas = None
    if input_device == 'teclado':
        teclas = filtrar_eventos_teclado(events)
    elif input_device == 'gamepad':
        teclas = filtrar_eventos_gamepad(events)

    for tcl in teclas:
        key = teclas[tcl]
        if key['pressed']:
            key['holding'] += 10
            key['held'] += 10
        else:
            key['hold'] = False
            key['holding'] = 0
            if not key['release']:
                key['held'] = 0

        if key['holding'] > holding:
            key['hold'] = True
            key['tap'] = False

        if key['hold']:
            data = {'nom': key['nom'], 'key': key['key'], 'type': 'hold', 'value': key['holding']}
            event.post(event.Event(HOLD, data))

        elif key['tap']:
            data = {'nom': key['nom'], 'key': key['key'], 'type': 'tap'}
            event.post(event.Event(TAP, data))
            key['tap'] = False

        elif key['release']:
            data = {'nom': key['nom'], 'key': key['key'], 'type': 'release', 'value': key['held']}
            event.post(event.Event(RELEASE, data))
            key['release'] = False
            key['held'] = 0

    return event.get()
