from engine.globs.event_dispatcher import EventDispatcher
from engine.mobs.behaviortrees import BehaviourTree
from engine.misc.resources import abrir_json
from engine.mobs import ControllableAI
from engine.globs import ModData
from . import Sensitivo, Animado


class Autonomo(Sensitivo, Animado):  # tiene que poder ver para ser autónomo
    AI = None  # determina cómo se va a mover el mob
    _AI = None  # copia de la AI original
    paused = False
    AI_type = ''  # 'Controllable' or  'Autonomous'

    def __init__(self, parent, data, **kwargs):
        ai_name = data['AI']

        self.AI = self.create_ai(ai_name)
        self._AI = self.AI

        EventDispatcher.register(self.toggle_pause_state, 'TogglePause')
        super().__init__(parent, data, **kwargs)

    def toggle_pause_state(self, event):
        self.paused = event.data['value']

    def create_ai(self, name):
        if name == 'controllable':
            self.AI_type = 'Controllable'
            return ControllableAI(self)

        else:
            self.AI_type = 'Autonomous'
            tree_data = abrir_json(ModData.mobs + 'behaviours/' + name + '.json')
            return BehaviourTree(self, tree_data)

    def update(self, *args):
        if not self.paused:
            self.AI.update()
            super().update(*args)
