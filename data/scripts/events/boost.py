from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import Mob_Group


def boost(evento):
    mob = Mob_Group.get_controlled_mob()
    attr = evento.data['attr']
    value = evento.data['value']
    mob[attr] += value


EventDispatcher.register(boost, "Boost")
