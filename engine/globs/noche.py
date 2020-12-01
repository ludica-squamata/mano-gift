from engine.globs.azoe_group import AzoeBaseSprite
from pygame import Surface, PixelArray, SRCALPHA
from .event_dispatcher import EventDispatcher
from .colores import COLOR_IGNORADO


class Noche(AzoeBaseSprite):
    oscurecer = False
    aclarar = False

    alpha = 0
    mod = 0

    overriden = False

    @classmethod
    def init(cls):
        EventDispatcher.register_many((cls.get_alarms, 'ClockAlarm'),
                                      (cls.set_darkness, 'MinuteFlag'))

    def __init__(self, parent, rect):
        img = Surface(rect.size, SRCALPHA)
        img.fill((0, 0, 0, self.alpha))
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

    # noinspection PyUnresolvedReferences
    def set_lights(self, lights):

        def clamp(n):
            return 0 if n < 0 else 255 if n > 255 else n

        imap = self.image.unmap_rgb  # cache para velocidad
        pxarray = PixelArray(self.image)

        for light in lights:
            image = light.image
            w, h = image.get_size()
            lx = light.rect.x
            ly = light.rect.y

            light_array = PixelArray(image)
            lmap = image.unmap_rgb
            for y in range(0, h):
                for x in range(0, w):
                    ox, oy = lx + x, ly + y
                    r, g, b, a = lmap(light_array[x, y])
                    if (r, g, b) != COLOR_IGNORADO:
                        _r, _g, _b, _a = imap(pxarray[ox, oy])
                        r = clamp(r + _r)
                        g = clamp(g + _g)
                        b = clamp(b + _b)
                        a = clamp(_a - (255 - a))
                        pxarray[ox, oy] = r, g, b, a
                        # self.luces.append(light)
                        # light.update()
        nch = pxarray.make_surface()
        self.image = nch

    @classmethod
    def trasparentar(cls, mod, max_alpha=230):  # this is gradual
        if 0 < cls.alpha + mod < max_alpha:
            cls.alpha += mod
            EventDispatcher.trigger('SetNight', 'Noche', {'mod': mod})

    def update(self):
        self.rect.topleft = self.parent.rect.topleft
        if self.oscurecer or self.aclarar or self.overriden:
            self.image.fill((0, 0, 0, self.alpha))
            self.overriden = False


Noche.init()
