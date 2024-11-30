from engine.misc.resources import abrir_json
from .props import *
from .items import *


def new_prop(parent, x, y, z=0, nombre=None, data=None, img=None):
    if data is None and img is None:
        raise TypeError
    elif data is None:
        data = {}

    tipo = data.get('tipo')
    if tipo == 'agarrable':
        prop = Agarrable(parent, x, y, z, data)
    elif tipo == 'movible':
        prop = Movible(parent, x, y, z, data)
    elif tipo == 'trepable':
        prop = Trepable(parent, x, y, z, data)
    elif tipo == 'operable':
        prop = Operable(parent, x, y, z, data)
    elif tipo == 'destruible':
        prop = Destruible(parent, x, y, z, data)
    elif tipo == 'estructura_compuesta':
        prop = EstructuraCompuesta(parent, x, y, data).props
    elif tipo == 'contenedor':
        prop = Contenedor(parent, x, y, z, data)
    else:
        prop = Escenografia(parent, x, y, z=z, nombre=nombre, data=data, imagen=img)

    if type(prop) is list:
        try:
            flat = [item for sublist in prop for item in sublist]
            return flat
        except TypeError:
            return prop
    else:
        return prop


def new_item(parent, nombre, ruta_or_data):
    if type(ruta_or_data) is str:  # ruta
        data = abrir_json(ruta_or_data)
    elif type(ruta_or_data) is dict:
        data = ruta_or_data
    else:
        raise TypeError('Incorrect data')

    subtipo = data['subtipo']
    item = None
    if subtipo == 'consumible':
        item = Consumible
    elif subtipo == 'equipable':
        item = Equipable
    elif subtipo == 'armadura':
        item = Armadura
    elif subtipo == 'arma':
        item = Arma
    elif subtipo == 'accesorio':
        item = Accesorio
    elif subtipo == 'pocion':
        item = Pocion
    elif subtipo == 'utilizable':
        item = Utilizable

    return item(parent, nombre, data)
