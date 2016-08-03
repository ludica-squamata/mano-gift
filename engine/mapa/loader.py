from engine.globs import GRUPO_ITEMS, GRUPO_MOBS, GRUPO_SALIDAS
from engine.globs import EngineData as Ed, ModData as Md
from engine.globs import MobGroup
from engine.misc import Resources as Rs
from engine.scenery import new_prop
from engine.mobs import PC, NPC
from .salida import Salida


class Loader:
    STAGE = None

    @classmethod
    def set_stage(cls, stage):
        cls.STAGE = stage

    @classmethod
    def load_everything(cls, entrada, mobs_data):
        cls.cargar_hero(entrada)
        cls.cargar_props()
        cls.cargar_mobs(mobs_data)
        cls.cargar_salidas()

    @classmethod
    def cargar_props(cls, ):
        imgs = cls.STAGE.data['refs']
        """:type imgs: dict"""
        pos = cls.STAGE.data['capa_ground']['props']

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
                        cls.STAGE.add_property(p, GRUPO_ITEMS, is_interactive)
                else:
                    cls.STAGE.add_property(prop, GRUPO_ITEMS, is_interactive)

    @classmethod
    def cargar_mobs(cls, extra_data, capa='capa_ground'):
        for key in cls.STAGE.data[capa]['mobs']:
            pos = cls.STAGE.data[capa]['mobs'][key]
            if key == 'npcs':
                clase = NPC

                for ref in pos:
                    data = Rs.abrir_json(Md.mobs + ref + '.json')
                    data.update(extra_data[ref])
                    for x, y in pos[ref]:
                        mob = clase(ref, x, y, data)
                        if capa == 'capa_ground':
                            cls.STAGE.add_property(mob, GRUPO_MOBS)

    @classmethod
    def cargar_hero(cls, entrada):
        x, y = cls.STAGE.data['entradas'][entrada]
        try:
            pc = MobGroup['heroe']
            Ed.HERO = pc
            Ed.HERO.ubicar(x, y)
            Ed.HERO.mapX = x
            Ed.HERO.mapY = y
            Ed.HERO.z = y + Ed.HERO.rect.h
            
        except (IndexError, KeyError, AttributeError):
            Ed.HERO = PC(Rs.abrir_json(Md.mobs + 'hero.json'), x, y)

        if Ed.HERO not in cls.STAGE.properties:
            Loader.STAGE.add_property(Ed.HERO, GRUPO_MOBS)

    @classmethod
    def cargar_salidas(cls):
        salidas = cls.STAGE.data['salidas']
        for salida in salidas:
            sld = Salida(salida, salidas[salida])
            cls.STAGE.add_property(sld, GRUPO_SALIDAS)
