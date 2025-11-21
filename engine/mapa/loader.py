from pygame import mask as mask_module, Surface, SRCALPHA, Rect, Color
from engine.globs import ModData, GRUPO_MOBS, Prop_Group, EngineData
from engine.misc import abrir_json, cargar_imagen, Config
from engine.globs.renderer import Renderer
from os import path, getcwd, listdir
from engine.scenery import new_prop
from engine.libs import randint
from engine.mobs import Mob
from .salida import Salida
import csv
import sys


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

        if 'props' in requested and 'props' in alldata:
            for prop in load_props(parent, alldata):
                Prop_Group.add(prop[0].nombre, prop[0])
                loaded.append((prop, prop[0].grupo))

        if 'csv' in requested:
            for mob in load_mob_csv(parent, alldata):
                loaded.append((mob, GRUPO_MOBS))

        return loaded


def load_props(parent, alldata: dict):
    imgs = alldata.get('refs', {})
    pos = alldata['props']

    loaded_props = []
    img = None
    for ref in pos:
        data = None
        if ref in imgs:
            if imgs[ref].endswith('.json'):
                data = abrir_json(ModData.items + alldata['refs'][ref])
            else:
                img = cargar_imagen(ModData.graphs + imgs[ref])  # because it points to a .png file instead.
        elif path.exists(ModData.items + ref + '.json'):
            # use ref as filename, if it exists.
            data = abrir_json(ModData.items + ref + '.json')
        else:
            img = None  # resets the image to None to prevent wrong item duplication.

        for item in pos[ref]:
            x, y = alldata['entradas'][item]['pos'] if type(item) is str else item
            is_interactive = False

            x += parent.world_x
            y += parent.world_y

            if data is not None:
                prop = new_prop(parent, x, y, data=data)
                is_interactive = hasattr(prop, 'accionable') and prop.accionable
            elif img is not None:
                prop = new_prop(parent, x, y, nombre=ref, img=img)
            else:
                print(f'Prop "{ref}" is invalid. Declare its path on the map "refs" to load.')
                prop = None

            if type(prop) is list:
                for p in prop:
                    is_interactive = p.accionable
                    loaded_props.append((p, is_interactive))
            elif prop is not None:
                loaded_props.append((prop, is_interactive))

    return loaded_props


def load_mobs(parent, alldata: dict):
    loaded_mobs = []
    for name in alldata.get('mobs', []):
        pos = alldata['mobs'][name]
        for i, item in enumerate(pos):
            if type(item) is str:
                x, y = alldata['entradas'][item]['pos']
            else:
                x, y = item

            if name in alldata['refs']:
                data = abrir_json(alldata['refs'][name])

            elif name in ModData.character_generator:
                data = ModData.character_generator[name](i)

            elif path.exists(ModData.fd_player + name + '.json'):
                data = abrir_json(ModData.fd_player + name + '.json')
                alldata['focus'] = name

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


def load_mob_csv(parent, all_data):
    loaded_mobs = []
    if path.exists(path.join(Config.savedir, 'mobs.csv')):
        ruta = path.join(Config.savedir, 'mobs.csv')
        fieldnames = ['name', 'x', 'y', 'id', 'chunk_name', 'adress']
        with open(ruta) as cvsfile:
            reader = csv.DictReader(cvsfile, fieldnames=fieldnames, delimiter=';')
            filname_list = [filename[:-5] for filename in listdir(ModData.mobs) if filename.endswith('.json')]
            name_list = [abrir_json(ModData.mobs + filename + '.json')['nombre'] for filename in filname_list]

            for row in [row for row in reader if row['chunk_name'] == parent.nombre]:
                name = row['name']
                x, y = int(row['x']), int(row['y'])
                a, b = row['adress'].split(',')
                adress = (int(a), int(b))
                if tuple(parent.adress) == adress:
                    if 'refs' in all_data and name in all_data['refs']:
                        data = abrir_json(all_data['refs'][name])

                    elif path.exists(ModData.mobs + name + '.json'):
                        data = abrir_json(ModData.mobs + name + '.json')

                    elif name in name_list:
                        filname = filname_list[name_list.index(name)]
                        data = abrir_json(ModData.mobs + filname + '.json')

                    elif name in ModData.character_generator:
                        data = ModData.character_generator[name]()

                    elif path.exists(ModData.fd_player + name + '.json'):
                        data = abrir_json(ModData.fd_player + name + '.json')
                        all_data['focus'] = name

                    data['id'] = row['id']
                    if NamedNPCs.npcs_with_ids is not None:
                        ids, names = NamedNPCs.npcs_with_ids
                        if data['nombre'] in names:
                            idx = names.index(data['nombre'])
                            if data.get('id', None) is None:
                                data['id'] = ids[idx]
                                del names[idx], ids[idx]

                    try:
                        mob = Mob(parent, x, y, data, focus=all_data.get('focus', False))
                        loaded_mobs.append((mob, GRUPO_MOBS))
                    except KeyError:
                        # the hero might not be in the chunk, creating a error while he is being loaded.
                        # This try/except clause catches the exception because the hero is added
                        # to the map from the outside.
                        pass

    return loaded_mobs


def load_chunks_csv(csv_file, silently=False):
    """Creates the json-dicts for each chunk from a csv file. These dicts are incomplete since they lack
    references to mobs or props, but due to the nature of dicts, such info could be added later.
    """
    with open(path.join(getcwd(), 'data', 'maps', csv_file)) as cvsfile:
        reader = csv.DictReader(cvsfile, fieldnames=['adress', 'id', 'sup', 'inf', 'izq', 'der',
                                                     'fondo', 'colisiones', 'terrain', 'latitude'], delimiter=';')
        chunks_data = {}
        silently = True if 'debug' not in sys.argv else silently
        for i, row in enumerate(reader):

            ad_x, ad_y = row['adress'].strip("[]").split(',')
            chunk_data = {
                'limites': {
                    'sup': None if row['sup'] == 'null' else row['sup'],
                    'inf': None if row['inf'] == 'null' else row['inf'],
                    'izq': None if row['izq'] == 'null' else row['izq'],
                    'der': None if row['der'] == 'null' else row['der']
                },
                "adress": [int(ad_x), int(ad_y)],
                "terrain": row['terrain'],
                'latitude': int(row['latitude'])
            }
            if not silently:
                chunk_data.update({
                    'fondo': cargar_imagen(ModData.graphs + row['fondo']),
                    'colisiones': None if row['colisiones'] == 'null' else cargar_imagen(
                        ModData.graphs + row['colisiones']),
                })
            else:
                chunk_data.update({
                    'fondo': row['fondo'],
                    'colisiones': None if row['colisiones'] == 'null' else row['colisiones']
                })
            chunks_data[row['id']] = chunk_data

            if not silently:
                EngineData.MENUS['loading'].actualizar(round(i / 756, 2))
                Renderer.update()

    ModData.preloaded_chunk_csv[csv_file] = chunks_data
    return chunks_data


def load_props_csv(csv_file, silently=True):
    with open(path.join(getcwd(), 'data', 'maps', csv_file), encoding='utf-8') as cvsfile:
        reader = csv.DictReader(cvsfile, fieldnames=['adress', 'pos', "ruta"], delimiter=';')

        data = {}
        for row in reader:
            ad_x, ad_y = row['adress'].strip("[]").split(',')
            x, y = row['pos'].strip("[]").split(',')
            ruta = row['ruta']
            nombre = ruta[6:-7]

            data[(int(ad_x), int(ad_y))] = {
                'pos': (int(x), int(y)),
                'nombre': nombre,
            }
            if not silently:
                data.update({
                    'imagen': cargar_imagen(ModData.graphs + ruta)
                })
            else:
                data.update({
                    'imagen': ruta  # because it points to a .png file.
                })

        return data


def cargar_salidas(chunk, all_data):
    salidas = {}
    img = Surface((800, 800), SRCALPHA)
    # la imagen de colisiones tiene SRCALPHA porque necesita tener alpha = 0

    for i, datos in enumerate(all_data):
        nombre = datos['nombre']
        stage = datos['stage']
        prop = None
        if 'prop' in datos and datos['prop'] is not None:
            prop = Prop_Group[datos['prop'].capitalize()]
            accion = prop.accion
            rect = Rect(0, 0, *prop.rect.size)
            rect.center = prop.rect.bottomright
        else:
            accion = 'caminar'
            rect = Rect(datos['rect'])

        entrada = datos['entrada']
        direcciones = datos['direcciones']
        id = ModData.generate_id()
        r, g, b, a = randint(0, 255), i % 255, i // 255, 255
        color = Color(r, g, b, a)
        # r ahora es randint para que cada salida tenga un color diferente en el debuggin.
        # esto es posible porque R no tiene efecto a la hora de detectar la colisión.
        salida = Salida(nombre, id, stage, rect, chunk, entrada, direcciones, accion, color)
        if prop is not None:
            prop.salida = salida
        salidas[b * 255 + g] = salida

        # pintamos el área de la salida con el color-código en GB. R y A permanecen en 255.
        # después se usará b*255+g para devolver el index.
        img.fill((r, g, b, a), rect)

    # la mascara se usa para la detección de colisiones.
    # las partes no pintadas tienen un alpha = 0, por lo que la mascara en esos lugares
    # permanece unset.
    mask = mask_module.from_surface(img)

    return salidas, mask, img
    # salidas: la lista de salidas, igual que siempre.
    # mask: máscara de colisiones de salidas.
    # img: imagen de colores codificados
