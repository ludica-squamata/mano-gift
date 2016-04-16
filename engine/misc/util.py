from pygame import mask, PixelArray, Surface, quit as py_quit
from .config import Config
import sys


class Util:
    ##
    # crea una sombra para la imagen pasada. de momento tiene inclinacion fija
    # @param surface Surface
    # @param mask MASK
    # @return Surface
    @staticmethod
    def crear_sombra(surface, _mask=None):
        if _mask is None:
            _mask = mask.from_surface(surface)
        h = surface.get_height()
        w = surface.get_width()
        pxarray = PixelArray(Surface((int(w + h / 2), h), 0, surface))
        for x in range(w):
            for y in range(h):
                if _mask.get_at((x, y)):
                    pxarray[int(x + (h - y) / 2), y] = (0, 0, 0, 150)
        return pxarray.make_surface().convert_alpha()

    @staticmethod
    def salir(output='normal'):
        """
        una funcion unificada para cerrar todo
        :param output:
        :type output:str
        :return:None
        """
        py_quit()
        print('Saliendo...\nStatus: ' + output)
        Config.guardar()
        sys.exit()
