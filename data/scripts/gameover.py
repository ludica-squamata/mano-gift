from engine.misc.util import Util
from engine.globs.eventDispatcher import EventDispatcher


def gameover(evento):
    if evento.data['obj'].nombre == 'heroe':
        Util.salir('gameover')

EventDispatcher.register(gameover, "MobMuerto")
