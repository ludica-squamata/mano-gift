from engine.globs import ModData, Tiempo, TimeStamp
from engine.scenery import new_item
from engine.misc import abrir_json, Config
from ._equipado import Equipado
from collections import Counter
from os import path, listdir
import csv


class Comerciante(Equipado):
    def __init__(self, parent, data, **kwargs):
        super().__init__(parent, data, **kwargs)
        self.wallet = Counter({'$': 0})

        ruta1 = path.join(ModData.game_fd, 'world_setup.json')
        ruta2 = path.join(Config.savedir, 'trading_list.csv')

        file_1 = abrir_json(ruta1)['inventario_inicial']
        reader_1 = []
        for trader in file_1:
            named_trader = None
            if trader.lower() == data['occupation']:
                named_trader = data['nombre']
            elif trader == data["nombre"]:
                named_trader = trader

            if named_trader is not None:
                for item in file_1[trader]:
                    entry = {'trader': named_trader, 'item': item, 'cant': file_1[trader][item], 'desde': "inicio"}

                    reader_1.append(entry)

        if not path.exists(ruta2):
            file_2 = open(ruta2, 'xt', encoding='utf-8', newline='\r\n')
        else:
            file_2 = open(ruta2, 'r', encoding='utf-8')
        reader_2 = list(csv.DictReader(file_2, ['trader', 'item', 'cant', "desde"], delimiter=";"))
        file_2.close()
        reader = reader_1 + reader_2
        for row in [row for row in reader if row['trader'] == self.nombre]:
            item = None
            now = Tiempo.clock.timestamp()
            timestamp = TimeStamp(*row['desde'].split(':')) if row['desde'] != 'inicio' else "inicio"
            if row['desde'] == 'inicio' or now >= timestamp:
                ruta = ModData.items + row['item'].lower().replace(" ", "_") + '.json'
                if path.exists(ruta):
                    item = new_item(self, ruta)
                elif row['item'] == 'Dinero':
                    self.wallet["$"] += int(row['cant'])
                else:
                    files = [abrir_json(path.join(ModData.items, file)) for file in listdir(ModData.items)]
                    item_file = [file for file in files if file.get('nombre', '') == row['item']]
                    item = new_item(self, item_file.pop()) if len(item_file) else None

                if item is not None:
                    cant = int(row['cant'])
                    if cant > 0:
                        for copy in [item] * cant:
                            self.inventario.agregar(copy)
                    else:
                        for _ in range(abs(cant)):
                            self.inventario.remover(item)

    def recibir_dinero(self, coin, value):
        self.wallet[coin] += value

    def entregar_dinero(self, coin, value):
        if self.wallet[coin] >= value:
            self.wallet[coin] -= value
            return True
        else:
            return False

    def vender_item(self, item):
        if item in self.inventario:
            self.inventario.remover(item)
