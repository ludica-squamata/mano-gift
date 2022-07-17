from engine.globs.event_dispatcher import EventDispatcher
from pygame import time, font
from datetime import datetime
from math import floor, ceil
from itertools import cycle


class Clock:
    _h = 0
    _m = 0
    _s = 0
    real = False
    day_flag = False
    hour_flag = False
    minute_flag = False
    second_flag = False
    enabled = False

    alarms = None

    def __init__(self, real=False, h=0, m=0, s=0, minute_lenght=60):
        """Nuevo Reloj Clock con capacidades superiores. Puede ser real o ficticio.
        Ahora con nuevas flags para minutos y segundos, además de horas y días.

        real determina si se usa un reloj real (que usa la hora del sistema)
        o uno ficticio. En caso de usar un reloj ficticio, es posible determinar
        la hora, minutos y segundos estableciendo valores para h, m y s.
        minute_lenght determina cuantos ticks (por defecto, 60 ticks = 1 segundo)
        dura un minuto de un reloj ficticio. Este valor es ignorado si el reloj
        es real.

        :param real: bool
        :param h: int
        :param m: int
        :param s: int
        :param minute_lenght: int
        """

        self.real = real

        if self.real:
            now = datetime.now().time()
            h = now.hour
            m = now.minute
            s = now.second
        else:
            self.ds = minute_lenght

        self._h = h
        self._m = m
        self._s = s

        EventDispatcher.register(self.on_pause, 'TogglePause')
        # las alarmas son tiempos específicos en los que Clock debe lanzar un evento.
        self.alarms = {}

    def on_pause(self, event):
        self.enabled = not event.data['value']

    def __repr__(self):
        return ':'.join([str(self._h), str(self._m).rjust(2, '0')])

    def is_real(self):
        return self.real

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, value):
        if self.real:
            if value != self._h:
                self.hour_flag = True
            if value == 0:
                self.day_flag = True
        else:
            self.hour_flag = True
            if value > 23:
                self.day_flag = True
                value = 0

            self._h = value

    @h.deleter
    def h(self):
        self._h = 0

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        if self.real:
            if value != self._m:
                self.minute_flag = True
        else:
            self.minute_flag = True
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
        if self.real:
            if value != self._m:
                self.second_flag = True
        else:
            self.second_flag = True
            if value > 59:
                self.m += 1
                value = 0

        self._s = value

    @s.deleter
    def s(self):
        self._s = 0

    def timestamp(self, h=0, m=0, s=0):
        """Without arguments, returns current tiemstamp
        with arguments, returns the specified TimeStamp
        :param s: int
        :param m: int
        :param h: int
        """

        if h == 0 and m == 0 and s == 0:
            return TimeStamp(self._h, self._m, self._s)
        else:
            return TimeStamp(h, m, s)

    def update(self):
        if self.enabled:
            self.day_flag = False
            self.hour_flag = False
            self.minute_flag = False
            self.second_flag = False

            if self.real:
                _time = datetime.now().time()
                self.h = _time.hour
                self.m = _time.minute
                self.s = _time.second
            else:
                self.s += self.ds

            ts = self.timestamp()
            if ts in self.alarms:
                EventDispatcher.trigger('ClockAlarm', 'Clock', {'time': self.alarms[ts]})

    def render(self, color):
        fuente = font.SysFont('Verdana', 16)
        text = str(self.timestamp())
        render = fuente.render(text, True, color)
        return render


class TimeStamp:
    def __init__(self, h=0, m=0, s=0):
        if type(h) is float:
            decimales = h - floor(h)
            h = int(h - decimales)
            m = int(decimales * 60)

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
            s1 = self._h * 3600 + self._m * 60 + self._s
            s2 = other.h * 3600 + other.m * 60 + other.s
            if s1 < s2:
                return True
        return False

    def __le__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            s1 = self._h * 3600 + self._m * 60 + self._s
            s2 = other.h * 3600 + other.m * 60 + other.s
            if s1 <= s2:
                return True
        return False

    def __eq__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            return self._h == other.h and self._m == other.m and self._s == other.s
        return False

    def __ne__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            return self._h != other.h and self._m != other.m and self._s != other.s
        return True

    def __hash__(self):
        return hash((self._h, self._m, self._s))

    def __gt__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            s1 = self._h * 3600 + self._m * 60 + self._s
            s2 = other.h * 3600 + other.m * 60 + other.s
            if s1 > s2:
                return True
        return False

    def __ge__(self, other):
        if hasattr(other, '_h') and hasattr(other, '_m') and hasattr(other, '_s'):
            s1 = self._h * 3600 + self._m * 60 + self._s
            s2 = other.h * 3600 + other.m * 60 + other.s
            if s1 >= s2:
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

    def __float__(self):
        s = (self._h * 3600 + self._m * 60 + self._s)
        return float(s / 3600)

    def __repr__(self):
        return ':'.join([str(self._h), str(self._m).rjust(2, '0')])


class Tiempo:
    FPS = time.Clock()
    dia, _frames = 0, 0
    noche = None
    clock = None

    @classmethod
    def set_clock(cls, is_real, min_lenght):
        cls.clock = Clock(real=is_real, minute_lenght=min_lenght)

    @classmethod
    def set_time(cls, dia, hora, mins=0, segs=0):
        cls.dia = dia
        cls.clock.h = hora
        cls.clock.m = mins
        cls.clock.s = segs

        SeasonalYear.init()

    @classmethod
    def set_year(cls, year, month, week):
        SeasonalYear.set_year(year, month, week)

    @classmethod
    def get_time(cls):
        return cls.dia, cls.clock.h, cls.clock.m, cls.clock.s

    @classmethod
    def save_time(cls, event):
        EventDispatcher.trigger(event.tipo + 'Data', 'Tiempo', {'tiempo': cls.get_time()})

    @classmethod
    def reset_days(cls):
        cls.dia = -1

    @classmethod
    def get_frames(cls):
        return cls._frames

    @classmethod
    def update(cls, rate=0):
        cls.FPS.tick(rate)

        cls._frames += 1
        if cls._frames == rate:
            cls.clock.update()
            cls._frames = 0
            if cls.clock.day_flag:
                cls.dia += 1
                EventDispatcher.trigger('DayFlag', 'Tiempo', {'days': cls.dia})
            if cls.clock.hour_flag:
                EventDispatcher.trigger('HourFlag', 'Tiempo', {"hora": cls.clock.timestamp()})
            if cls.clock.minute_flag:
                EventDispatcher.trigger('MinuteFlag', 'Tiempo', {"hora": cls.clock.timestamp()})
            if cls.clock.second_flag:
                EventDispatcher.trigger('SecondFlag', 'Tiempo', {"hora": cls.clock.timestamp()})

    @classmethod
    def update_alarms(cls, alarms):
        cls.clock.alarms.update(alarms)
        cls.clock.update()


class SeasonalYear:
    # default values
    year_lenght = 360  # days
    month_lenght = 30  # days
    week_lenght = 7  # days

    # varies with season and biome
    day_lenght = 0  # hours

    biome = None
    season = None

    week_day = 0
    month_day = 0

    biomes = {  # los valores son la cantidad de horas de luz que puede tener un día.
        "polar": {  # corresponde a latitudes entre 90º y 30º N/S
            "summer": 24, "winter": 0, 'seaon_lenght': year_lenght // 2},
        "equatorial": {  # corresponde a latitudes entre 30ºS y 30ºN
            "spring": 12, "fall": 12, 'seaon_lenght': year_lenght // 2},
        "tempered": {  # corresponde a latitudes entre 30º y 90º N/S.
            "spring": 12, "summer": 19, "fall": 12, "winter": 10, 'season_lenght': year_lenght // 4}
    }
    season_cycler = cycle(['summer', 'fall', 'winter', 'spring'])  # itertools.cycle
    month_cycler = None

    @classmethod
    def init(cls):
        cls.biome = 'tempered'
        cls.season = next(cls.season_cycler)
        cls.set_day_duration()
        cls.propagate()

        EventDispatcher.register(cls.cycle_time, 'DayFlag')
        if cls.month_cycler is None:  # cls.set_year() was not called.
            cls.month_cycler = cycle([i for i in range(cls.year_lenght // cls.month_lenght)])
            cls.month = next(cls.month_cycler)

    @classmethod
    def set_year(cls, year, month, week):
        # this method may not be called if custom "world_properties" are not present in mod.json
        cls.year_lenght = year
        cls.month_lenght = month
        cls.week_lenght = week

        cls.month_cycler = cycle([i for i in range(year // month)])
        cls.month = next(cls.month_cycler)

        cls.week_day = 0

    @classmethod
    def cycle_time(cls, event):
        # Tiempo ya de por si cuenta los días.
        number_of_days = event.data['days']
        # No hay necesidad de que SeasonalYear los cuente también
        if number_of_days % cls.biomes[cls.biome]['season_lenght'] == 0:
            cls.season = next(cls.season_cycler)
            cls.set_day_duration()
            cls.propagate()

        if number_of_days == cls.year_lenght:
            cls.season = next(cls.season_cycler)
            Tiempo.reset_days()

        if number_of_days % cls.month_lenght == 0:
            cls.month = next(cls.month_cycler)
            cls.month_day = 0
        else:
            cls.month_day += 1

        cls.week_day = number_of_days % cls.week_lenght

    @classmethod
    def set_day_duration(cls):
        if cls.season in cls.biomes[cls.biome]:
            cls.day_lenght = cls.biomes[cls.biome][cls.season]

    @classmethod
    def propagate(cls):
        # Este trigger es para setear las timestamps en Stage.
        EventDispatcher.trigger('UpdateTime', 'SeasonalYear', {'new_daylenght': cls.day_lenght})

    @classmethod
    def cargar_timestamps(cls):
        horas_dia = cls.day_lenght
        offset = ceil(12 - (horas_dia / 2))
        actual = Tiempo.clock.timestamp()
        amanece = TimeStamp(offset + 1)
        mediodia = TimeStamp(offset + (horas_dia / 2))
        anochece = TimeStamp(offset + horas_dia)
        atardece = TimeStamp((float(mediodia) + float(anochece) + 1) / 2)

        Tiempo.clock.alarms.update({atardece: 'atardece', anochece: 'anochece',
                                    amanece: 'amanece', mediodia: 'mediodía'})

        return actual, amanece, mediodia, atardece, anochece


EventDispatcher.register(Tiempo.save_time, 'Save')
