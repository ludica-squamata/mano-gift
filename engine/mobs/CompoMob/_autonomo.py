from engine.globs.event_dispatcher import EventDispatcher
from engine.mobs.behaviourtrees import BehaviourTree
from engine.misc.resources import abrir_json
from engine.mobs import ControllableAI
from engine.globs import ModData
from . import Sensitivo, Animado


class Autonomo(Sensitivo, Animado):  # tiene que poder ver para ser autónomo
    paused = False
    AI_type = ''  # 'Controllable' or  'Autonomous'

    pause_overridden = False
    _trees = None

    def __init__(self, parent, data, **kwargs):
        super().__init__(parent, data, **kwargs)
        ai_name = data['AI']
        self._trees = {ai_name: self.create_ai(ai_name)}
        self['AI'] = self._trees[ai_name]

        EventDispatcher.register(self.toggle_pause_state, 'TogglePause')

    def toggle_pause_state(self, event):
        if not self.pause_overridden:
            self.paused = event.data['value']

    def unload(self):
        super().unload()
        EventDispatcher.deregister(self.toggle_pause_state, 'TogglePause')

    def create_ai(self, name):
        if name == 'controllable':
            self.AI_type = 'Controllable'
            return ControllableAI(self)

        else:
            self.AI_type = 'Autonomous'
            tree_data = abrir_json(ModData.mobs + 'behaviours/' + name + '.json')
            return BehaviourTree(self, tree_data)

    def switch_behaviour(self, name):
        tree_data = abrir_json(ModData.mobs + 'behaviours/' + name + '.json')
        if name not in self._trees:
            self._trees[name] = BehaviourTree(self, tree_data)
        self["AI"].reset()
        self["AI"] = self._trees[name]
        self["AI"].update()

    def update(self, *args):
        if not self.paused and not self.dead:
            self["AI"].update()
            super().update(*args)
