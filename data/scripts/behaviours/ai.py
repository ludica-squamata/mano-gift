from engine.globs.event_dispatcher import EventDispatcher
from engine.mobs.behaviourtrees import Leaf, Failure, Success
from engine.mobs.scripts.a_star import Nodo
from engine.globs.game_state import Game_State


class HasSetLocation(Leaf):
    def process(self):
        e = self.get_entity()
        # get the location set by another entity
        loc = Game_State.get2(e.nombre)

        if loc:
            nodo = Nodo(*loc, 32)
            self.tree.set_context('punto_final', nodo)
            # reset the flag to prevent infinite loop
            Game_State.del2(e.nombre)
            return Success
        else:
            return Failure


def exit_event(event):
    mob = event.data['mob']
    mob.AI.set_context('go to', event.data['pos'])
    Game_State.set2(f"{event.data['mob']}.goto.{event.data['pos']}")


EventDispatcher.register(exit_event, "Exit")


class ReachExit(Leaf):
    def process(self):
        e = self.get_entity()
        if e.parent.mascara_salidas.overlap(e.mask, (e.x, e.y)) is not None:
            r, g, b, a = e.parent.imagen_salidas.get_at((e.x, e.y))
            e.parent.salidas[b * 255 + g].trigger(e)

        return Success


class IsItNightTime(Leaf):
    def process(self):
        if Game_State.get2('NightTime'):
            return Success
        else:
            return Failure


class IsThereABed(Leaf):
    def process(self):
        e = self.get_entity()
        if 'bed' in e.parent.parent.points_of_interest.get(e.parent.nombre, {}):
            self.tree.set_context('bed', e.parent.parent.points_of_interest[e.parent.nombre]['bed'])
            # print(f"{e.nombre}: 'phew! there is a bed. I'm going to sleep.")
            return Success
        else:
            # print(f"{e.nombre}: 'shit! there is no bed in this map!")
            return Failure


class GoToBed(Leaf):
    def process(self):
        bed = self.tree.get_context('bed')
        self.tree.set_context('punto_final', Nodo(*bed))
        self.tree.set_context('in_bed', True)
        return Success


class IsInBed(Leaf):
    def process(self):
        if self.tree.get_context('in_bed'):
            return Success
        else:
            return Failure


class DoNothing(Leaf):
    def process(self):
        e = self.get_entity()
        mobs = [mob for mob in e.parent.properties.get_sprites_from_layer(2) if mob != e]
        self.tree.set_context('others', mobs)
        return Success


class WhereAreOthers(Leaf):
    def process(self):
        e = self.get_entity()
        mobs = [entity for entity in e.perceived['seen'] if entity.tipo == "Mob" and entity != e]
        mob_routes = {}
        for mob in mobs:
            mob_id = mob.id
            if mob.AI_type == "Autonomous":
                tree = mob.AI
                ruta = tree.get_context('camino')
                mob_routes[mob_id] = ruta

        self.tree.set_context('other_routes', mob_routes)

        return Success
