from pygame import display as pantalla,init as py_init,image,event as EVENT, font
from engine.globs import Constants as C, Tiempo as T, EngineData as ED, ModData
from engine.quests import QuestManager
from engine.IO.modos import modo
from engine.misc import Resources as r, Config

py_init()
tamanio = C.ANCHO, C.ALTO
ModData.init(r.abrir_json("engine.ini"))
pantalla.set_caption(ModData.data['nombre'])
pantalla.set_icon(image.load(ModData.graphs+ModData.data['icono']))
fondo = pantalla.set_mode(tamanio)

fuente = font.SysFont('verdana',16,bold=True)
#if Config.dato('mostrar_intro'): anim = intro(fondo)

modo._popMenu('Debug')
while True:
    T.FPS.tick(60)
    T.contar_tiempo()
    QuestManager.update()
    events = EVENT.get([2,3,12]) # es ligeramente más eficiente
    EVENT.clear() # no itererar sobre lo que no nos interesa
    
    modo.Juego(events)
    if ED.MODO == 'Aventura':
        cambios = modo.Aventura(events,fondo)
    elif ED.MODO == 'Dialogo':
        cambios = modo.Dialogo(events,fondo)
    elif ED.MODO == 'Menu':
        cambios = modo.Menu(events,fondo)
    
    cambios.append(fondo.blit(fuente.render(str(int(T.FPS.get_fps())),True,(255,0,0)),(10,0)))
    
    pantalla.update(cambios)

