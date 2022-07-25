from pygame.sprite import LayeredUpdates, Sprite
from pygame import Rect


class AzoeGroup(LayeredUpdates):
    _spritelist = None

    def __init__(self, name, *sprites, **kwargs):
        self.name = name
        self.collition_rect = Rect(0, 0, 1, 1)
        super().__init__(*sprites, **kwargs)

    def __repr__(self):
        return "<%s[%d]>" % (self.name, len(self))

    def get_spr_at(self, pos):
        _sprites = self._spritelist
        self.collition_rect.topleft = pos
        colliding_idxs = self.collition_rect.collidelist(_sprites)
        colliding = _sprites[colliding_idxs] if colliding_idxs >= 0 else None
        return colliding

    def get_spr(self, idx):
        return self.get_sprite(idx)

    def sprs(self):
        return self.sprites()


class AzoeBaseSprite(Sprite):
    """A very basic class, base for all the sprites in the engine that are not a true AzoeSprite"""

    def __init__(self, parent, nombre, image=None, rect=None):
        super().__init__()
        self.parent = parent
        self.nombre = nombre
        if image is not None:
            self.image = image
        if rect is not None:
            self.rect = rect


class ChunkGroup:
    lenght = 0

    def __init__(self):
        self._group = {}
        self._list = []

    def __getitem__(self, adress):
        if adress in self._group:
            return self._group[adress]

    def __setitem__(self, adress, value):
        if adress not in self._group:
            self._group[adress] = value
            self._list.append(value)
            self.lenght += 1

    def __delitem__(self, adress):
        if adress in self._group:
            item = self._group[adress]
            del self._group[adress]
            self._list.remove(item)
            self.lenght -= 1

    def __len__(self):
        return self.lenght

    def add(self, *chunks):
        for chunk in chunks:
            adress = chunk.adress.center
            self[adress] = chunk

    def sprs(self):
        return self._list
