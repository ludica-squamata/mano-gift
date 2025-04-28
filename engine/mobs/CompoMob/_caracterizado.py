from engine.base.azoe_sprite import AzoeSprite
from engine.globs.mod_data import ModData


class Caracterizado(AzoeSprite):
    _chars = None  # un diccionario con las caracteristicas y sus valores
    _allchars = None  # una lista con todos los nombres de caracteristicas, por si acaso

    def __init__(self, parent, *args, **kwargs):
        """Ignora cuáles son los atributos o para qué se usan, esa decisión depende
        enteramente del modder."""
        self._chars = {}
        self._allchars = []
        super().__init__(parent, *args, **kwargs)
        for attr in self.data['atributos']:
            self._chars[attr] = self.data['atributos'][attr]
            self._allchars.append(attr)

        for char in ModData.data['caracteristicas']:
            if char in self._chars:
                for sub in ModData.data['caracteristicas'][char]:
                    self._chars[sub] = ModData.attr_derivation(self._chars[char])
                    self._allchars.append(sub)

        for attr in ModData.custom_attr:
            ModData.custom_attr[attr](self)

    def get_chars(self):
        for attr in self.data['atributos']:
            # no sé si este generator está bien hecho. Soy nuevo en esto, pero me pareció que correspondía. 20/3/2021
            yield self._chars[attr]

    def get_attr_names(self):
        for attr in self.data['atributos']:
            yield attr

    def __getitem__(self, item):
        if type(item) == int and 0 <= item < len(self._allchars):
            return self[self._allchars[item]]
        if item in self._chars:
            return self._chars[item]
        else:  # esto viene a ser __missing__(), pero como ese método es llamado por dict.__getitem__(),
            return 1  # es más sencillo simplemente devolver lo que habría devuelto ese método.

    def __setitem__(self, key, value):
        self._chars[key] = value

    def __delitem__(self, key):
        if key in self._chars:
            self._chars[key] = 0

    def __contains__(self, item):
        return item in self._allchars

    def mover(self, dx, dy):
        dx *= self['Velocidad']  # Nótese que 'Velocidad' es una propiedad que solo tiene el mob Controllable.
        dy *= self['Velocidad']  # Otros mobs no la tienen, y por eso usan el '1' que devuelve __getitem__()
        return dx, dy
