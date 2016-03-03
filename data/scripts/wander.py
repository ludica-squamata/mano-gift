from random import randint, choice
from engine.mobs.behaviortrees import Leaf


class WanderAbout(Leaf):

    def process(self):
        self.entity.mov_ticks += 1
        if self.entity.mov_ticks == 3:
            self.entity.mov_ticks = 0
            if randint(1, 101) <= 10:  # 10% de probabilidad
                lista = list(self.entity.direcciones.keys())
                lista.remove(self.entity.direccion)
                self.entity.direccion = choice(lista)
