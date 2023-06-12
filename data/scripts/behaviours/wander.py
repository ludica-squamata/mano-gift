from engine.mobs.scripts.a_star import a_star, determinar_direccion, Nodo
from engine.mobs.behaviortrees import Leaf, Success, Failure, Running
from random import randrange, choice
from engine.misc import ReversibleDict


class IsTalking(Leaf):
    def process(self):
        e = self.get_entity()
        if e.hablando:
            opuesta = ReversibleDict(arriba='abajo', derecha='izquierda')
            e.cambiar_direccion(opuesta[e.interlocutor.direccion])
            e.detener_movimiento()
            # must keep the present continous
            return Running
        else:
            # Is NOT talking, therefore, Failure.
            return Failure


class Wait(Leaf):
    def process(self):
        e = self.get_entity()
        e.detener_movimiento()
        self.tree.set_context('timer', 60 * 3)
        return Success


class GetRandomDir(Leaf):
    def process(self):
        e = self.get_entity()
        w, h = e.parent.mask.get_size()

        x = randrange(32, w, 32)
        y = randrange(32, h, 32)

        nodo = Nodo(x, y, 32)
        self.tree.set_context('punto_final', nodo)
        return Success


class GetRoute(Leaf):
    def process(self):
        e = self.get_entity()
        mapa = self.tree.get_context('mapa')
        prox = self.tree.get_context('next')
        pd = self.tree.get_context('punto_final')

        class Point:
            x = 0
            y = 0

            def __init__(self, x, y):
                self.x = x
                self.y = y

        pre_x, pre_y = None, None
        if (e.x / 32).is_integer():
            pi_x = e.x
        else:
            pi_x = round((e.x / 32)) * 32
            pre_x = e.x

        if (e.y / 32).is_integer():
            pi_y = e.y
        else:
            pi_y = round((e.y / 32)) * 32
            pre_y = e.y

        pi = Nodo(pi_x, pi_y, 32)

        post_x, post_y = None, None
        pd_x, pd_y = None, None
        if not (pd.x / 32).is_integer():
            pd_x = round((pd.x / 32)) * 32
            post_x = pd.x

        if not (pd.y / 32).is_integer():
            pd_y = round((pd.y / 32)) * 32
            post_y = pd.y

        if pd_x is not None or pd_y is not None:
            pd = Nodo(pd_x, pd_y, 32)
            self.tree.set_context('punto_final', pd)

        ruta = a_star(pi, pd, mapa)
        if pre_x is not None or pre_y is not None:
            if pre_x is None:
                pre_x = pi_x
            if pre_y is None:
                pre_y = pi_y
            punto = Point(pre_x, pre_y)
            ruta.insert(0, punto)

        if post_x is not None or post_y is not None:
            if pre_x is None:
                post_x = pi_x
            if pre_y is None:
                post_y = pi_y
            punto = Point(post_x, post_y)
            ruta.append(punto)

        if ruta is None or len(ruta) == 1:
            return Failure

        self.tree.set_context('camino', ruta)
        self.tree.set_context('punto_proximo', ruta[prox])
        return Success


class NextPosition(Leaf):
    def process(self):
        e = self.get_entity()
        camino = self.tree.get_context('camino')
        prox = self.tree.get_context('next')
        curr_p = Nodo(e.x, e.y, 32)

        if curr_p == self.tree.get_context('punto_final'):
            # there is no "next" point
            return Failure

        elif curr_p == camino[prox]:
            self.tree.set_context('next', prox + 1)
            prox = self.tree.get_context('next')
            self.tree.set_context('punto_proximo', camino[prox])
        return Success


class Move(Leaf):
    def process(self):
        e = self.get_entity()
        pd = self.tree.get_context('punto_proximo')
        pi = Nodo(e.x, e.y, 32)

        if pi != pd:
            direccion = determinar_direccion((pi.x, pi.y), (pd.x, pd.y))
            if direccion != e.direccion:
                e.cambiar_direccion(direccion)
            e.mover(*e.direcciones[direccion])
            return Running
        else:
            return Success


class GetMap(Leaf):
    def process(self):
        e = self.get_entity()
        cuadros = e.parent.mask
        self.tree.erase_keys('mapa', 'next', 'camino', 'punto_proximo', 'punto_final')

        self.tree.set_context('mapa', cuadros)
        self.tree.set_context('next', 1)
        return Success


class LookAround(Leaf):
    def process(self):
        e = self.get_entity()
        if self.tree.get_context('head_orientation') is False:
            orientacion = choice('left,right'.split(','))
            self.tree.set_context('head_orientation', orientacion)
            e.cambiar_direccion2(self.tree.get_context('head_orientation'))
        timer = self.tree.get_context('timer')
        if timer > 30:
            self.tree.set_context('timer', timer - 1)
        else:
            return Success


class KeepLooking(Leaf):
    def process(self):
        timer = self.tree.get_context('timer')
        if timer > 0:
            self.tree.set_context('timer', timer - 1)
            return Running
        else:
            self.tree.erase_keys('head_orientation', 'timer')
            return Success
