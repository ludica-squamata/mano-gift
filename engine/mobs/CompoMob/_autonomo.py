from engine.mobs.behaviortrees import BehaviourTree
from . import Sensitivo, Animado
from engine.globs import EngineData, ModData
from engine.misc.resources import Resources


class Autonomo(Sensitivo, Animado):  # tiene que poder ver para ser autónomo
    AI = None  # determina cómo se va a mover el mob
    """:type AI:()->None"""

    def __init__(self, data, x, y, **kwargs):
        nombre = data['states'][0]['AI']
        tree_data = Resources.abrir_json(ModData.mobs + 'behaviours/' + nombre + '.json')
        self.AI = BehaviourTree(self, tree_data)  # function alias!

        self._AI = self.AI  # copia de la AI original
        super().__init__(data, x, y, **kwargs)

    def update(self, *args):
        super().update(*args)
        if not EngineData.onPause:
            # detectados = self.oir() + self.ver()
            self.AI.update()
