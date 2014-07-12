from .prop import Prop
from .items import *
from .subs import *
from .subsub import *

def newProp(nombre,imagen,x,y,data=None):
    if data == None:
        prop = Prop(nombre,imagen,x,y)
    else:
        args = nombre,imagen,x,y,data
        tipo = data['tipo']
        if tipo == 'agarrable':    prop = Agarrable(*args)
        elif tipo == 'movible':    prop = Movible(*args)
        elif tipo == 'trepable':   prop = Trepable(*args)
        elif tipo == 'operable':   prop = Operable(*args)
        elif tipo == 'destruible': prop = Destruible(*args)
        elif tipo == 'equipable':  prop = Equipable(*args)
        elif tipo == 'consumible': prop = Consumible(*args)
        elif tipo == 'contenedor': prop = Contenedor(*args)
        elif tipo == 'armadura':   prop = Armadura(*args)
        elif tipo == 'arma':       prop = Arma(*args)
        elif tipo == 'pocion':     prop = Pocion(*args)
        else:                      prop = None
    
    return prop