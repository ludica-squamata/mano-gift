from engine.globs import GRUPO_ITEMS, GRUPO_MOBS
from engine.scenery import new_prop
from engine.misc import abrir_json
from engine.globs import ModData
from engine.mobs import Mob
from .salida import Salida


def load_everything(alldata):
    loaded = []
    for mob in load_mobs(alldata):
        loaded.append((mob, GRUPO_MOBS))
    for prop in load_props(alldata):
        loaded.append((prop, GRUPO_ITEMS))
    return loaded


def load_something(alldata, requested):
    """
    :type requested: list
    :type alldata: dict
    """
    loaded = []

    if 'Mob' in requested:
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
    for name in alldata['mobs']:
        pos = alldata['mobs'][name]
        for x, y in pos:
            data = abrir_json(ModData.mobs + name + '.json')
            mob = Mob(x, y, data)
            loaded_mobs.append((mob, GRUPO_MOBS))

    return loaded_mobs


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
