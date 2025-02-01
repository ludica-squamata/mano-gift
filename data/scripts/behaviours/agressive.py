from engine.mobs.behaviourtrees import Leaf, Failure, Success
from engine.globs.game_groups import Mob_Group
from engine.mobs.scripts.a_star import Nodo, determinar_direccion


class ObtenerObjetivo(Leaf):
    def process(self):
        mob = Mob_Group.get_by_trait("nombre", 'Apple')
        if mob is not None:
            self.tree.set_context('target', mob)
            # e = self.get_entity()
            # mobs = [mob for mob in e.parent.properties.get_sprites_from_layer(2) if mob != e]
            self.tree.set_context('others', [])
            return Success
        else:
            return Failure


class DoISeeIt(Leaf):
    def process(self):
        e = self.get_entity()
        target = self.tree.get_context('target')
        if target in e.perceived['seen']:
            # print('objetivo a la vista')
            return Success
        else:
            # print('objetivo perdido')
            return Failure

class DoIHearIt(Leaf):
    def process(self):
        e = self.get_entity()
        target = self.tree.get_context('target')
        if target in e.perceived['heard']:

            return Success
        else:
            # print('target lost')
            return Failure


class TurnToTarget(Leaf):
    def process(self):
        e = self.get_entity()
        t = self.tree.get_context('target')
        e_on_map_pos = e.rel_x, e.rel_y
        t_on_map_pos = t.rel_x, t.rel_y
        direccion = determinar_direccion(e_on_map_pos, t_on_map_pos)
        if direccion != e.direccion:
            e.cambiar_direccion(direccion)
            self.parent.parent.reset()
            return Success
        else:
            return Failure  #?

class StopIfCollide(Leaf):
    def process(self):
        entity = self.get_entity()
        target = self.tree.get_context('target')
        dx, dy = self.tree.get_context('movement')
        print(dx, dy)
        if entity.colisiona(target, dx, dy):
            entity.detener_movimiento()
            return Success
        else:
            return Failure

class AtacarObjetivo(Leaf):
    def process(self):
        print('aca')
        pass


class Abortar(Leaf):
    def process(self):
        pass

class Reset(Leaf):
    def process(self):
        self.parent.reset()
        return Success

class ObtenerPosicion(Leaf):
    def process(self):
        target = self.tree.get_context('target')
        x = target.rel_x
        y = target.rel_y
        # if target.body_direction == 'abajo':
        #     y -= 16
        # if target.body_direction == "derecha":

        n = Nodo(x, y, 32)
        self.tree.set_context('punto_final', n)
        return Success
