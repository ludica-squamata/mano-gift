from engine.libs import choice
from os import path, getcwd, listdir
from engine.misc import abrir_json


def generate_random_chars(puntos=50):
    engine_data = abrir_json(path.join(getcwd(), 'engine.json'))
    data = abrir_json(path.join(engine_data['folder'], engine_data['data_file']))
    char_names = [i for i in data['caracteristicas']]
    puntuacion = [0] * len(char_names)
    while puntos > 0:
        chosen = choice(char_names)
        idx = char_names.index(chosen)
        puntuacion[idx] += 1
        puntos -= 1

    return dict(zip(char_names, puntuacion))


def choose_a_head():
    ruta = path.join(getcwd(), 'data', 'grafs', 'mobs', 'imagenes')
    choices = []
    for file in listdir(ruta):
        if file.startswith('heads'):
            choices.append('mobs/imagenes/' + file)

    chosen = choice(choices)
    return chosen


def choose_a_body():
    # stub until more bodies become available.
    pass


def gen_chararcter():
    d = {
        "nombre": "aristocrat",
        "raza": "human",
        "atributos": generate_random_chars(),
        "imagenes": {
            "heads": choose_a_head(),
            "atk": None,
            "death": None,
            "idle": "mobs/imagenes/aristocrat_idle_walk_body.png",
            "diag_face": "mobs/imagenes/npc_face.png"
        },
        "alpha": "mobs/colisiones/human_walk.png",
        "AI": "ai"
    }
    return d
