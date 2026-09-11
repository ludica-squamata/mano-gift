from engine.globs.event_dispatcher import EventDispatcher
from engine.mobs.behaviourtrees import Leaf, Failure, Success
from engine.mobs.scripts.a_star import Nodo, a_star
from engine.globs.game_state import Game_State
from engine import Mob_Group
from math import trunc


class HasSetLocation(Leaf):
    def process(self):
        e = self.get_entity()
        # get the location set by another entity
        loc = Game_State.get2(e.nombre)

        if loc:
            nodo = Nodo(*loc, 32)
            self.tree.set_context('punto_final', nodo)
            # reset the flag to prevent infinite loop
            Game_State.del2(e.nombre)
            return Success
        else:
            return Failure


def exit_event(event):
    mob = event.data['mob']
    mob['AI'].set_context('go to', event.data['pos'])
    Game_State.set2(f"{event.data['mob']}.goto.{event.data['pos']}")


EventDispatcher.register(exit_event, "Exit")


class ReachExit(Leaf):
    def process(self):
        e = self.get_entity()
        if e.last_map is not None:
            mapa = e.last_map
            if mapa.mascara_salidas.overlap(e.mask, (e.rel_x, e.rel_y)) is not None:
                r, g, b, a = e.parent.imagen_salidas.get_at((e.rel_x, e.rel_y))
                e.parent.salidas[b * 255 + g].trigger(e)

        return Success


class IsItNightTime(Leaf):
    def process(self):
        if Game_State.get2('NightTime'):
            return Success
        else:
            return Failure


class IsThereABed(Leaf):
    def process(self):
        e = self.get_entity()
        if e.last_map is None:
            return Failure
        points_of_interest = e.last_map.points_of_interest
        point = [points_of_interest[point] for point in points_of_interest if point == 'bed']

        if len(point):
            self.tree.set_context('bed', point[0].nodo)
            # print(f"{e.nombre}: 'phew! there is a bed. I'm going to sleep.")
            return Success
        else:
            # print(f"{e.nombre}: 'shit! there is no bed in this map!")
            return Failure


class GoToBed(Leaf):
    def process(self):
        bed = self.tree.get_context('bed')
        self.tree.set_context('punto_final', bed)
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
        e = self.get_entity()
        mobs = [mob for mob in Mob_Group if mob != e]
        self.tree.set_context('others', mobs)
        return Success


class WhereAreOthers(Leaf):
    def process(self):
        e = self.get_entity()
        mobs = [entity for entity in e.perceived['seen'] if entity.tipo == "Mob" and entity != e]
        mob_routes = {}
        for mob in mobs:
            mob_id = mob.id
            tree = mob['AI']
            ruta = tree.get_context('camino')
            mob_routes[mob_id] = ruta

        self.tree.set_context('other_routes', mob_routes)

        return Success


class CheckRoute(Leaf):
    def process(self):
        entity = self.get_entity()
        camino = self.tree.get_context('camino')
        mapa = self.tree.get_context('mapa')
        proximo = self.tree.get_context('next')
        others = self.tree.get_context('others')
        evaded = self.tree.get_context('evaded')

        m_g = Mob_Group.contents()

        nodos = [Nodo(trunc(m.rel_x / 32) * 32, trunc(m.rel_y / 32) * 32, m.current_adress) for m in m_g if m != entity]
        restante = camino[proximo:]
        occupied = [i for i, nodo in enumerate(restante) if nodo in nodos]

        if len(occupied) and not evaded:
            print('aca')
            oc = occupied[0] # Posición del obstáculo dentro de "restante"; por ahora es solo 1.

            rango = 2 # Dos nodos antes y dos nodos después; "2" podría ser configurable segun la visión del mob.
            inicio = max(0, oc - rango)
            fin = min(len(restante) - 1, oc + rango)

            nuevo_inicio = restante[inicio]
            nuevo_objetivo = restante[fin]

            nuevo_camino = a_star(nuevo_inicio, nuevo_objetivo, mapa, others)
            restante[inicio:fin + 1] = nuevo_camino

            camino[proximo:] = restante # reemplazamos el segmento del camino ocupado

            self.tree.set_context('camino', camino)
            self.tree.set_context('evaded', True)

        return Success