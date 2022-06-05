from pygame import mask as mask_module, Surface, SRCALPHA
from engine.misc import abrir_json, cargar_imagen
from engine.globs import GRUPO_ITEMS, GRUPO_MOBS
from engine.scenery import new_prop
from engine.globs import ModData
from engine.mobs import Mob
from .salida import Salida


def load_everything(alldata: dict):
    loaded = []
    for mob in load_mobs(alldata):
        loaded.append((mob, GRUPO_MOBS))
    for prop in load_props(alldata):
        loaded.append((prop, GRUPO_ITEMS))
    return loaded


def load_something(alldata: dict, requested: str):
    """
    :type requested: list
    :type alldata: dict
    """
    loaded = []
    if requested is not None:
        if 'mobs' in requested:
            for mob in load_mobs(alldata):
                loaded.append((mob, GRUPO_MOBS))

        if 'props' in requested:
            for prop in load_props(alldata):
                loaded.append((prop, prop[0].grupo))

        return loaded


def load_props(alldata: dict):
    imgs = alldata.get('refs', {})
    pos = alldata['props']

    loaded_props = []
    img = None
    for ref in pos:
        if ref in imgs:
            if imgs[ref].endswith('.json'):
                data = abrir_json(ModData.items + alldata['refs'][ref])
            else:
                img = cargar_imagen(ModData.graphs + imgs[ref])  # because it points to a .png file instead.
                data = False
        else:
            # use ref as filename
            data = abrir_json(ModData.items + ref + '.json')

        for item in pos[ref]:
            if type(item) is str:
                x, y = alldata['entradas'][item]['pos']
            else:
                x, y = item

            if data:
                prop = new_prop(x, y, data=data)
                is_interactive = hasattr(prop, 'accionable') and prop.accionable
            else:
                prop = new_prop(x, y, nombre=ref, img=img)
                is_interactive = False

            if type(prop) is list:
                for p in prop:
                    is_interactive = p.accionable
                    loaded_props.append((p, is_interactive))
            else:
                loaded_props.append((prop, is_interactive))

    return loaded_props


def load_mobs(alldata: dict):
    loaded_mobs = []
    for name in alldata['mobs']:
        pos = alldata['mobs'][name]
        for i, item in enumerate(pos):
            if type(item) is str:
                x, y = alldata['entradas'][item]['pos']
            else:
                x, y = item

            if name in alldata['refs']:
                data = abrir_json(alldata['refs'][name])
            elif name in ModData.character_generator:
                data = ModData.character_generator[name]()
            else:
                data = abrir_json(ModData.mobs + name + '.json')
            mob = Mob(x, y, data)
            loaded_mobs.append((mob, GRUPO_MOBS))

    return loaded_mobs


def cargar_salidas(mapa, alldata, size):
    salidas = []
    img = Surface(size, SRCALPHA)
    # la imagen de colisiones tiene SRCALPHA porque necesita tener alpha = 0
    for i, datos in enumerate(alldata['salidas']):
        nombre = datos['nombre']
        stage = datos['stage']
        rect = datos['rect']
        chunk = datos['chunk']
        entrada = datos['entrada']
        direcciones = datos['direcciones']
        id = ModData.generate_id()

        salidas.append(Salida(nombre, id, mapa, stage, rect, chunk, entrada, direcciones))
        r, g, b, a = 255, i % 255, i // 255, 255
        # pintamos el área de la salida con el color-código en GB. R y A permanecen en 255.
        # después se usará b*255+g para devolver el index.
        img.fill((r, g, b, a), rect)

    # la mascara se usa para la detección de colisiones.
    # las partes no pintadas tienen un alpha = 0, por lo que la mascara en esos lugares
    # permanece unset.
    mask = mask_module.from_surface(img)

    return salidas, mask, img
