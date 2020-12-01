from engine.globs.event_dispatcher import EventDispatcher
from pygame import draw, Surface, SRCALPHA


class LightSource:
    """Los objetos de esta clase tienen un area de luz, que permite ver y genera sombras"""
    origen = None
    # una coordenada desde donde se calcula el area.
    # por ejemplo para un poste con iluminacion en la punta? por defecto center

    estatico = False  # para simular luces lejanas, como el sol. no les cambia el rect.pos
    encendido = False  # apaguen esas luces!
    # animacion???

    def __init__(self, parent, nombre, data, x, y):
        self.parent = parent
        radius = data['proyecta_luz']
        self.origen = data['origen']

        self.nombre = nombre
        self.image = Surface((radius * 2, radius * 2), SRCALPHA)
        self.image.fill((1, 1, 1, 255))
        self.rect = self.image.get_rect()
        self.rect.right = x+self.origen[0]
        self.rect.bottom = y+self.origen[1]

        draw.circle(self.image, (255, 0, 0, 15), (self.rect.w//2, self.rect.h//2), radius)

    def update(self):
        noche = self.parent.stage.noche
        if not self.encendido:
            noche.set_light(self)
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
