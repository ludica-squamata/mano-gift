from engine.mobs.behaviortrees import BehaviourTree
from . import Sensitivo, Animado
from engine.globs import EngineData as Ed, ModData as Md
from engine.misc.resources import Resources as Rs


class Autonomo(Sensitivo, Animado):  # tiene que poder ver para ser autónomo
    AI = None  # determina cómo se va a mover el mob
    """:type AI:()->None"""

    def __init__(self, data, x, y, **kwargs):
        nombre = data['states'][0]['AI']
        tree_data = Rs.abrir_json(Md.mobs + 'behaviours/' + nombre + '.json')
        module = Rs.load_module_from_script(nombre)
        self.AI = BehaviourTree(self, tree_data, module)  # function alias!

        self._AI = self.AI  # copia de la AI original
        super().__init__(data, x, y, **kwargs)

    def update(self, *args):
        if not Ed.onPause and not self.dead:
            # detectados = self.oir() + self.ver()
            e = self.AI.update()
            if e is not None:
                self.AI.reset()
        super().update(*args)
