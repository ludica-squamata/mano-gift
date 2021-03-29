from engine.mobs.inventory import Inventory
from ._caracterizado import Caracterizado


class Equipado(Caracterizado):
    equipo = {'yelmo': None, 'aro 1': None, 'aro 2': None, 'cuello': None, 'peto': None,
              'guardabrazos': None, 'brazales': None, 'faldar': None, 'quijotes': None,
              'grebas': None, 'mano buena': None, 'mano mala': None, 'botas': None, 'capa': None,
              'cinto': None, 'guantes': None, 'anillo 1': None, 'anillo 2': None}
    inventario = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventario = Inventory(10, 10 + self['ModCarga'])
        self.dureza = 0

    def equipar_item(self, item):
        self.equipo[item.espacio] = item
        if hasattr(item, 'proteccion'):
            self.dureza += item.proteccion
        elif hasattr(item, 'efecto'):
            pass
        self.inventario.remover(item)

    def desequipar_item(self, item):
        self.equipo[item.espacio] = None
        if hasattr(item, 'proteccion'):
            self.dureza -= item.proteccion
        self.inventario.agregar(item)
