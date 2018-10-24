# ModState.py
from .event_dispatcher import EventDispatcher


class GameState:
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
    def load(cls, event):
        variables = event.data.get('savegame', {}).get('variables', {})
        cls._innerdict.update(variables)

    @classmethod
    def save(cls, event):
        EventDispatcher.trigger(event.tipo + 'Data', 'GameState', {'variables': cls.variables()})

    @classmethod
    def variables(cls):
        return cls._innerdict.copy()


EventDispatcher.register(GameState.load, 'NewGame')
EventDispatcher.register(GameState.save, 'Save')
