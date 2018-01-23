from engine.mobs.Inventory import Inventory
from ._atribuido import Atribuido


class Equipado(Atribuido):
    equipo = {'yelmo': None, 'aro 1': None, 'aro 2': None, 'cuello': None, 'peto': None,
              'guardabrazos': None, 'brazales': None, 'faldar': None, 'quijotes': None,
              'grebas': None, 'mano buena': None, 'mano mala': None, 'botas': None, 'capa': None,
              'cinto': None, 'guantes': None, 'anillo 1': None, 'anillo 2': None}
    inventario = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventario = Inventory(10, 10 + self.ataque)

    def equipar_item(self, item):
        self.equipo[item.espacio] = item
        self.inventario.remover(item)

    def desequipar_item(self, item):
        self.equipo[item.espacio] = None
        self.inventario.agregar(item)
