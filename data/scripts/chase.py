from engine.mobs.behaviortrees import Leaf, Success, Failure
from engine.globs import EngineData as Ed, MobGroup


class GetMobPos(Leaf):
    def process(self):
        cuadros = Ed.MAPA_ACTUAL.grilla
        self.tree.clear_context()

        self.tree.set_context('mapa', cuadros)
        self.tree.set_context('next', 0)

        if 'heroe' in MobGroup:
            mob_pos = MobGroup['heroe'].mapRect
        else:
            return Failure

        punto = cuadros[mob_pos.x//32, mob_pos.y//32]
        self.tree.set_context('punto_final', punto)

        return Success
