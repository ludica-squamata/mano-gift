from random import randint, choice
from engine.mobs.behaviortrees import Leaf, Success, Failure


class GetRandomDir(Leaf):
    def process(self):
        e = self.tree.entity
        dx, dy = 0, 0
        if randint(1,101) <= 10:
            lista = list(e.direcciones.keys())
            lista.remove(e.direccion)
            d = choice(lista)
            self.tree.shared_context['direccion'] = d
        else:
            self.tree.shared_context['direccion'] = e.direccion
        return Success


class CheckCollition(Leaf):
    def process(self):
        e = self.tree.entity
        direccion = self.tree.shared_context['direccion']
        x, y = e.direcciones[direccion]
        v = e.velocidad
        dx, dy = x * v, y * v
        if self.tree.entity.detectar_colisiones(dx, dy):
            return Failure
        else:
            return Success


class ChangeDirection(Leaf):
    def process(self):
        self.tree.entity.cambiar_direccion('contraria')
        self.tree.shared_context['direccion'] = self.tree.entity.direccion
        return Success


class Move(Leaf):
    def process(self):
        direccion = self.tree.shared_context['direccion']
        self.tree.entity.cambiar_direccion(direccion)
        self.tree.entity.mover()
        return Success
