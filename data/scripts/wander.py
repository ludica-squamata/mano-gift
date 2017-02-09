from random import choice
from engine.mobs.behaviortrees import Leaf, Success, Failure
from engine.mobs.scripts.a_star import a_star, determinar_direccion
from engine.globs import EngineData as Ed


class GetRandomDir(Leaf):
    def process(self):
        cuadros = Ed.MAPA_ACTUAL.grilla
        self.tree.shared_context.clear()

        self.tree.set_context('mapa', cuadros)
        self.tree.set_context('next', 0)

        punto = False
        while not punto:
            punto = choice(cuadros)
        self.tree.set_context('punto_final', punto)

        return Success


class GetRoute(Leaf):
    def process(self):
        e = self.get_entity()
        mapa = self.tree.get_context('mapa')
        prox = self.tree.get_context('next')
        pd = self.tree.get_context('punto_final')
        
        pi = mapa[e.mapRect.x//32, e.mapRect.y//32]
        ruta = a_star(pi, pd, mapa)
        
        self.tree.set_context('camino', ruta)
        self.tree.set_context('punto_proximo', ruta[prox])

        return Success


class NextPosition(Leaf):
    def process(self):
        e = self.get_entity()
        mapa = self.tree.get_context('mapa')
        camino = self.tree.get_context('camino')
        prox = self.tree.get_context('next')
        curr_p = mapa[e.mapRect.x//32, e.mapRect.y//32]

        if curr_p == self.tree.get_context('punto_final'):
            return Failure

        elif curr_p == camino[prox]:    
            self.tree.set_context('next', prox + 1)
            prox = self.tree.get_context('next')
            self.tree.set_context('punto_proximo', camino[prox])

        return Success


class Move(Leaf):
    def process(self):
        e = self.tree.entity
        mapa = self.tree.shared_context['mapa']
        pd = self.tree.shared_context['punto_proximo']
        pi = mapa[e.mapRect.x//32, e.mapRect.y//32]

        if pi != pd:
            direccion = determinar_direccion((pi.x, pi.y), (pd.x, pd.y))
            e.cambiar_direccion(direccion)
            e.mover()

        else:
            # Esto no deberia ser necesario.
            self.tree.reset()
            return Success
