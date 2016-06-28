# script.py
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import EngineData


class Script:
    mapa = False

    @classmethod
    def update(cls):
        if EngineData.char_name and EngineData.MAPA_ACTUAL is not None:
            cls.mapa = True
            EventDispatcher.trigger("nuevo", "Script", {'scene': 0})
