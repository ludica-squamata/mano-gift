from .event_dispatcher import EventDispatcher
from .game_groups import Mob_Group, Prop_Group
from .game_state import GameState


class Sun:
    light = None
    lights = None

    alpha = 0  # nigth alpha, this value and it accompanying function have nothing to do with the Sun.
    aclarar = False
    oscurecer = False

    current_light = None

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
    def set_by_event(cls, event):
        alarm = event.data['time']
        cls.set_light(alarm)

    @classmethod
    def set_light(cls, alarm):
        if alarm == 'amanece':
            cls.light = cls.lights[0]
            cls.aclarar = True
            EventDispatcher.trigger('ShadowFade', 'Sun', {'do_fade': True, 'inverted': True})
            EventDispatcher.trigger('NightFall', 'Night', {'value': False})
            GameState.del2('NightTime')
        elif alarm == 'mediodía':
            cls.light = cls.lights[1]  # overhead light.
            cls.aclarar = False
            EventDispatcher.trigger('ShadowFade', 'Sun', {'do_fade': False, 'inverted': False})
        elif alarm == 'atardece':
            cls.light = cls.lights[2]
            EventDispatcher.trigger('ShadowFade', 'Sun', {'do_fade': True, 'inverted': True})
            cls.oscurecer = False
        else:
            cls.oscurecer = True
            EventDispatcher.trigger('ShadowFade', 'Sun', {'do_fade': False, 'inverted': False})
            EventDispatcher.trigger('NightFall', 'Night', {'value': True})
            GameState.set2('NightTime')
            cls.light = None

        cls.current_light = cls.light

        cls.update()

    @classmethod
    def set_mod(cls, actual, amanece, mediodia, atardece, anochece):

        alarm = None
        if amanece < actual < mediodia:  # mañana
            if actual - amanece < mediodia - actual:
                elapsed = actual - amanece
                cls.alpha = 230 - (elapsed.h * 60 + elapsed.m)
            else:
                elapsed = mediodia - actual
                cls.alpha = elapsed.h * 60 + elapsed.m
            cls.aclarar = True
            alarm = 'amanece'

        elif atardece < actual < anochece:  # tarde noche
            if actual - atardece < anochece - actual:
                elapsed = actual - atardece
                cls.alpha = elapsed.h * 60 + elapsed.m
            else:
                elapsed = anochece - actual
                cls.alpha = 230 - (elapsed.h * 60 + elapsed.m)
            cls.oscurecer = True
            alarm = 'atardece'

        elif mediodia < actual < atardece:  # dia
            cls.alpha = 0
            alarm = 'mediodía'

        elif anochece < actual or actual < amanece:  # noche
            cls.alpha = 230
            alarm = 'anochece'

        cls.set_light(alarm)

    @classmethod
    def update(cls):
        for mob in Mob_Group:
            if cls.light is not None:
                mob.recibir_luz_solar(cls.light)

        for item in Prop_Group:
            if cls.light is not None:
                item.recibir_luz_solar(cls.light)
