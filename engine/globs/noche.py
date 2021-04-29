from engine.globs.azoe_group import AzoeBaseSprite
from pygame import Surface, PixelArray, SRCALPHA
from .event_dispatcher import EventDispatcher
from .colores import COLOR_IGNORADO


class Noche(AzoeBaseSprite):
    oscurecer = False
    aclarar = False

    alpha = 0
    mod = 0
    last_alpha = 0

    overriden = False

    lights = None

    @classmethod
    def init(cls):
        EventDispatcher.register_many((cls.get_alarms, 'ClockAlarm'),
                                      (cls.set_darkness, 'MinuteFlag'))

    def __init__(self, parent, rect):
        img = Surface(rect.size, SRCALPHA)
        img.fill((0, 0, 0, self.alpha))
        self.lights = []
        super().__init__(parent, 'night block', image=img, rect=rect)

    @classmethod
    def set_mod(cls, actual, amanece, mediodia, atardece, anochece):

        if amanece < actual < mediodia:  # mañana
            if actual-amanece < mediodia-actual:
                elapsed = actual-amanece
                cls.alpha = 230-(elapsed.h * 60 + elapsed.m)
            else:
                elapsed = mediodia-actual
                cls.alpha = elapsed.h * 60 + elapsed.m

        elif atardece < actual < anochece:  # tarde noche
            if actual-atardece < anochece-actual:
                elapsed = actual-atardece
                cls.alpha = elapsed.h * 60 + elapsed.m
            else:
                elapsed = anochece-actual
                cls.alpha = 230 - (elapsed.h * 60 + elapsed.m)

        elif mediodia < actual < atardece:  # dia
            cls.alpha = 0

        elif anochece < actual or actual < amanece:  # noche
            cls.alpha = 230

        EventDispatcher.trigger('SetNight', 'Noche', {'alpha': cls.alpha})

        cls.overriden = True
        ts = anochece - atardece
        s = ts.h * 3600 + ts.m * 60 + ts.s
        cls.mod = round(230 / (s // 60))  # 1

    @classmethod
    def get_alarms(cls, event):
        if event.data['time'] == 'atardece':
            cls.oscurecer = True
        elif event.data['time'] == 'anochece':
            cls.oscurecer = False
            EventDispatcher.trigger('NightFall', 'Noche', {'value': True})

        elif event.data['time'] == 'amanece':
            cls.aclarar = True
        elif event.data['time'] == 'mediodía':
            cls.aclarar = False

    @classmethod
    def set_darkness(cls, event):
        if event.tipo == 'MinuteFlag':
            if cls.oscurecer:
                cls.trasparentar(cls.mod)

            elif cls.aclarar:
                cls.trasparentar(-cls.mod)

    def set_light(self, light):
        self.lights.append(light)

    def unset_light(self, light):
        if light in self.lights:
            self.lights.remove(light)

    def draw_lights(self):
        self.image.fill((0, 0, 0, self.alpha))
        pxarray = PixelArray(self.image.copy())

        for light in self.lights:
            px_li = PixelArray(light.image)
            w, h = light.rect.size
            lx, ly = light.rect.center
            for x in range(w):
                for y in range(h):
                    color = light.image.unmap_rgb(px_li[x, y])
                    if color != COLOR_IGNORADO:
                        pxarray[x+lx, y+ly] = color

        self.image = pxarray.make_surface()

    @classmethod
    def trasparentar(cls, mod, max_alpha=230):  # this is gradual
        if 0 < cls.alpha + mod < max_alpha:
            cls.alpha += mod
            EventDispatcher.trigger('SetNight', 'Noche', {'mod': mod})
            EventDispatcher.trigger("LightLevel", "Noche", {"level": 230-cls.alpha})

    def update(self):
        self.rect.topleft = self.parent.rect.topleft
        if self.alpha != self.last_alpha:
            self.last_alpha = self.alpha
            self.draw_lights()


Noche.init()
