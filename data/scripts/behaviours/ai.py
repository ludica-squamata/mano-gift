from engine.globs.event_dispatcher import EventDispatcher
from engine.mobs.behaviortrees import Leaf, Failure, Success
from engine.mobs.scripts.a_star import Nodo
from engine.globs.game_state import GameState


class HasSetLocation(Leaf):
    def process(self):
        e = self.get_entity()
        # get the location set by another entity
        loc = GameState.get(e.nombre, False)

        if loc:
            nodo = Nodo(*loc, 32)
            self.tree.set_context('punto_final', nodo)
            # reset the flag to prevent infinite loop
            GameState.set(e.nombre, False)
            return Success
        else:
            return Failure


def exit_event(event):
    GameState.set(event.data['mob'], event.data['pos'])


EventDispatcher.register(exit_event, "Exit")


class ReachExit(Leaf):
    def process(self):
        e = self.get_entity()
        rect = e.mapRect
        mapa = e.stage
        if mapa.mascara_salidas.overlap(e.mask, rect.topleft) is not None:
            r, g, b, a = mapa.imagen_salidas.get_at(rect.topleft)
            mapa.salidas[b * 255 + g].trigger(e)

        return Success
