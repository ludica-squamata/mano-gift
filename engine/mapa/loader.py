from engine.globs import EngineData as Ed, Constants as Cs, MobGroup, ModData as Md
from engine.misc import Resources as Rs
from engine.mobs import NPCSocial, PC
from engine.quests import QuestManager
from engine.scenery import newProp
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
        cls.cargar_quests()
        cls.cargar_salidas()

    @classmethod
    def cargar_props(cls, ):
        imgs = cls.STAGE.data['refs']
        """:type imgs: dict"""
        pos = cls.STAGE.data['capa_ground']['props']

        for ref in pos:
            try:
                data = Rs.abrir_json(Md.items + ref + '.json')
                if ref in imgs:
                    imagen = Rs.cargar_imagen(imgs[ref])
                else:
                    imagen = Rs.cargar_imagen(data['image'])
            except IOError:
                data = False
                imagen = Rs.cargar_imagen(imgs[ref])

            for x, y in pos[ref]:
                if data:
                    prop = newProp(ref, imagen, x, y, data)
                    add_interactive = True
                else:
                    prop = newProp(ref, imagen, x, y)
                    add_interactive = False

                cls.STAGE.add_property(prop, Cs.CAPA_GROUND_ITEMS, add_interactive)

    @classmethod
    def cargar_mobs(cls, extra_data, capa = 'capa_ground'):
        for key in cls.STAGE.data[capa]['mobs']:
            pos = cls.STAGE.data[capa]['mobs'][key]
            if key == 'npcs':
                clase = NPCSocial

                for ref in pos:
                    data = Rs.abrir_json(Md.mobs + ref + '.json')
                    data.update(extra_data[ref])
                    for x, y in pos[ref]:
                        mob = clase(ref, x, y, data)
                        if capa == 'capa_ground':
                            cls.STAGE.add_property(mob, Cs.CAPA_GROUND_MOBS)
                        elif capa == 'capa_top':
                            cls.STAGE.add_property(mob, Cs.CAPA_TOP_MOBS)

    @classmethod
    def cargar_hero(cls, entrada):
        x, y = cls.STAGE.data['entradas'][entrada]
        try:
            pc = MobGroup['heroe']
            Ed.HERO = pc
            Ed.HERO.ubicar(x, y)
            Ed.HERO.mapX = x
            Ed.HERO.mapY = y
        except (IndexError, KeyError, AttributeError):
            Ed.HERO = PC(Rs.abrir_json(Md.mobs + 'hero.json'), x, y)

        Loader.STAGE.add_property(Ed.HERO, Cs.CAPA_HERO)

    @classmethod
    def cargar_quests(cls, ):
        if 'quests' in cls.STAGE.data:
            for quest in cls.STAGE.data['quests']:
                QuestManager.add(quest)

    @classmethod
    def cargar_salidas(cls):
        salidas = cls.STAGE.data['salidas']
        for salida in salidas:
            sld = Salida(salida, salidas[salida])
            cls.STAGE.add_property(sld, Cs.CAPA_GROUND_SALIDAS)
