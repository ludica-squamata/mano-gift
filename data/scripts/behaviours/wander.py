from engine.mobs.scripts.a_star import a_star, determinar_direccion, Nodo
from engine.mobs.behaviourtrees import Leaf, Success, Failure, Running
from engine.globs.renderer import Camara
from engine.misc import ReversibleDict
from random import randrange, choice
from math import trunc


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
        camino = []
        if e.x % 32 != 0 or e.y % 32 != 0:  # alinear con celda si se guardó en cualquier lado
            x = trunc(e.x / 32) * 32
            y = trunc(e.y / 32) * 32
            camino.append([x, y])
        else:
            x = randrange(32, 32 * 23, 32)
            y = randrange(32, 32 * 23, 32)

        camino.append([x, y])
        e.direccion = determinar_direccion([e.x, e.y], [x, y])
        self.tree.set_context('ticks', 0)
        self.tree.set_context('punto_final', [x, y])
        self.tree.set_context('camino', camino)

        return Success


class GetRoute(Leaf):
    def process(self):
        e = self.get_entity()
        mapa = self.tree.get_context('mapa')
        prox = self.tree.get_context('next')
        pd = self.tree.get_context('punto_final')
        others = self.tree.get_context('others')
        others = others if others is not False else []
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
        if not (pd.x / 32).is_integer():
            pd_x = round((pd.x / 32)) * 32
            post_x = pd.x
        else:
            pd_x = pd.x

        if not (pd.y / 32).is_integer():
            pd_y = round((pd.y / 32)) * 32
            post_y = pd.y
        else:
            pd_y = pd.y

        if pd_x is not None or pd_y is not None:
            pd = Nodo(pd_x, pd_y, 32)
            self.tree.set_context('punto_final', pd)
        try:
            ruta = a_star(pi, pd, mapa, others)

        except RuntimeError:
            self.tree.erase_keys('mapa', 'next', 'camino', 'punto_proximo', 'punto_final')
            return Failure

        if ruta is None or len(ruta) == 1:
            self.tree.erase_keys('mapa', 'next', 'camino', 'punto_proximo', 'punto_final')
            return Failure

        if pre_x is not None or pre_y is not None:
            if pre_x is None:
                pre_x = pi_x
            if pre_y is None:
                pre_y = pi_y
            punto = Nodo(pre_x, pre_y, 32)
            ruta.insert(0, punto)

        if post_x is not None or post_y is not None:
            if pre_x is None:
                post_x = pi_x
            if pre_y is None:
                post_y = pi_y
            punto = Nodo(post_x, post_y, 32)
            ruta.append(punto)

        if ruta is None or len(ruta) == 1:
            self.tree.erase_keys('mapa', 'next', 'camino', 'punto_proximo', 'punto_final')
            return Failure

        self.tree.set_context('camino', ruta)
        self.tree.set_context('punto_proximo', ruta[prox])
        return Success

def direccion_alinear(e):
    dx = e.x % 32
    dy = e.y % 32

    if dx != 0:
        return 'izquierda' if dx > 16 else 'derecha'
    if dy != 0:
        return 'arriba' if dy > 16 else 'abajo'

    return None

class NextPosition(Leaf):
    def process(self):
        entity = self.get_entity()
        camino = self.tree.get_context('camino')
        proximo = self.tree.get_context('next')
        punto_final = self.tree.get_context('punto_final')
        punto = camino[proximo] if proximo < len(camino) else punto_final
        curr_p = [entity.x, entity.y]

        def esta_alineado(e):
            return e.x % 32 == 0 and e.y % 32 == 0



        if not esta_alineado(entity):
            entity.direccion = direccion_alinear(entity)
            return Success

        if curr_p == punto:
            if proximo + 1 < len(camino):
                self.tree.set_context('next', proximo + 1)
                entity.direccion = determinar_direccion(curr_p, punto)

        if curr_p == punto_final:
            self.tree.erase_keys('punto_final', 'camino', 'next')
            return Failure
        else:
            entity.direccion = determinar_direccion(curr_p, punto_final)
            return Success


class Move(Leaf):
    def process(self):
        e = self.get_entity()
        x, y = e.direcciones[e.direccion]
        ticks = self.tree.get_context('ticks')
        ticks += 1
        self.tree.set_context('ticks', ticks)
        e.mover(x, y)
        if e.x % 32 == 0 and e.y % 32 == 0:
            self.tree.set_context('ticks', 0)
            return Success
        if ticks >= 32:
            # 🔥 forzar realineación, no éxito
            e.direccion = direccion_alinear(e)
            self.tree.set_context('ticks', 0)
            return Running
        else:
            return Running


class GetMap(Leaf):
    def process(self):
        if Camara.current_map is not None:
            cuadros = Camara.current_map.mask
            self.tree.erase_keys('mapa', 'next', 'camino', 'punto_proximo', 'punto_final')
            self.tree.set_context('mapa', cuadros)
            self.tree.set_context('next', 0)
            self.tree.set_context('movement', [0, 0])
            return Success
        else:
            return Failure


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
