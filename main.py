from pygame import display as pantalla, init as py_init, event, font, joystick, image
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import Tiempo, ModData, ANCHO, ALTO
from engine.IO.taphold import get_taphold_events
from engine.misc import abrir_json, Config
from engine.globs.renderer import Renderer
import os

py_init()
for idx in range(joystick.get_count()):
    joystick.Joystick(idx).init()
ModData.init(abrir_json("engine.json"))
pantalla.set_caption(ModData.data['nombre'])
pantalla.set_icon(image.load(ModData.graphs + ModData.data['icono']))
os.environ['SDL_VIDEO_CENTERED'] = "{!s},{!s}".format(0, 0)
fondo = pantalla.set_mode((ANCHO, ALTO))
event.set_blocked([1, 4, 5, 6, 17])  # all mouse- and video-related events
cambios = []

fuente = font.SysFont('verdana', 16, bold=True)
rojo = 255, 0, 0

EventDispatcher.trigger('InitSystem', 'engine', {'intro': Config.dato('mostrar_intro')})  # init_system

while True:
    Tiempo.update(60)
    EventDispatcher.process()
    get_taphold_events(event.get())
    cambios = Renderer.update()

    cambios.append(fondo.blit(fuente.render(str(int(Tiempo.FPS.get_fps())), True, rojo), (10, 0)))
    cambios.append(fondo.blit(fuente.render(str(Tiempo.clock.timestamp()), True, rojo), (570, 0)))
    pantalla.update(cambios)
