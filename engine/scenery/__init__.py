from .props import *
from .items import *


def new_prop(nombre, x, y, data=None, img=None):
    if data is None and img is None:
        raise TypeError
    elif data is None:
        data = {}

    args = nombre, x, y, data
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
    elif tipo == 'estructura3D':
        prop = Estructura3D(*args).props
    else:
        prop = Escenografia(nombre, x, y, data=data, imagen=img)

    return prop
