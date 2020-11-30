from engine.globs.azoe_group import AzoeBaseSprite
from pygame import Surface, PixelArray, SRCALPHA
from .event_dispatcher import EventDispatcher
from .colores import COLOR_IGNORADO


class Noche(AzoeBaseSprite):
    oscurecer = False
    aclarar = False
    flag = False

    alpha = 0
    mod = 0
    color = None

    @classmethod
    def init(cls):
        cls.alpha = 0
        cls.mod = 0
        cls.color = (0, 0, 0, 0)

    def __init__(self, parent, size):
        img = Surface(size, SRCALPHA)
        img.fill(self.color)
        rect = img.get_rect()
        super().__init__(parent, 'night block', image=img, rect=rect)
        # self.z = 100000
        # self.alpha = 230
        # self.alpha_mod = 0

    #     self.show()
    #     EventDispatcher.register_many((self.get_alarms, 'ClockAlarm'),
    #                                   (self.set_darkness, 'MinuteFlag'),
    #                                   (lambda e: self.show(), 'ShowNight'))
    #
    # def show(self):
    #     EventDispatcher.trigger('SetTheNight', 'Noche', {'noche': self})

    @classmethod
    def set_mod(cls, alarm_dict):
        atardece = alarm_dict['atardece']
        anochece = alarm_dict['anochece']
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
            # self.image.fill((0, 0, 0, self.alpha))
            EventDispatcher.trigger('SetNight', 'Noche', {'alpha': mod})
    #
    # def set_transparency(self, mod):  # this is direct
    #     self.alpha = mod
    #     self.image.fill((0, 0, 0, self.alpha))


Noche.init()
