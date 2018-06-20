from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from engine.misc import abrir_json, Config
from engine.globs import Tiempo, ModData
from pygame import init as py_init
from engine.IO import taphold

py_init()
ModData.init(abrir_json("engine.json"))
Renderer.init(ModData.data['nombre'], ModData.graphs + ModData.data['icono'])
taphold.init()

EventDispatcher.trigger('InitSystem', 'engine', {'intro': Config.dato('mostrar_intro')})  # init_system
while True:
    Tiempo.update(60)
    EventDispatcher.process()
    taphold.get_events()
    Renderer.update()
