from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import Mob_Group


def boost(evento):
    mob = Mob_Group['heroe']
    attr = evento.data['attr']
    value = evento.data['value']

    if hasattr(mob, attr):
        # no se me ocurre un forma más elegante de hacerlo.
        exec('mob.' + attr + '+=' + str(value))


EventDispatcher.register(boost, "Boost")
