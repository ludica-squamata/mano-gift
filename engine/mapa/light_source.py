from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import Mob_Group
from pygame import Rect


class LightSource:
    """Los objetos de esta clase tienen un area de luz, que permite ver y genera sombras"""
    origen = None
    # una coordenada desde donde se calcula el area.
    # por ejemplo para un poste con iluminacion en la punta? por defecto center

    estatico = False  # para simular luces lejanas, como el sol. no les cambia el rect.pos
    encendido = True  # apaguen esas luces!
    # animacion???
    nombre = 'luz'

    def __init__(self, item, x, y):
        self.item = item
        self.rect = Rect(0, 0, 32, 32)
        self.rect.center = item.rect.x + x, item.rect.y + y
        self.origen = self.rect.center

        EventDispatcher.register(self.update, 'MinuteFlag')

    def update(self, event):
        del event
        for mob in Mob_Group:
            mob.recibir_luz(self)

    def __repr__(self):
        x, y = str(self.rect.centerx), str(self.rect.centery)
        return 'LightSource of ' + self.item.nombre + ' @' + ','.join([x, y])


class DayLight:
    """Luz de día, ocupa toda la pantalla"""
    estatico = True

    def __init__(self, amanecer, atardecer, anochercer):
        self.nombre = 'Sol'
        self.amanece = amanecer
        self.atardece = atardecer
        self.anochece = anochercer

        # EventDispatcher.register(self.movimiento_por_rotacion, 'HourFlag')

    def movimiento_por_rotacion(self, event):
        h = event.data['hora']
        light = 0
        if h == self.amanece:
            # print('amanece')
            light = 4
        elif h == self.atardece:
            # print('atardece')
            light = 1
        elif h == self.anochece:
            # print('anochece')
            light = 0

        EventDispatcher.trigger('SolarMovement', self.nombre, {"light": light})


__all__ = ['LightSource', 'DayLight']
