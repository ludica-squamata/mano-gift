from pygame.sprite import LayeredUpdates


class AzoeGroup(LayeredUpdates):
    def __init__(self, name, *sprites, **kwargs):
        self.name = name
        super().__init__(sprites, kwargs)
    
    def __repr__(self):
        return "<%s[%d]>" % (self.name, len(self))
