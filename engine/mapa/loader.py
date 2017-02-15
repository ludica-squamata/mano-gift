from engine.globs import GRUPO_ITEMS, GRUPO_MOBS
from engine.globs import EngineData as Ed, ModData as Md
from engine.globs import MobGroup
from engine.misc import Resources as Rs
from engine.scenery import new_prop
from engine.mobs import PC, NPC
from .salida import Salida


class Loader:

    @classmethod
    def load_everything(cls, alldata, x, y):
        loaded = []
        for mob in cls.load_hero(x, y) + cls.load_mobs(alldata):
            loaded.append((mob, GRUPO_MOBS))
        for prop in cls.load_props(alldata):
            loaded.append((prop, GRUPO_ITEMS))
        return loaded

    @classmethod
    def load_something(cls, alldata, x, y, requested):
        """
        :type requested: list
        :type alldata: dict
        :type x: int
        :type y: int
        """
        loaded = []
        if 'PC' in requested:
            loaded.append((cls.load_hero(x, y), GRUPO_MOBS))

        if 'NPC' in requested:
            for mob in cls.load_mobs(alldata):
                loaded.append((mob, GRUPO_MOBS))

        if 'Prop' in requested:
            for prop in cls.load_props(alldata):
                loaded.append((prop, GRUPO_ITEMS))

        return loaded

    @staticmethod
    def load_props(alldata):
        imgs = alldata['refs']
        pos = alldata['props']

        loaded_props = []
        for ref in pos:
            try:
                data = Rs.abrir_json(Md.items + ref + '.json')
            except IOError:
                data = False

            for x, y in pos[ref]:
                if data:
                    prop = new_prop(ref, x, y, data=data)
                    is_interactive = hasattr(prop, 'accion')
                else:
                    prop = new_prop(ref, x, y, img=imgs[ref])
                    is_interactive = False

                if type(prop) is list:
                    for p in prop:
                        loaded_props.append((p, is_interactive))
                else:
                    loaded_props.append((prop, is_interactive))

        return loaded_props

    @staticmethod
    def load_mobs(alldata):
        loaded_mobs = []
        for key in alldata['mobs']:
            pos = alldata['mobs'][key]
            for ref in pos:
                data = Rs.abrir_json(Md.mobs + key + '.json')
                for x, y in pos:
                    mob = NPC(ref, x, y, data)
                    loaded_mobs.append((mob, GRUPO_MOBS))

        return loaded_mobs

    @staticmethod
    def load_hero(x, y):
        try:
            pc = MobGroup['heroe']
            Ed.HERO = pc
            Ed.HERO.ubicar(x, y)
            Ed.HERO.mapRect.center = x, y
            Ed.HERO.z = Ed.HERO.mapRect.y + Ed.HERO.rect.h
            
        except (IndexError, KeyError, AttributeError):
            Ed.HERO = PC(Rs.abrir_json(Md.mobs + 'hero.json'), x, y)

        return [Ed.HERO]

    @staticmethod
    def cargar_salidas(alldata):
        salidas = []
        for datos in alldata['salidas']:
            nombre = datos['nombre']
            stage = datos['nombre']
            rect = datos['rect']
            chunk = datos['chunk']
            entrada = datos['entrada']
            direcciones = datos['direcciones']

            salidas.append(Salida(nombre, stage, rect, chunk, entrada, direcciones))

        return salidas
