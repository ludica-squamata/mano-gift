from pygame import quit
from .config import Config
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
