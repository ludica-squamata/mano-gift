from engine.globs import GRUPO_ITEMS, GRUPO_MOBS
from engine.scenery import new_prop
from engine.globs import Mob_Group
from engine.misc import abrir_json
from engine.globs import ModData
from engine.mobs import PC, NPC
from .salida import Salida


def load_everything(alldata, x, y):
    loaded = []
    for mob in [load_hero(x, y)] + load_mobs(alldata):
        loaded.append((mob, GRUPO_MOBS))
    for prop in load_props(alldata):
        loaded.append((prop, GRUPO_ITEMS))
    return loaded


def load_something(alldata, x, y, requested):
    """
    :type requested: list
    :type alldata: dict
    :type x: int
    :type y: int
    """
    loaded = []
    if 'PC' in requested:
        loaded.append(([load_hero(x, y)], GRUPO_MOBS))

    if 'NPC' in requested:
        for mob in load_mobs(alldata):
            loaded.append((mob, GRUPO_MOBS))

    if 'Prop' in requested:
        for prop in load_props(alldata):
            loaded.append((prop, GRUPO_ITEMS))

    return loaded


def load_props(alldata):
    imgs = alldata['refs']
    pos = alldata['props']

    loaded_props = []
    for ref in pos:
        try:
            data = abrir_json(ModData.items + ref + '.json')
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


def load_mobs(alldata):
    loaded_mobs = []
    for key in alldata['mobs']:
        pos = alldata['mobs'][key]
        for x, y in pos:
            data = abrir_json(ModData.mobs + key + '.json')
            mob = NPC(key, x, y, data)
            loaded_mobs.append((mob, GRUPO_MOBS))

    return loaded_mobs


def load_hero(x, y):
    if 'heroe' in Mob_Group:
        return Mob_Group['heroe']
    else:
        return PC(abrir_json(ModData.mobs + 'hero.json'), x, y)


def cargar_salidas(alldata):
    salidas = []
    for datos in alldata['salidas']:
        nombre = datos['nombre']
        stage = datos['stage']
        rect = datos['rect']
        chunk = datos['chunk']
        entrada = datos['entrada']
        direcciones = datos['direcciones']

        salidas.append(Salida(nombre, stage, rect, chunk, entrada, direcciones))

    return salidas
