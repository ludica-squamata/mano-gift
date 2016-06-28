from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import EngineData as Ed


def nuevo(evento):
    Ed.setear_escena(evento.data['scene'])

EventDispatcher.register(nuevo, "nuevo")
