from .props import *


def new_prop(nombre, x, y, z=0, data=None, img=None):
    if data is None and img is None:
        raise TypeError
    elif data is None:
        data = {}

    args = nombre, x, y, z, data
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
        prop = Estructura3D(nombre, x, y, data).props
    else:
        prop = Escenografia(nombre, x, y, z=z, data=data, imagen=img)

    if type(prop) is list:
        try:
            flat = [item for sublist in prop for item in sublist]
            return flat
        except TypeError:
            return prop
    else:
        return prop
