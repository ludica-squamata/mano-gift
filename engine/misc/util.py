from .config import Config
from pygame import quit
from math import sqrt
from sys import exit


def salir(output='normal'):
    """
    una funcion unificada para cerrar todo
    :param output:
    :type output:str
    :return:None
    """
    quit()
    print('Saliendo...\nStatus: ' + output)
    Config.guardar()
    exit()


def salir_handler(event):
    data = ''
    if event.data:
        data = event.data['status']
    salir(output=data)


def euclidean(p: tuple, q: tuple):
    x1, y1 = p
    x2, y2 = q

    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)