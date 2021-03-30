from engine.mobs.inventory import Inventory
from ._caracterizado import Caracterizado
from engine.scenery import new_item


class Equipado(Caracterizado):
    equipo = {'yelmo': None, 'aro 1': None, 'aro 2': None, 'cuello': None, 'peto': None,
              'guardabrazos': None, 'brazales': None, 'faldar': None, 'quijotes': None,
              'grebas': None, 'mano buena': None, 'mano mala': None, 'botas': None, 'capa': None,
              'cinto': None, 'guantes': None, 'anillo 1': None, 'anillo 2': None}
    inventario = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self)
        self.inventario = Inventory(10, 10 + self['ModCarga'])
        self.dureza = 0

    def equipar_item(self, item, espacio):
        self.equipo[espacio] = item
        if hasattr(item, 'proteccion'):
            self.dureza += item.proteccion

        elif hasattr(item, 'method'):
            stat = item.data.get('efecto', {}).get('stat', '')
            mod = item.data.get('efecto', {}).get('mod', '')
            method = item.data.get('efecto', {}).get('method', '')

            if method == 'percentage':
                valmaximo = self[stat + 'Max']
                valactual = self[stat]
                valor = int((mod * valmaximo) / 100)
                if valor + valactual > valmaximo:
                    valor = valmaximo
                else:
                    valor += valactual

                self[stat] = valor

            if method == 'incremental':
                actual = self[stat]
                valor = actual + mod
                self[stat] = valor

        self.inventario.remover(item)

    def desequipar_item(self, item):
        self.equipo[item.espacio] = None
        if hasattr(item, 'proteccion'):
            self.dureza -= item.proteccion

        elif hasattr(item, 'method'):
            stat = item.data.get('efecto', {}).get('stat', '')
            mod = item.data.get('efecto', {}).get('mod', '')
            method = item.data.get('efecto', {}).get('method', '')

            if method == 'percentage':
                valmaximo = self[stat + 'Max']
                self[stat] = valmaximo

            if method == 'incremental':
                actual = self[stat]
                valor = actual - mod
                self[stat] = valor

        self.inventario.agregar(item)

    def enviar_item(self, item_data, entity):
        item_name = item_data.split('/')[-1][:-5]
        if item_name in self.inventario:
            item = self.inventario[item_name]
        else:
            item = new_item(item_name, item_data)
        if item in self.inventario:  # NPCs create items from scratch
            self.inventario.remover(item)
        entity.recibir_item(item)

    def recibir_item(self, item):
        self.inventario.agregar(item)
