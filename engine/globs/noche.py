from engine.globs.azoe_group import AzoeBaseSprite
from pygame import Surface, PixelArray, SRCALPHA
from .event_dispatcher import EventDispatcher
from .colores import COLOR_IGNORADO
from .sun import Sun


class Noche(AzoeBaseSprite):
    oscurecer = False
    aclarar = False

    mod = 1

    lights = None

    images = None

    def __init__(self, parent, rect):
        img = Surface(rect.size, SRCALPHA)
        img.fill((0, 0, 0, Sun.alpha))
        self.images = {}
        self.lights = []
        super().__init__(parent, 'night block', image=img, rect=rect)
        EventDispatcher.register(self.set_darkness, 'MinuteFlag')

    def set_darkness(self, event):
        if event.tipo == 'MinuteFlag':
            if Sun.oscurecer:
                self.trasparentar(+1)

            elif Sun.aclarar:
                self.trasparentar(-1)

    def set_light(self, light):
        self.lights.append(light)

    def unset_light(self, light):
        if light in self.lights:
            self.lights.remove(light)

    def draw_lights(self):
        if Sun.alpha in self.images:
            self.image = self.images[Sun.alpha]
            # images are cached to boost performance by avoiding unnecessary PixelArraying
        else:
            self.image.fill((0, 0, 0, Sun.alpha))
            pxarray = PixelArray(self.image.copy())

            for light in self.lights:
                px_li = PixelArray(light.image)
                w, h = light.rect.size
                lx, ly = light.origin_rect.center
                for x in range(w):
                    for y in range(h):
                        color = light.image.unmap_rgb(px_li[x, y])
                        if color != COLOR_IGNORADO:
                            pxarray[x+lx, y+ly] = color

            image = pxarray.make_surface()
            self.images[Sun.alpha] = image
            self.image = image

    def trasparentar(self, mod, max_alpha=230):
        if 0 < Sun.alpha + mod <= max_alpha:
            Sun.alpha += mod
            EventDispatcher.trigger("LightLevel", "Noche", {"level": 230 - Sun.alpha})
            self.set_transparency()

    def set_transparency(self):
        self.image.fill((0, 0, 0, Sun.alpha))

    def update(self):
        self.rect.topleft = self.parent.rect.topleft
        if len(self.lights):
            self.draw_lights()
        else:
            self.set_transparency()

        EventDispatcher.trigger("LightLevel", "Noche", {"level": 230 - Sun.alpha})
        Sun.update()

    def __repr__(self):
        return f'Nightblock of {self.parent}'
