from .prop import *
from .items import *

def newProp(nombre,imagen,x,y,data=None):
    if data == None:
        prop = Escenografia(nombre,imagen,x,y)
    else:
        args = nombre,imagen,x,y,data
        tipo = data['tipo']
        if tipo == 'agarrable':    prop = Agarrable(*args)
        elif tipo == 'movible':    prop = Movible(*args)
        elif tipo == 'trepable':   prop = Trepable(*args)
        elif tipo == 'operable':   prop = Operable(*args)
        elif tipo == 'destruible': prop = Destruible(*args)
        else:                      prop = None
    
    return prop