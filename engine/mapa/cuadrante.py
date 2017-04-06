from pygame.sprite import Group
from pygame import Rect
from engine.globs import Mob_Group
from engine.globs.eventDispatcher import EventDispatcher


class Cuadrante:
    def __init__(self, x, y, w, h):
        super().__init__()
        self.idx = x * 2 + y
        self.nombre = 'Cuadrante #'+str(self.idx)
        self.itemgroup = Group()
        self.mobgroup = Group()
        self.rect = Rect(w * x, h * y, w, h)
        EventDispatcher.register(self.event_remove, "DeleteItem")

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
        return self.rect.collidepoint(item.mapRect.topleft)

    def __getitem__(self, item):
        return item

    def __iter__(self):
        a = self.mobgroup.sprites()
        b = self.itemgroup.sprites()
        return iter(a+b)

    def update_mobs(self):
        self.mobgroup.empty()
        for mob in Mob_Group:
            if self.rect.collidepoint(mob.mapRect.topleft):
                self.mobgroup.add(mob)
                mob.idx_quadrant = self.idx

    def update(self):
        self.update_mobs()

    def __repr__(self):
        return self.nombre
