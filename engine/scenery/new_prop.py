from .props import *


def new_prop(x, y, z=0, nombre=None, data=None, img=None):
    if data is None and img is None:
        raise TypeError
    elif data is None:
        data = {}

    args = x, y, z, data
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
        prop = Estructura3D(x, y, data).props
    else:
        prop = Escenografia(x, y, z=z, nombre=nombre, data=data, imagen=img)

    if type(prop) is list:
        try:
            flat = [item for sublist in prop for item in sublist]
            return flat
        except TypeError:
            return prop
    else:
        return prop
