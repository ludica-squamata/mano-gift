from pygame import image, Rect, Surface, SRCALPHA
import json

__all__ = ['cargar_imagen', 'split_spritesheet', 'abrir_json', 'guardar_json', 'combine_mob_spritesheets']

_images = {}


def cargar_imagen(ruta):
    if ruta not in _images:
        _images[ruta] = image.load(ruta).convert_alpha()

    return _images[ruta]


def split_spritesheet(ruta, w=32, h=32):
    if type(ruta) is Surface:
        spritesheet = ruta
    else:
        spritesheet = cargar_imagen(ruta)
    ss = spritesheet.subsurface  # function alias
    ancho = spritesheet.get_width()
    alto = spritesheet.get_height()
    sprites = []
    dh = int(alto / h)
    dw = int(ancho / w)
    if dh == 0 or dw == 0:
        sprites.append(spritesheet)
    else:
        for y in range(dh):
            for x in range(dw):
                sprites.append(ss(Rect(((ancho / (ancho / w)) * x, (alto / (alto / h)) * y, w, h))))
    return sprites


def combine_mob_spritesheets(head_file, body_file, w=32, h=32):
    heads = split_spritesheet(head_file, w * 4, h)
    bodies = cargar_imagen(body_file)
    sprites = []
    for head in heads:
        _w, _h = head.get_size()
        new = Surface((_w, _h * 3), SRCALPHA)
        for i in range(3):
            new.blit(head, (0, i * h))
        copy = bodies.copy()
        copy.blit(new, (0, 0))
        sprites.extend(split_spritesheet(copy, w, h))

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
        json.dump(datos, file, sort_keys=True, indent=2, separators=(',', ':'), ensure_ascii=False)
