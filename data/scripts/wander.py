from random import choice, randint
from engine.mobs.behaviortrees import Leaf, Success, Failure, Running
from engine.mobs.scripts.a_star import a_star, determinar_direccion
from engine.misc import ReversibleDict


class IsTalking(Leaf):
    def process(self):
        e = self.get_entity()
        if e.hablando:
            opuesta = ReversibleDict(arriba='abajo', derecha='izquierda')
            e.cambiar_direccion(opuesta[e.interlocutor.direccion])
            return Failure
        else:
            return Success


class Wait(Leaf):
    def process(self):
        e = self.get_entity()
        if randint(0, 101) == 5:
            return Success
        else:
            e.detener_movimiento()


class GetRandomDir(Leaf):
    def process(self):
        e = self.get_entity()
        cuadros = e.stage.grilla
        self.tree.clear_context()

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
        if ruta is None:
            return Failure

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
        e = self.get_entity()
        mapa = self.tree.get_context('mapa')
        pd = self.tree.get_context('punto_proximo')
        pi = mapa[e.mapRect.x//32, e.mapRect.y//32]

        if pi != pd:
            direccion = determinar_direccion((pi.x, pi.y), (pd.x, pd.y))
            if direccion != e.direccion:
                e.cambiar_direccion(direccion)
            e.mover()
            return Running
        else:
            return Success
