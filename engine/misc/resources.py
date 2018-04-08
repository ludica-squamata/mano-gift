from pygame import image, Rect
from importlib import machinery
import json

__all__ = ['cargar_imagen', 'split_spritesheet', 'abrir_json', 'guardar_json',
           'load_module_from_script', 'raw_load_module']


def cargar_imagen(ruta):
    from engine.globs.mod_data import ModData
    ar = image.load(ModData.graphs + ruta).convert_alpha()
    return ar


def split_spritesheet(ruta, w=32, h=32):
    spritesheet = cargar_imagen(ruta)
    ss = spritesheet.subsurface  # function alias
    ancho = spritesheet.get_width()
    alto = spritesheet.get_height()
    tamanio = w, h
    sprites = []
    for y in range(int(alto / h)):
        for x in range(int(ancho / w)):
            sprites.append(ss(Rect(((int(ancho / (ancho / w)) * x, int(alto / (alto / h)) * y), tamanio))))
    return sprites


def abrir_json(ruta, encoding='utf-8'):
    """
    :param ruta:
    :type ruta:str
    :param encoding:
    :type encoding: string
    :return:
    :rtype: dict
    """
    with open(ruta, 'r', encoding=encoding) as file:
        return json.load(file)


def guardar_json(ruta, datos, encoding='utf-8'):
    """
    :param datos:
    :type datos: dict
    :param ruta:
    :type ruta:str
    :param encoding:
    :type encoding: string
    """
    with open(ruta, 'w', encoding=encoding) as file:
        json.dump(datos, file, sort_keys=True, indent=2, separators=(',', ':'))


def load_module_from_script(name):
    from engine.globs.mod_data import ModData
    ruta = ModData.fd_scripts + name + '.py'
    _module = machinery.SourceFileLoader("module.name", ruta).load_module()
    return _module


def raw_load_module(ruta):
    _module = machinery.SourceFileLoader("module.name", ruta).load_module()
    return _module
