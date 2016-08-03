# ModState.py


class ModState:
    _innerdict = {}
    # la implementación puede cambiar en el futuro
    # por un tree, un par de arrays, una db o algo así.

    @classmethod
    def get(cls, key, default_value=False):
        if key in cls._innerdict:
            return cls._innerdict[key]
        else:
            return default_value

    @classmethod
    def set(cls, key, value):
        cls._innerdict[key] = value

    # los siguientes métodos podrían cambiar en un futuro,
    # dependiendo de la implementación del guardado
    @classmethod
    def load(cls, data):
        cls._innerdict = data

    @classmethod
    def save(cls):
        return cls._innerdict

    @classmethod
    def flags(cls):
        return cls._innerdict.items()
