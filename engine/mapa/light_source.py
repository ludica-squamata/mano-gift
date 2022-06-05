from engine.globs.event_dispatcher import EventDispatcher
from pygame import draw, Surface, SRCALPHA, mask
from engine.globs.renderer import Camara
from engine.globs import COLOR_IGNORADO, Light_Group
from pygame.sprite import Sprite


class LightSource(Sprite):
    """Los objetos de esta clase tienen un area de luz, que permite ver y genera sombras"""
    origen = None
    # una coordenada desde donde se calcula el area.
    # por ejemplo para un poste con iluminacion en la punta? por defecto center

    encendido = False  # apaguen esas luces!
    # animacion???

    def __init__(self, parent, nombre, data, x, y, map_id=None):
        super().__init__()
        self.parent = parent
        radius = data['proyecta_luz']
        self.origen = data['origen']

        self.nombre = nombre
        self.image = Surface((radius * 2, radius * 2), SRCALPHA)
        img = self.image.copy()
        self.image.fill(COLOR_IGNORADO)
        self.rect = self.image.get_rect(center=self.parent.rect.midtop)

        # origin_rect es para la Noche
        self.origin_rect = self.rect.copy()
        self.origin_rect.right = x + self.origen[0]
        self.origin_rect.bottom = y + self.origen[1]
        self.z = self.rect.bottom

        self.stage = self.parent.stage
        self.mapRect = self.image.get_rect(center=self.origin_rect.center)
        self.mapRect.x += self.rect.w // 2
        self.mapRect.y += self.rect.h // 2

        draw.circle(self.image, (255, 255, 225, 0), (self.rect.w // 2, self.rect.h // 2), radius)
        EventDispatcher.register(self.switch, 'LightLevel')
        draw.circle(img, (255, 255, 255, 255), (self.rect.w // 2, self.rect.h // 2), radius)
        self.mask = mask.from_surface(img)
        Camara.add_real(self)
        Light_Group.add(map_id, self)

    def switch(self, event):
        noche = self.parent.stage.noche
        if event.data['level'] < 100 and not self.encendido:
            self.encendido = True
            noche.set_light(self)
        elif event.data['level'] > 200:
            self.encendido = False
            noche.unset_light(self)

    def colisiona(self, other, off_x=0, off_y=0):
        if self.nombre != other.nombre and self.encendido:
            x = self.rect.x + off_x - other.rect.x
            y = self.rect.y + off_y - other.rect.y
            if self.mask.overlap(other.mask, (-x, -y)):
                print(self, 'colisiona', x, y)
                other.recibir_luz_especular(self)
            else:
                other.desiluminar(self)

    def ubicar(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def __repr__(self):
        return 'LightSource of ' + self.nombre + ' '+str(self.parent.id)
