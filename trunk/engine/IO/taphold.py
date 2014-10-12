from pygame import KEYDOWN, KEYUP, event as EVENT
from engine.globs import Constants as C

def _filtrar(events):
    teclas = C.TECLAS.devolver()
    for event in events:
        if event.type == KEYDOWN:
            if event.key in teclas:
                teclas[event.key]['pressed'] = True
                EVENT.post(event)
        
        elif event.type == KEYUP:
            if event.key in teclas:
                key = teclas[event.key]
                key['pressed'] = False
                if not key['hold']:
                    key['tap'] = True
                else:
                    key['release'] = True
    
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
            
        if key['holding'] > 100: #este limite deberia ser variable
            key['hold'] = True
            key['tap'] = False            
        
        if key['hold']:
            EVENT.post(EVENT.Event(24,{'key':key['key'],
                                       'type':'holding',
                                       'holding':key['holding']}))
        elif key['tap']:
            EVENT.post(EVENT.Event(25,{'key':key['key'],
                                       'type':'tapping'}))
            key['tap'] = False
        elif key['release']:
            EVENT.post(EVENT.Event(26,{'key':key['key'],
                                       'type':'release',
                                       'holding':key['held']
                                       }))
            key['release'] = False
            key['held'] = 0
    
    return EVENT.get()