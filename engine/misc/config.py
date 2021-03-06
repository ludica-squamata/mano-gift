from .resources import abrir_json, guardar_json
from pygame import K_LEFT, K_RIGHT, K_DOWN, K_UP, K_x, K_z, K_RETURN
import os


class Config:
    # configuraciones
    data = {}
    __changed = False

    __defaults = {
        "mostrar_intro": True,
        "recordar_menus": True,
        "metodo_de_entrada": 'teclado',

        "comandos": {
            "arriba": K_UP,
            "abajo": K_DOWN,
            "derecha": K_RIGHT,
            "izquierda": K_LEFT,
            "accion": K_x,
            "menu": K_RETURN,
            "contextual": K_z,
        }
    }
    savedir = os.path.join(os.getcwd(), "save")

    @classmethod
    def cargar(cls):
        if not len(cls.data):
            if os.path.isfile(os.path.join(cls.savedir, 'config.json')):
                cls.data = abrir_json(os.path.join(cls.savedir, 'config.json'))
            else:
                cls.data = cls.defaults()
                cls.__changed = True
                cls.guardar()

        return cls.data

    @classmethod
    def defaults(cls, clave=None):
        dato = cls.__defaults
        if clave is not None:
            if not isinstance(clave, list):
                clave = clave.split('/')
            for x in clave:
                if x in dato:
                    dato = dato[x]
                else:
                    dato = None
        return dato

    @classmethod
    def dato(cls, clave=None):
        dato = cls.cargar()
        if clave is not None:
            if not isinstance(clave, list):
                clave = clave.split('/')
            for x in clave:
                if x in dato:
                    dato = dato[x]
                else:
                    dato = cls.defaults(clave)
                    break
        return dato

    @classmethod
    def asignar(cls, clave, valor):
        dato = cls.cargar()
        if not isinstance(clave, list):
            clave = clave.split('/')
        last = clave.pop()
        if len(clave) > 0:
            for x in clave:
                if x in dato:
                    dato = dato[x]
                else:
                    dato[x] = {}
                    dato = dato[x]
        dato[last] = valor
        cls.__changed = True

    @classmethod
    def guardar(cls):
        if cls.__changed:
            if not os.path.exists(cls.savedir):
                os.mkdir('save')
            guardar_json(os.path.join(cls.savedir, 'config.json'), cls.data)
