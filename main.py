from pygame import display as pantalla,init as py_init,image,event as EVENT
from engine.globs import Constants as C, Tiempo as T, EngineData as ED, ModData
from engine.quests import QuestManager
from engine.IO.modos import modo
from engine.misc import Resources as r, Config
from data import intro,introduccion
from pygame import font
py_init()
tamanio = C.ANCHO, C.ALTO
ModData.init(r.abrir_json("engine.ini"))
pantalla.set_caption(ModData.data['nombre'])
pantalla.set_icon(image.load(ModData.data['icono']))
fondo = pantalla.set_mode(tamanio)

fuente = font.SysFont('verdana',16,bold=True)
if Config.dato('mostrar_intro'): anim = intro(fondo)
init = introduccion()
init.ejecutar(fondo)

while True:
    T.FPS.tick(60)
    render = fuente.render(str(int(T.FPS.get_fps())),True,(255,0,0))
    T.contar_tiempo()
    QuestManager.update()
    events = EVENT.get()
    modo.Juego(events)
    if ED.MODO == 'Aventura':
        cambios = modo.Aventura(events,fondo)
    elif ED.MODO == 'Dialogo':
        cambios = modo.Dialogo(events,fondo)
    elif ED.MODO == 'Menu':
        cambios = modo.Menu(events,fondo) 
    
    if ED.onPause:
        ED.menu_actual.update()
    fondo.blit(render,(10,0))
    pantalla.update(cambios)

