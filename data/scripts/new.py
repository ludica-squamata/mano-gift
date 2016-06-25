from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import EngineData as Ed


def nuevo(evento):
    Ed.setear_escena('casas y arboles (normal)')

EventDispatcher.register(nuevo, "nuevo")
