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
        if e.rel_x % 32 != 0 or e.rel_y % 32 != 0:  # alinear con celda si se guardó en cualquier lado
            x = trunc(e.rel_x / 32) * 32
            y = trunc(e.rel_y / 32) * 32
            camino.append(Nodo(x, y,e.parent.adress))

        # x = randrange(32, 32 * 23, 32)
        # y = randrange(32, 32 * 23, 32)

        if e.current_adress == (0, 0):
            nodo = Nodo(0,0,(1,0))
        else:
            nodo = Nodo(0,0, (0, 0))
        camino.append(nodo)
        self.tree.erase_keys('regresar')
        self.tree.set_context('ticks', 0)
        self.tree.set_context('punto_final', nodo)
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
        if (e.rel_x / 32).is_integer():
            pi_x = e.rel_x
        else:
            pi_x = round((e.rel_x / 32)) * 32
            pre_x = e.rel_x

        if (e.rel_y / 32).is_integer():
            pi_y = e.rel_y
        else:
            pi_y = round((e.rel_y / 32)) * 32
            pre_y = e.rel_y

        pi = Nodo(pi_x, pi_y, e.current_adress)

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
            pd = Nodo(pd_x, pd_y, pd.adress)
            self.tree.set_context('punto_final', pd)

        ruta = a_star(pi, pd, mapa, others)

        if ruta is None or len(ruta) == 1:
            self.tree.erase_keys('mapa', 'next', 'camino', 'punto_proximo', 'punto_final')
            return Failure

        if pre_x is not None or pre_y is not None:
            if pre_x is None:
                pre_x = pi_x
            if pre_y is None:
                pre_y = pi_y
            punto = Nodo(pre_x, pre_y, e.current_adress)
            ruta.insert(0, punto)

        if post_x is not None or post_y is not None:
            if pre_x is None:
                post_x = pi_x
            if pre_y is None:
                post_y = pi_y
            punto = Nodo(post_x, post_y, tuple(pd.adress))
            ruta.append(punto)

        if ruta is None or len(ruta) == 1:
            self.tree.erase_keys('mapa', 'next', 'camino', 'punto_proximo', 'punto_final')
            return Failure

        self.tree.set_context('camino', ruta)
        self.tree.set_context('punto_proximo', ruta[prox])
        return Success


class NextPosition(Leaf):
    def process(self):
        entity = self.get_entity()
        camino = self.tree.get_context('camino')
        proximo = self.tree.get_context('next')
        punto_final = self.tree.get_context('punto_final')
        punto = camino[proximo] if proximo < len(camino) else punto_final
        curr_p = Nodo(entity.rel_x, entity.rel_y, entity.current_adress)

        if punto == curr_p:
            if proximo + 1 < len(camino):
                self.tree.set_context('next', proximo + 1)
                g_x1 = camino[proximo].adress[0] * 800 + camino[proximo].x
                g_y1 = camino[proximo].adress[1] * 800 + camino[proximo].y

                g_x2 = camino[proximo+1].adress[0] * 800 + camino[proximo+1].x
                g_y2 = camino[proximo+1].adress[1] * 800 + camino[proximo+1].y
                entity.direccion = determinar_direccion(entity.direccion, [g_x1, g_y1], [g_x2,g_y2])
                # hace que el mob no se detenga en el frame donde calcula el siguiente nodo al que ir
                x, y = entity.direcciones[entity.direccion]
                if not entity.detectar_colisiones():
                    entity.mover(x, y)
                return Success

        if punto_final == curr_p:
            self.tree.erase_keys('punto_final', 'punto_proximo', 'camino', 'next', 'adress')
            return Failure
        else:
            g_x1 = camino[proximo].adress[0] * 800 + camino[proximo].x
            g_y1 = camino[proximo].adress[1] * 800 + camino[proximo].y

            g_x2 = punto_final.adress[0] * 800 + punto_final.x
            g_y2 = punto_final.adress[1] * 800 + punto_final.y
            entity.direccion = determinar_direccion(entity.direccion, [g_x1, g_y1], [g_x2,g_y2])
            # hace que el mob no se detenga en el frame donde calcula el siguiente nodo al que ir
            x, y = entity.direcciones[entity.direccion]
            if not entity.detectar_colisiones():
                entity.mover(x, y)
            return Success


class Move(Leaf):
    def process(self):
        e = self.get_entity()
        x, y = e.direcciones[e.direccion]
        ticks = self.tree.get_context('ticks')
        ticks += 1
        self.tree.set_context('ticks', ticks)
        if not e.detectar_colisiones():
            e.mover(x, y)
        else:
            e.detener_movimiento()
            self.tree.erase_keys('punto_final', 'punto_proximo', 'camino', 'next', "ticks")
            return Failure
        if e.rel_x % 32 == 0 and e.rel_y % 32 == 0:
            self.tree.set_context('ticks', 0)
            return Success
        else:
            return Running


class GetMap(Leaf):
    def process(self):
        if Camara.current_map is not None:
            cuadros = Camara.current_map.parent
            self.tree.erase_keys('mapa', 'next', 'camino', 'punto_proximo', 'punto_final')
            self.tree.set_context('mapa', cuadros)
            self.tree.set_context('next', 0)
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
