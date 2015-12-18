from pygame import display as pantalla, init as py_init, image, event as Event, font, joystick
from engine.globs import Constants as C, Tiempo, EngineData as ED, ModData
from engine.misc import Resources as r, Config
from engine.IO.modos import Modo

py_init()
joystick.Joystick(0).init()
tamanio = C.ANCHO, C.ALTO
ModData.init(r.abrir_json("engine.ini"))
pantalla.set_caption(ModData.data['nombre'])
pantalla.set_icon(image.load(ModData.graphs + ModData.data['icono']))
fondo = pantalla.set_mode(tamanio)

fuente = font.SysFont('verdana', 16, bold=True)
rojo = 255,0,0
if Config.dato('mostrar_intro'): ModData.intro(fondo)

Event.set_blocked([1,4,5,6,17])
# all mouse- and video-related events

Modo.pop_menu('Debug')
while True:
    Tiempo.update(60)
    events = Event.get()
    Modo.juego(events)
    if ED.MODO == 'Aventura':
        cambios = Modo.aventura(events, fondo)
    elif ED.MODO == 'Dialogo':
        cambios = Modo.dialogo(events, fondo)
    elif ED.MODO == 'Menu':
        cambios = Modo.menu(events, fondo)

    cambios.append(fondo.blit(fuente.render(str(int(Tiempo.FPS.get_fps())), True, rojo), (10, 0)))
    cambios.append(fondo.blit(fuente.render(str(Tiempo.clock.timestamp()), True, rojo), (570, 0)))
    pantalla.update(cambios)
