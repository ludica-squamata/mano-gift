from pygame.sprite import LayeredUpdates, Sprite


class AzoeGroup(LayeredUpdates):
    def __init__(self, name, *sprites, **kwargs):
        self.name = name
        super().__init__(sprites, kwargs)
    
    def __repr__(self):
        return "<%s[%d]>" % (self.name, len(self))


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
