# script.py
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import EngineData


class Script:
    mapa = False

    @classmethod
    def update(cls):
        if EngineData.char_name and not cls.mapa:
            cls.mapa = True
            EventDispatcher.trigger("nuevo", "Script", {'char_name': EngineData.char_name})
