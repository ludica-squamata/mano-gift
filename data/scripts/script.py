# script.py
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import EngineData


class Script:

    @classmethod
    def update(cls):
        if EngineData.char_name and EngineData.MAPA_ACTUAL is None:
            EventDispatcher.trigger("nuevo", "Script", {'scene': 0})
