from .game_groups import Mob_Group, Item_Group, Prop_Group
from .event_dispatcher import EventDispatcher
from engine.misc.config import Config
from csv import DictReader, DictWriter
from .mod_data import ModData
from os import path, getcwd
from .tiempo import Tiempo


class ItemHistoryRegistry:

    @classmethod
    def init(cls):
        cls.events = []
        cls.delta = []
        EventDispatcher.register(cls.record, 'RecordHistory')
        EventDispatcher.register(cls.flush_delta, 'SaveDataFile')

        ruta = path.join(getcwd(), Config.savedir, 'item_history_list.csv')
        with open(ruta, 'rt', encoding='utf-8') as csv_file:
            reader = DictReader(csv_file, delimiter=';')
            cls.rows = list(reader)

    @classmethod
    def record(cls, event):
        if event.data not in cls.rows:
            cls.events.append(event.data)
            cls.delta.append(event.data)

    @classmethod
    def rewind(cls):
        whats = {event['what'] for event in cls.rows}
        for what in whats:
            if Item_Group.get_by_id(what) is not None:
                item = Item_Group.get_by_id(what)
                affected = [ev for ev in cls.rows if ev['what'] == what]
                if len(affected) > 1:
                    for evento in affected:
                        if evento['event'] != 'worldgen':
                            if evento['event'] == 'pickup':
                                mob = Mob_Group[evento['to']]
                                item.action(mob, from_history=True)

    @classmethod
    def flush_delta(cls, event):
        d = cls.delta
        cls.delta = []
        if event.origin:
            ruta = path.join(getcwd(), Config.savedir, 'item_history_list.csv')
            with open(ruta, 'wt', encoding='utf-8') as csv_file:
                fieldnames = ['when', 'what', 'event', 'to']
                writer = DictWriter(csv_file, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
                writer.writeheader()
                for row in d:
                    writer.writerow(row)


ItemHistoryRegistry.init()
