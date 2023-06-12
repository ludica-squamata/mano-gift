from engine.globs.event_dispatcher import EventDispatcher
from engine.mobs.behaviortrees import Leaf, Failure, Success
from engine.mobs.scripts.a_star import Nodo
from engine.globs.game_state import GameState


class HasSetLocation(Leaf):
    def process(self):
        e = self.get_entity()
        # get the location set by another entity
        loc = GameState.find(prefix=f'{e.nombre}.goto')

        if loc:
            prefix = f'{e.nombre}.goto.'
            x, y = loc[0].strip(prefix).strip('[]').split(',')
            nodo = Nodo(int(x), int(y), 32)
            self.tree.set_context('punto_final', nodo)
            # reset the flag to prevent infinite loop
            GameState.del2(loc[0])
            return Success
        else:
            return Failure


def exit_event(event):
    GameState.set2(f"{event.data['mob']}.goto.{event.data['pos']}")


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
        if GameState.get2('NightTime'):
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
        return Success
