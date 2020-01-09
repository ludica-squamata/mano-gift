from engine.base.azoe_sprite import AzoeSprite
from engine.globs.mod_data import ModData


class Caracterizado(AzoeSprite):
    _chars = None  # un diccionario con las caracteristicas y sus valores
    _allchars = None  # una lista con todos los nombres de caracteristicas, por si acaso

    def __init__(self, *args, **kwargs):
        """Ignora cuáles son los atributos o para qué se usan, esa decisión depende
        enteramente del modder."""
        self._chars = {}
        self._allchars = []
        super().__init__(**kwargs)
        for attr in self.data['atributos']:
            self._chars[attr] = self.data['atributos'][attr]
            self._allchars.append(attr)

        for char in ModData.data['caracteristicas']:
            if char in self._chars:
                for sub in ModData.data['caracteristicas'][char]:
                    # acá habría que hacer algún cambio a la D&D, pero eso tendría que determinarlo el mooder.
                    self._chars[sub] = self._chars[char]
                    self._allchars.append(sub)

    def __getitem__(self, item):
        if item in self._chars:
            return self._chars[item]

    def __setitem__(self, key, value):
        self._chars[key] = value

    def __delitem__(self, key):
        if key in self._chars:
            self._chars[key] = 0

    def __contains__(self, item):
        return item in self._allchars

    def mover(self, dx, dy):
        dx *= 3
        dy *= 3
        return dx, dy
