from ._animado import Animado
from ._sensitivo import Sensitivo
from engine.globs.event_dispatcher import EventDispatcher


class Combativo(Sensitivo, Animado):

    def recibir_danio(self, danio):
        self['Salud'] -= danio
        EventDispatcher.trigger('MobWounded', self.tipo, {'mob': self, "value": self['Salud'], "stat": "Salud"})

        if self['Salud'] <= 0:
            if self.death_img is not None:
                self.image = self.death_img
                # esto queda hasta que haga sprites 'muertos' de los npcs
                # pero necesito más resolución para hacerlos...
            self.dead = True
            EventDispatcher.trigger('MobDeath', self.tipo, {'obj': self})

    def atacar(self, sprite):
        if super().atacar(sprite):
            x, y = self.direcciones[self.direccion]

            x, y = x * self['Retroceso'], y * self['Retroceso']
            sprite.reubicar(x, y)
            sprite.recibir_danio(self['DañoCC'])
