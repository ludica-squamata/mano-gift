from engine.mobs.scripts import movimiento
from engine.mobs.behaviortrees import BehaviourTree
from . import Sensitivo, Animado
from engine.globs import EngineData as Ed, ModData as Md
from importlib import machinery
from engine.misc.resources import Resources as Rs


class Autonomo(Sensitivo, Animado):  # tiene que poder ver para ser autónomo
    AI = None  # determina cómo se va a mover el mob
    """:type AI:()->None"""
    objetivo = None  # el mob al que este cazador está persiguiendo

    def __init__(self, *args, **kwargs):
        nombre = args[0]['AI']
        ruta = Md.scripts+nombre+'.py'
        tree_data = Rs.abrir_json(Md.mobs+'behaviours/'+nombre+'.json')
        module = machinery.SourceFileLoader("module.name", ruta).load_module()
        self.AI = BehaviourTree(self, tree_data, module)  # function alias!

        self._AI = self.AI  # copia de la AI original
        super().__init__(*args, **kwargs)

    def determinar_accion(self, detectados):
        """Cambia la AI, la velocidad y la visión de un mob
        si su objetivo está entre los detectados"""

        if self.objetivo in detectados:
            self.velocidad = 2
            self.AI = movimiento.AI_pursue
            self.vision = 'circulo'
            self.mover_vis = self.mover_cir_vis
        else:
            # Esto permite acercarse hasta la espalda del mob, a lo MGS
            self.velocidad = 1
            self.AI = self._AI
            self.vision = 'cono'
            self.mover_vis = self.mover_tri_vis

    def mover(self):
        self.AI.update()
        self.cambiar_direccion(self.direccion)
        dx, dy = self.direcciones[self.direccion]
        super().mover(dx, dy)

    def update(self, *args):
        if not Ed.onPause and not self.dead:
            detectados = self.oir()+self.ver()
            self.determinar_accion(detectados)
            self.mover()
        super().update(*args)
