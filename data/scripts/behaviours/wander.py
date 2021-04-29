from engine.mobs.behaviortrees import Leaf, Success, Failure, Running
from engine.mobs.scripts.a_star import a_star, determinar_direccion, Nodo
from engine.globs.event_dispatcher import EventDispatcher
from engine.misc import ReversibleDict
from random import randrange, randint


class IsTalking(Leaf):
    def process(self):
        e = self.get_entity()
        if e.hablando:
            opuesta = ReversibleDict(arriba='abajo', derecha='izquierda')
            e.cambiar_direccion(opuesta[e.interlocutor.direccion])
            e.detener_movimiento()
            EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Is talking', 'pos': (400, 0)})
            # must keep the present continous
            return Running
        else:
            EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Is not talking', 'pos': (400, 0)})
            # Is NOT talking, therefore, Failure.
            return Failure


class Wait(Leaf):
    def process(self):
        e = self.get_entity()
        if randint(0, 101) <= 5:
            EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Is not waiting', 'pos': (400, 0)})
            # Is NOT waiting, therefore, Failure
            return Failure
        else:
            EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Is waiting', 'pos': (400, 0)})
            e.detener_movimiento()
            # must keep the present continous
            return Running


class GetRandomDir(Leaf):
    def process(self):
        e = self.get_entity()
        w, h = e.stage.mask.get_size()

        x = randrange(32, w, 32)
        y = randrange(32, h, 32)

        nodo = Nodo(x, y, 32)
        self.tree.set_context('punto_final', nodo)
        EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Has set a point', 'pos': (400, 0)})
        return Success


class GetRoute(Leaf):
    def process(self):
        e = self.get_entity()
        mapa = self.tree.get_context('mapa')
        prox = self.tree.get_context('next')
        pd = self.tree.get_context('punto_final')

        pi = Nodo(*e.mapRect.center, 32)
        ruta = a_star(pi, pd, mapa)
        if ruta is None or len(ruta) == 1:
            return Failure

        self.tree.set_context('camino', ruta)
        self.tree.set_context('punto_proximo', ruta[prox])
        EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Has set a route', 'pos': (400, 0)})
        return Success


class NextPosition(Leaf):
    def process(self):
        e = self.get_entity()
        camino = self.tree.get_context('camino')
        prox = self.tree.get_context('next')
        curr_p = Nodo(*e.mapRect.center, 32)

        if curr_p == self.tree.get_context('punto_final'):
            EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Has reached final point', 'pos': (400, 0)})
            # there is no "next" point
            return Failure

        elif curr_p == camino[prox]:
            self.tree.set_context('next', prox + 1)
            prox = self.tree.get_context('next')
            self.tree.set_context('punto_proximo', camino[prox])
            EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Has reached next point', 'pos': (400, 0)})
            return Success


class Move(Leaf):
    def process(self):
        e = self.get_entity()
        pd = self.tree.get_context('punto_proximo')
        pi = Nodo(*e.mapRect.center, 32)

        if pi != pd:
            direccion = determinar_direccion((pi.x, pi.y), (pd.x, pd.y))
            if direccion != e.direccion:
                e.cambiar_direccion(direccion)
            e.mover(*e.direcciones[direccion])
            EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Is moving to point', 'pos': (400, 0)})
            return Running
        else:
            EventDispatcher.trigger('DEBUG', 'Leaf', {'text': 'Has moved to point', 'pos': (400, 0)})
            return Success


class GetMap(Leaf):
    def process(self):
        e = self.get_entity()
        cuadros = e.stage.mask
        self.tree.clear_context()

        self.tree.set_context('mapa', cuadros)
        self.tree.set_context('next', 0)
        return Success
