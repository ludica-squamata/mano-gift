from pygame.sprite import Group
from pygame import Rect
from engine.globs import MobGroup
from engine.globs.eventDispatcher import EventDispatcher


class Cuadrante:
    def __init__(self, x, y, w, h):
        super().__init__()
        self.idx = x * 2 + y
        self.itemgroup = Group()
        self.mobgroup = Group()
        self.rect = Rect(w * x, h * y, w, h)
        EventDispatcher.register(self.event_remove, "DelItem")

    def add(self, item):
        if item.tipo == 'Mob':
            self.mobgroup.add(item)
        else:
            self.itemgroup.add(item)

        item.idx_quadrant = self.idx

    def event_remove(self, event):
        self.remove(event.data['obj'])

    def remove(self, item):
        if item.tipo == 'Mob':
            self.mobgroup.remove(item)
        else:
            self.itemgroup.remove(item)

    def contains(self, item):
        return self.rect.collidepoint((item.mapX, item.mapY))

    def __getitem__(self, item):
        return item

    def __iter__(self):
        a = self.mobgroup.sprites()
        b = self.itemgroup.sprites()
        return iter(a+b)

    def update_mobs(self):
        self.mobgroup.empty()
        for mob in MobGroup:
            if self.rect.collidepoint((mob.mapX, mob.mapY)):
                self.mobgroup.add(mob)
                mob.idx_quadrant = self.idx

    def update(self):
        self.update_mobs()
