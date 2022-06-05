from .event_dispatcher import EventDispatcher
from .game_groups import Mob_Group


class Sun:
    light = None
    lights = None

    alpha = 0  # nigth alpha, this value and it accompanying function have nothing to do with the Sun.
    aclarar = False
    oscurecer = False

    @classmethod
    def init(cls, latitude):
        # noroeste, noreste, suroeste, sureste
        cls.set_latitude(latitude, 0, 6, 2, 4)
        EventDispatcher.register(cls.set_by_event, 'ClockAlarm')

    @classmethod
    def set_latitude(cls, latitude, noroeste=0, noreste=6, suroeste=2, sureste=4):
        if latitude >= 0:  # el ">=" es porque las sombras este y oeste no andan bien
            # latitud norte
            cls.lights = [suroeste, 8, sureste]  # Puede que esto,
        elif latitude < 0:
            # latitud sur
            cls.lights = [noroeste, 8, noreste]  # esté al revés.

    @classmethod
    def calculate(cls, actual, amanece, mediodia, atardece, anochece):
        alarm = None
        if amanece < actual < mediodia:  # mañana
            alarm = 'amanece'
        elif mediodia < actual < atardece:  # dia
            alarm = 'mediodía'
        elif atardece < actual < anochece:  # tarde noche
            alarm = 'atardece'
        elif anochece < actual or actual < amanece:  # noche
            alarm = 'anochece'

        cls.set_light(alarm)

    @classmethod
    def set_by_event(cls, event):
        alarm = event.data['time']
        cls.set_light(alarm)

    @classmethod
    def set_light(cls, alarm):
        if alarm == 'amanece':
            cls.light = cls.lights[0]
        elif alarm == 'mediodía':
            cls.light = cls.lights[1]  # overhead light.
        elif alarm == 'atardece':
            cls.light = cls.lights[2]
        elif alarm == 'anochece':
            cls.light = None

        for mob in Mob_Group:
            mob.recibir_luz_solar(cls.light)

    @classmethod
    def set_mod(cls, actual, amanece, mediodia, atardece, anochece):

        if amanece < actual < mediodia:  # mañana
            if actual-amanece < mediodia-actual:
                elapsed = actual-amanece
                cls.alpha = 230-(elapsed.h * 60 + elapsed.m)
            else:
                elapsed = mediodia-actual
                cls.alpha = elapsed.h * 60 + elapsed.m
            cls.aclarar = True

        elif atardece < actual < anochece:  # tarde noche
            if actual-atardece < anochece-actual:
                elapsed = actual-atardece
                cls.alpha = elapsed.h * 60 + elapsed.m
            else:
                elapsed = anochece-actual
                cls.alpha = 230 - (elapsed.h * 60 + elapsed.m)
            cls.oscurecer = True

        elif mediodia < actual < atardece:  # dia
            cls.alpha = 0

        elif anochece < actual or actual < amanece:  # noche
            cls.alpha = 230

        EventDispatcher.trigger('SetNight', 'Noche', {'alpha': cls.alpha})

        ts = anochece - atardece
        s = ts.h * 3600 + ts.m * 60 + ts.s
        cls.mod = round(230 / (s // 60))  # 1
        # cls.propagate(cls.alpha)
