from pygame.sprite import LayeredUpdates, Sprite
from pygame import Rect


class AzoeGroup(LayeredUpdates):
    def __init__(self, name, *sprites, **kwargs):
        self.name = name
        super().__init__(sprites, kwargs)
    
    def __repr__(self):
        return "<%s[%d]>" % (self.name, len(self))

    def get_sprites_at(self, pos):
        """Funciona como Pygame.LayeredUpdates, excepto que usa un rect válido"""
        _sprites = self._spritelist
        # en LayeredUpdates, el rect tiene un tamaño igual a 0,0.
        rect = Rect(pos, (1, 1))
        colliding_idx = rect.collidelistall(_sprites)
        colliding = [_sprites[i] for i in colliding_idx]
        return colliding


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
