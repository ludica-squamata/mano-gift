from .config import Config
from pygame import quit
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
