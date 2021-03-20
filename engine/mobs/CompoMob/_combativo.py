from ._animado import Animado
from ._sensitivo import Sensitivo
from ._suertudo import Suertudo
from ._equipado import Equipado
from engine.globs.event_dispatcher import EventDispatcher


class Combativo(Sensitivo, Animado, Suertudo, Equipado):
    is_damageable = True

    def hurt(self, damage):
        damage -= self.dureza
        self['Salud'] -= damage
        EventDispatcher.trigger('MobWounded', self.tipo,
                                {'mob': self,
                                 "value": self['Salud'],
                                 "stat": "Salud",
                                 "factor": -damage}
                                )

        if self['Salud'] <= 0:
            if self.death_img is not None:
                self.image = self.death_img
                # esto queda hasta que haga sprites 'muertos' de los npcs
                # pero necesito más resolución para hacerlos...
            self.dead = True
            EventDispatcher.trigger('MobDeath', self.tipo, {'obj': self})

    def atacar(self, sprite):
        if super().atacar(sprite) and sprite.is_damageable:
            x, y = self.direcciones[self.direccion]

            x, y = x * self['Retroceso'], y * self['Retroceso']
            a, b = self.luck(), sprite.luck()

            if self['Ataque']+self['Nivel']+a >= sprite['Evasión']+sprite['Nivel']+b:
                EventDispatcher.trigger('AttackSuccess', self.tipo, {'victim': sprite, 'attaker': self})
                sprite.reubicar(x, y)
                sprite.hurt(self['DañoCC'])
            else:
                EventDispatcher.trigger('MissedAttack', self.tipo, {'mob': sprite})
