from engine.globs import Constants as Cs, EngineData as Ed
from engine.misc import Config
from pygame import event
from pygame import KEYDOWN, KEYUP
from pygame import JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, JOYAXISMOTION


def filtrar_eventos_teclado(events):
    teclas = Cs.TECLAS.devolver()
    for _event in events:
        if _event.type == KEYDOWN:
            if Ed.setKey:
                event.post(event.Event(Cs.TAP, {'key': _event.key, 'type': 'tapping'}))
            if _event.key in teclas:
                teclas[_event.key]['pressed'] = True

        elif _event.type == KEYUP:
            if _event.key in teclas:
                key = teclas[_event.key]
                key['pressed'] = False
                if not key['hold']:
                    key['tap'] = True
                else:
                    key['release'] = True

    return teclas


def filtrar_eventos_gamepad(events):
    teclas = Cs.TECLAS.devolver()
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
            key['held'] += 1
        else:
            key['hold'] = False
            key['holding'] = 0
            if not key['release']:
                key['held'] = 0

        if key['holding'] > holding:
            key['hold'] = True
            key['tap'] = False

        if key['hold']:
            event.post(event.Event(Cs.HOLD, {'key': key['key'], 'type': 'holding', 'holding': key['holding']}))

        elif key['tap']:
            event.post(event.Event(Cs.TAP, {'key': key['key'], 'type': 'tapping'}))
            key['tap'] = False

        elif key['release']:
            event.post(event.Event(Cs.RELEASE, {'key': key['key'], 'type': 'release', 'holding': key['held']}))
            key['release'] = False
            key['held'] = 0

    return event.get()
