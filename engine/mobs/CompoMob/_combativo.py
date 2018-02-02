from ._animado import Animado
from ._interactivo import Interactivo
from engine.globs.eventDispatcher import EventDispatcher


class Combativo(Animado, Interactivo):

    def recibir_danio(self, danio):
        self.salud_act -= danio
        EventDispatcher.trigger('MobWounded', self.tipo, {'mob': self})

        if self.salud_act <= 0:
            if self.death_img is not None:
                self.image = self.death_img
                # esto queda hasta que haga sprites 'muertos' de los npcs
                # pero necesito más resolución para hacerlos...
            self.dead = True
            EventDispatcher.trigger('MobDeath', self.tipo, {'obj': self})

    def atacar(self):
        if super().atacar():
            sprite = self.sprite_interaction()
            x, y = self.direcciones[self.direccion]

            x, y = x * self.fuerza, y * self.fuerza
            sprite.reubicar(x, y)
            sprite.recibir_danio(self.fuerza)
