from engine.mobs.behaviortrees import Leaf, Success
from engine.mobs.scripts.a_star import Nodo


class GetHousePos(Leaf):
    def process(self):
        e = self.get_entity()
        cuadros = e.stage.mask
        salida = e.stage.parent.salidas[1]

        x, y = salida.mapRect.x, salida.mapRect.y,
        nodo = Nodo(x, y, 32)
        self.tree.clear_context()
        self.tree.set_context('SalidaIDX', 1)
        self.tree.set_context('mapa', cuadros)
        self.tree.set_context('next', 0)

        self.tree.set_context('punto_final', nodo)
        return Success


class ReachExit(Leaf):
    def process(self):
        e = self.get_entity()
        idx = self.tree.get_context('SalidaIDX')
        curr_p = Nodo(*e.mapRect.center, 32)
        if curr_p == self.tree.get_context('punto_final'):
            e.stage.parent.salidas[idx].trigger(e)
        return Success
