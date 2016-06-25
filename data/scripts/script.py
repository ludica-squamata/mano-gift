# script.py
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import EngineData as Ed


class Script:
    mapa = False

    @classmethod
    def update(cls):
        if Ed.char_name and not cls.mapa:
            cls.mapa = True
            EventDispatcher.trigger("nuevo", "Script", {'char_name': Ed.char_name})
