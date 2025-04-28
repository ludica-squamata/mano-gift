from engine.globs import ModData, Tiempo, TimeStamp
from engine.scenery import new_item
from engine.misc import abrir_json, Config
from ._equipado import Equipado
from collections import Counter
from os import path, listdir
import csv


class Comerciante(Equipado):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wallet = Counter({'$': 0})

        ruta = path.join(Config.savedir, 'trading_list.csv')
        if path.exists(ruta):
            with open(ruta, 'r') as csv_file:
                reader = csv.DictReader(csv_file, ['trader', 'item', 'cant', "desde"], delimiter=";")
                for row in [row for row in reader if row['trader'] == self.nombre]:
                    now = Tiempo.clock.timestamp()
                    timestamp = TimeStamp(*row['desde'].split(':')) if row['desde'] != 'inicio' else "inicio"
                    if row['desde'] == 'inicio' or now >= timestamp:
                        ruta = ModData.items + row['item'].lower().replace(" ", "_") + '.json'
                        if path.exists(ruta):
                            item = new_item(self, ruta)
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
        else:
            file = open(ruta, 'xt', encoding='utf-8', newline='\r\n')
            # if the trading file doesn't exist, the mob will create it.
            file.close()

    def recibir_dinero(self, coin, value):
        self.wallet[coin] += value

    def entregar_dinero(self, coin, value):
        self.wallet[coin] -= value

    def vender_item(self, item):
        if item in self.inventario:
            self.inventario.remover(item)
