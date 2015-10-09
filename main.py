from pygame import display as pantalla, init as py_init, image, event as EVENT, font
from engine.globs import Constants as C, Tiempo, EngineData as ED, ModData
from engine.misc import Resources as r, Config
from engine.quests import QuestManager
from engine.IO.modos import Modo

py_init()
tamanio = C.ANCHO, C.ALTO
ModData.init(r.abrir_json("engine.ini"))
pantalla.set_caption(ModData.data['nombre'])
pantalla.set_icon(image.load(ModData.graphs + ModData.data['icono']))
fondo = pantalla.set_mode(tamanio)

fuente = font.SysFont('verdana', 16, bold=True)
if Config.dato('mostrar_intro'): ModData.intro(fondo)

Modo._popMenu('Debug')
while True:
    Tiempo.update(60)
    QuestManager.update()
    events = EVENT.get([2, 3, 12])  # es ligeramente más eficiente
    EVENT.clear()  # no itererar sobre lo que no nos interesa

    Modo.juego(events)
    if ED.MODO == 'Aventura':
        cambios = Modo.aventura(events, fondo)
    elif ED.MODO == 'Dialogo':
        cambios = Modo.dialogo(events, fondo)
    elif ED.MODO == 'Menu':
        cambios = Modo.menu(events, fondo)

    cambios.append(fondo.blit(fuente.render(str(int(Tiempo.FPS.get_fps())), True, (255, 0, 0)), (10, 0)))
    cambios.append(fondo.blit(fuente.render(str(Tiempo.clock.timestamp()), True, (255, 0, 0)), (570, 0)))
    pantalla.update(cambios)