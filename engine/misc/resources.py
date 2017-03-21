from pygame import image, Rect
from importlib import machinery
import json


class Resources:
    """Los métodos de esta clase permiten cargar imágenes, sonidos, etc."""

    @staticmethod
    def cargar_imagen(ruta):
        from engine.globs.mod_data import ModData
        ar = image.load(ModData.graphs + ruta).convert_alpha()
        return ar

    @staticmethod
    def split_spritesheet(ruta, w=32, h=32):
        spritesheet = Resources.cargar_imagen(ruta)
        ancho = spritesheet.get_width()
        alto = spritesheet.get_height()
        tamanio = w, h
        sprites = []
        for y in range(int(alto / h)):
            for x in range(int(ancho / w)):
                sprites.append(spritesheet.subsurface(Rect(((int(ancho / (ancho / w)) * x,
                                                             int(alto / (alto / h)) * y),
                                                            tamanio))))
        return sprites

    @staticmethod
    def abrir_json(archivo):
        """
        :param archivo:
        :type archivo:str
        :return:
        :rtype: dict
        """
        ex = open(archivo, 'r')
        data = json.load(ex)
        ex.close()
        return data

    @staticmethod
    def guardar_json(archivo, datos):
        ex = open(archivo, 'w')
        json.dump(datos, ex, sort_keys=True, indent=4, separators=(',', ': '))
        ex.close()

    @staticmethod
    def load_module_from_script(name):
        from engine.globs.mod_data import ModData
        ruta = ModData.fd_scripts + name + '.py'
        module = machinery.SourceFileLoader("module.name", ruta).load_module()
        return module

    @staticmethod
    def raw_load_module(ruta):
        module = machinery.SourceFileLoader("module.name", ruta).load_module()
        return module
