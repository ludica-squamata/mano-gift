# ModState.py
from .event_dispatcher import EventDispatcher


class GameState:
    _string_list = None

    # la implementación puede cambiar en el futuro
    # por un tree, un par de arrays, una db o algo así.

    @classmethod
    def init(cls):
        EventDispatcher.register_many(
            (cls.load, 'NewGame'),
            (cls.save, 'Save')
        )
        cls._string_list = []

    @classmethod
    def __contains__(cls, flag):
        """To be able to perform '<flag> in GameState'"""
        if type(flag) is str:
            return flag in cls._string_list
        else:
            raise TypeError('Flags must be just strings')

    @classmethod
    def get2(cls, flag):
        """Gets the flag if it is set, which is just the passed string, or False if the flag is not set."""
        if type(flag) is str:
            if flag in cls._string_list:
                return flag
            else:
                return False
        else:
            raise TypeError('Flags must be just strings')

    @classmethod
    def gets(cls, *flag):
        """WIP: Gets an arbitrary number of flags and only True if all of them are set, False otherwise"""
        print(flag)

    @classmethod
    def set2(cls, flag, silently=True):
        """Sets the flag only if the flag has not been already set.

        Raises a Error if the flag is already set and silently is set to False.
        """
        if type(flag) is str:
            if flag not in cls._string_list:
                cls._string_list.append(flag)
            elif not silently:
                raise ValueError()
        else:
            raise TypeError('Flags must be just strings')

    @classmethod
    def del2(cls, flag):
        """Erases/unsets the flag."""
        if flag in cls._string_list:
            index = cls._string_list.index(flag)
            del cls._string_list[index]

    # los siguientes métodos podrían cambiar en un futuro,
    # dependiendo de la implementación del guardado
    @classmethod
    def load(cls, event):
        variables = event.data.get('savegame', {}).get('variables', [])
        cls._string_list = variables if variables is not None else []

    @classmethod
    def save(cls, event):
        EventDispatcher.trigger(event.tipo + 'Data', 'GameState', {'flags': cls._string_list})

    @classmethod
    def flags(cls):
        return cls._string_list

    @classmethod
    def find(cls, prefix=None, suffix=None):
        flags = None
        if prefix is None and suffix is None:
            flags = cls.flags()
        elif prefix is not None:
            flags = [flag for flag in cls._string_list if flag.startswith(prefix)]
        elif suffix is not None:
            flags = [flag for flag in cls._string_list if flag.endswith(suffix)]

        return flags


GameState.init()
