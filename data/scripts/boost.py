from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import MobGroup


def boost(evento):
    mob = MobGroup['heroe']
    attr = evento.data['attr']
    value = evento.data['value']

    if hasattr(mob, attr):
        # no se me ocurre un forma más elegante de hacerlo.
        exec('mob.' + attr + '+=' + str(value))


EventDispatcher.register(boost, "DialogEvent")
