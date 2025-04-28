# script.py
from importlib import import_module
from engine.globs import Game_State, ModData, Mob_Group
from engine.globs.event_dispatcher import EventDispatcher


def init_game(event):
    data = {"mapa": "new",
            "entrada": "center",
            "tiempo": [0, 13, 0],
            "focus": "heroe"}

    if 'savegame' in event.data:
        data.update(event.data['savegame'])

    EventDispatcher.trigger('LoadGame', 'Script', data)


def init_system(event):
    if event.data['intro']:
        module = import_module('data.scripts.intro', ModData.fd_scripts)

        # se supone que el modder sabe cómo se llama la función
        getattr(module, 'creditos_introduccion')()
    EventDispatcher.trigger('OpenMenu', 'Script', {'value': 'Principal'})


EventDispatcher.register(init_system, 'InitSystem')
EventDispatcher.register(init_game, 'NewGame')


def about(event):
    who = event.data['who']
    if who.nombre == Mob_Group.get_by_trait('occupation', 'hero'):
        Game_State.set2(f"dialog.{event.data['about']}.enabled")


EventDispatcher.register(about, 'TookItem')

# def set_monsters_attitude(event):
#     monsters = Mob_Group.get_by_trait('raza', 'blob')
#     if monsters is not None:
#         for monster in [monsters]:
#             monster.AI.set_context('hates', 'Apple')
#
#
# EventDispatcher.register(set_monsters_attitude, 'TookItem')
