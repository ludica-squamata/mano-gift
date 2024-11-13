# ModState.py
from .event_dispatcher import EventDispatcher


class GameState:
    _string_list = None

    # la implementación puede cambiar en el futuro
    # por un tree, un par de arrays, una db o algo así.

    def __init__(self):
        EventDispatcher.register_many(
            (self.load, 'NewGame'),
            (self.save, 'Save')
        )
        self._string_list = []

    def __contains__(self, flag):
        """To be able to perform '<flag> in Game_State'"""
        if type(flag) is str:
            return flag in self._string_list
        else:
            raise TypeError('Flags must be just strings')

    def get2(self, flag):
        """Gets the flag if it is set, which is just the passed string, or False if the flag is not set."""
        if type(flag) is str:
            if flag in self._string_list:
                return flag
            else:
                return False
        else:
            raise TypeError('Flags must be just strings')

    def gets(self, *flags):
        """Gets an arbitrary number of flags and only True if all of them are set, False otherwise"""
        return all([flag in self._string_list for flag in flags])

    def set2(self, flag, silently=True):
        """Sets the flag only if the flag has not been already set.

        Raises a Error if the flag is already set and silently is set to False.
        """
        if type(flag) is str:
            if flag not in self._string_list:
                self._string_list.append(flag)
            elif not silently:
                raise ValueError()
        else:
            raise TypeError('Flags must be just strings')

    def del2(self, flag):
        """Erases/unsets the flag."""
        if flag in self._string_list:
            index = self._string_list.index(flag)
            del self._string_list[index]

    # los siguientes métodos podrían cambiar en un futuro,
    # dependiendo de la implementación del guardado

    def load(self, event):
        variables = event.data.get('savegame', {}).get('variables', [])
        self._string_list = variables if variables is not None else []

    def save(self, event):
        EventDispatcher.trigger(event.tipo + 'Data', 'Game_State', {'flags': self._string_list})

    def flags(self):
        return self._string_list

    def find(self, prefix=None, suffix=None):
        flags = None
        if prefix is None and suffix is None:
            flags = self.flags()
        elif prefix is not None:
            flags = [flag for flag in self._string_list if flag.startswith(prefix)]
        elif suffix is not None:
            flags = [flag for flag in self._string_list if flag.endswith(suffix)]

        return flags


Game_State = GameState()

__all__ = {
    "Game_State"
}