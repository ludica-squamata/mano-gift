from .resources import Resources
import os

class Config:
    # configuraciones
    data = {}
    __changed = False

    __defaults = {
        "mostrar_intro": True,
        "recordar_menus": True,
        "metodo_de_entrada":'teclado',

        "teclas": {
            "arriba": 273,
            "abajo": 274,
            "derecha": 275,
            "izquierda": 276,

            "accion": 120,
            "hablar": 115,
            "cancelar": 97,
            "inventario": 122,
            "posicion": 304,

            "menu": 13,
            "debug": 282,
            "salir": 27
        },
        
        "botones":{
            "inventario": 0,
            "cancelar": 1,
            "hablar": 2,
            "accion": 3,
            "posicion": 4,
            "debug": 5,
            
            "menu": 8,
            "salir": 9,
            "derecha": 10,
            "izquierda": 11,
            "arriba": 12,
            "abajo": 13
        }
    }

    @classmethod
    def cargar(cls):
        if not len(cls.data):
            if os.path.isfile('config.json'):
                cls.data = Resources.abrir_json('config.json')
            else:
                cls.data = cls.defaults()
                cls.__changed = True
                cls.guardar()

        return cls.data

    @classmethod
    def defaults(cls, clave = None):
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
    def dato(cls, clave = None):
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
            Resources.guardar_json('config.json', cls.data)
