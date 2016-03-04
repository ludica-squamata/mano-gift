from .props import *
from .items import *


def new_prop(nombre, imagen, x, y, data=None):
    if data is None:
        data = {}
    args = nombre, imagen, x, y, data
    tipo = data.get('tipo')
    if tipo == 'agarrable':
        prop = Agarrable(*args)
    elif tipo == 'movible':
        prop = Movible(*args)
    elif tipo == 'trepable':
        prop = Trepable(*args)
    elif tipo == 'operable':
        prop = Operable(*args)
    elif tipo == 'destruible':
        prop = Destruible(*args)
    else:
        prop = Escenografia(*args)

    return prop
