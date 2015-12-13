from pygame import time, Surface, PixelArray, SRCALPHA
from engine.base import AzoeSprite
from .constantes import Constants as Cs
from engine.globs.eventDispatcher import EventDispatcher


class Clock:
    _h = 0
    _m = 0
    _s = 0
    day_flag = False
    hour_flag = False

    def __init__(self, h = 0, m = 0, s = 0):
        self._h = h
        self._m = m
        self._s = s
        self.day_flag = False
        self.hour_flag = False

    def __repr__(self):
        return ':'.join([str(self._h), str(self._m).rjust(2, '0')])

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        self.hour_flag = True
        if value > 23:
            self._h = 0
            self.day_flag = True
        else:
            self._h = value

    @h.deleter
    def h(self):
        self._h = 0

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        if value > 59:
            self.h += 1
            value = 0
        self._m = value

    @m.deleter
    def m(self):
        self._m = 0

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, value):
        if value > 59:
            self._m += 1
            value = 0
        self._s = value

    @s.deleter
    def s(self):
        self._s = 0

    def timestamp(self, h = 0, m = 0, s = 0):
        """Without arguments, returns current tiemstamp
        with arguments, returns the specified TimeStamp
        """

        if h == 0 and m == 0 and s == 0:
            return TimeStamp(self._h, self._m, self._s)
        else:
            return TimeStamp(h, m, s)

    def update(self, dm = 1):
        self.day_flag = False
        self.hour_flag = False
        self.m += dm


class TimeStamp:
    def __init__(self, h = 0, m = 0, s = 0):
        self._h = h
        self._m = m
        self._s = s

    # read-only properties
    @property
    def h(self):
        """Read-only hour value"""
        return self._h

    @property
    def m(self):
        """Read-only minute value"""
        return self._m

    @property
    def s(self):
        """Read-only second value"""
        return self._s

    # rich comparison methods
    def __lt__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            if self._h < other.h:
                return True

            if self._m < other.m:
                return True

            if self._s < other.s:
                return True

        return False

    def __le__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            if self._h <= other.h:
                if self._m <= other.m:
                    if self._s <= other.s:
                        return True
        return False

    def __eq__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            return self._h == other.h and self._m == other.m and self._s == other.s
        return False

    def __ne__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            if self._h != other.h:
                if self._m != other.m:
                    if self._s != other.s:
                        return True
            return False
        return True

    def __gt__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            if self._h > other.h:
                return True
            if self._m > other.m:
                return True
            if self._s > other.s:
                return True
        return False

    def __ge__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            if self._h >= other.h:
                if self._m >= other.m:
                    if self._s >= other.s:
                        return True
        return False

    # operations, add, sub, mul
    @staticmethod
    def _convert(s):
        m = 0
        h = 0
        if s > 59:
            m += s // 60
            s %= 60
        if m > 59:
            h += m // 60
            m %= 60

        return TimeStamp(h, m, s)

    def __add__(self, other):
        s = (self._h * 3600 + self._m * 60 + self._s) + (other.h * 3600 + other.m * 60 + other.s)
        return self._convert(s)

    def __sub__(self, other):
        s = (self._h * 3600 + self._m * 60 + self._s) - (other.h * 3600 + other.m * 60 + other.s)
        return self._convert(s)

    def __mul__(self, factor):
        if not isinstance(factor, int):
            raise NotImplementedError('Solo puede multiplicarse por un factor')
        s = (self._h * 3600 + self._m * 60 + self._s) * factor
        return self._convert(s)

    def __repr__(self):
        return ':'.join([str(self._h), str(self._m).rjust(2, '0')])


class Noche(AzoeSprite):
    def __init__(self, size):
        img = Surface(size, SRCALPHA)
        img.fill((0, 0, 0, 230))  # llenamos con color rgba. como es srcalpha funciona bien

        super().__init__(img)

        self.ubicar(0, 0)

    def set_lights(self, *lights):

        def clamp(n):
            return 0 if n < 0 else 255 if n > 255 else n

        imap = self.image.unmap_rgb  # cache para velocidad
        pxarray = PixelArray(self.image)

        for light in lights:
            if light.nombre == 'sol':
                # chapuza para velocidad
                self.image.fill(light.color, light.rect)
            else:
                image = light.image
                lx = light.rect.x
                ly = light.rect.y

                light_array = PixelArray(image)
                lmap = image.unmap_rgb
                for y in range(0, image.get_width()):
                    for x in range(0, image.get_height()):
                        ox, oy = lx + x, ly + y
                        r, g, b, a = lmap(light_array[x, y])
                        if (r, g, b) != Cs.COLOR_IGNORADO:
                            _r, _g, _b, _a = imap(pxarray[ox, oy])
                            r = clamp(r + _r)
                            g = clamp(g + _g)
                            b = clamp(b + _b)
                            a = clamp(_a - (255 - a))
                            pxarray[ox, oy] = r, g, b, a
        nch = pxarray.make_surface()
        self.image = nch


class Tiempo:
    FPS = time.Clock()
    dia, _frames = 0, 0
    clock = Clock()
    noche = None

    @classmethod
    def setear_momento(cls, dia, hora, mins = 0):
        cls.dia = dia
        cls.clock.h = hora
        cls.clock.m = mins

    @classmethod
    def update(cls, rate):
        cls.FPS.tick(rate)

        cls._frames += 1
        if cls._frames == rate:
            cls.clock.update()
            cls._frames = 0
            if cls.clock.day_flag:
                cls.dia += 1
            if cls.clock.hour_flag:
                EventDispatcher.trigger('hora', 'Tiempo', {"hora": cls.clock.timestamp()})
    
    @classmethod
    def crear_noche(cls, tamanio):
        cls.noche = Noche(tamanio)
