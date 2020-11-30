from engine.globs.event_dispatcher import EventDispatcher
# from engine.globs import Mob_Group
from pygame import draw, Surface, SRCALPHA
from engine.globs.tiempo import Tiempo


class LightSource:
    """Los objetos de esta clase tienen un area de luz, que permite ver y genera sombras"""
    origen = None
    # una coordenada desde donde se calcula el area.
    # por ejemplo para un poste con iluminacion en la punta? por defecto center

    estatico = False  # para simular luces lejanas, como el sol. no les cambia el rect.pos
    encendido = True  # apaguen esas luces!
    # animacion???

    def __init__(self, nombre, radius, x, y):
        self.nombre = nombre
        self.image = Surface((radius * 2, radius * 2), SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

        # TODO: no se ve el circulo no importa cuál sea el radio. Puede ser un problema de Noche.set_lights()
        draw.circle(self.image, (0, 0, 0, 230), self.rect.center, 1)

    def update(self):
        if Tiempo.noche is not None and not self.encendido:
            Tiempo.noche.set_lights([self])
            self.encendido = True

    def __repr__(self):
        return 'LightSource of ' + self.nombre


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
