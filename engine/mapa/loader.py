from pygame import mask as mask_module, Surface, SRCALPHA, Rect, Color
from engine.globs import ModData, GRUPO_MOBS, Prop_Group
from engine.misc import abrir_json, cargar_imagen
from engine.scenery import new_prop
from engine.libs import randint
from engine.mobs import Mob
from .salida import Salida


class NamedNPCs:
    npcs_with_ids = None


def load_something(parent, alldata: dict, requested: str):
    """
    :type requested: list
    :type alldata: dict
    :type parent: ChunkMap
    """
    loaded = []
    if requested is not None:
        if 'mobs' in requested:
            for mob in load_mobs(parent, alldata):
                loaded.append((mob, GRUPO_MOBS))

        if 'props' in requested:
            for prop in load_props(parent, alldata):
                Prop_Group.add(prop[0].nombre, prop[0])
                loaded.append((prop, prop[0].grupo))

        return loaded


def load_props(parent, alldata: dict):
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
                prop = new_prop(parent, x, y, data=data)
                is_interactive = hasattr(prop, 'accionable') and prop.accionable
            else:
                prop = new_prop(parent, x, y, nombre=ref, img=img)
                is_interactive = False

            if type(prop) is list:
                for p in prop:
                    is_interactive = p.accionable
                    loaded_props.append((p, is_interactive))
            else:
                loaded_props.append((prop, is_interactive))

    return loaded_props


def load_mobs(parent, alldata: dict):
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

            if NamedNPCs.npcs_with_ids is not None:
                ids, names = NamedNPCs.npcs_with_ids
                if data['nombre'] in names:
                    idx = names.index(data['nombre'])
                    data['id'] = ids[idx]
                    del names[idx], ids[idx]

            mob = Mob(parent, x, y, data, focus=alldata.get('focus', False))
            loaded_mobs.append((mob, GRUPO_MOBS))

    return loaded_mobs


def cargar_salidas(parent, alldata):
    salidas = []
    img = Surface((800, 800), SRCALPHA)
    # la imagen de colisiones tiene SRCALPHA porque necesita tener alpha = 0
    chunk = None
    for i, datos in enumerate(alldata):
        nombre = datos['nombre']
        stage = datos['stage']
        rect = Rect(datos['rect'])
        chunk = parent.get_chunk_by_adress(datos['chunk_adress'])
        entrada = datos['entrada']
        direcciones = datos['direcciones']
        id = ModData.generate_id()

        r, g, b, a = randint(0, 255), i % 255, i // 255, 255
        # r ahora es randint para que cada salida tenga un color diferente en el debuggin.
        # esto es posible porque R no tiene efecto a la hora de detectar la colisión.
        color = Color(r, g, b, a)
        salidas.append(Salida(nombre, id, stage, rect, chunk, entrada, direcciones, color))

        # pintamos el área de la salida con el color-código en GB. R y A permanecen en 255.
        # después se usará b*255+g para devolver el index.
        img.fill((r, g, b, a), rect)

    # la mascara se usa para la detección de colisiones.
    # las partes no pintadas tienen un alpha = 0, por lo que la mascara en esos lugares
    # permanece unset.
    mask = mask_module.from_surface(img)

    chunk.set_salidas(salidas, mask, img)
    # salidas: la lista de salidas, igual que siempre.
    # mask: máscara de colisiones de salidas.
    # img: imagen de colores codificados
