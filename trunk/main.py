from pygame import display as pantalla,init as py_init,image,event as EVENT
from engine.globs import Constants as C, Tiempo as T, EngineData as ED, ModData
from engine.quests import QuestManager
from engine.UI.modos import modo
from engine.misc import Resources as r, Config

py_init()
tamanio = C.ANCHO, C.ALTO
ModData.init(r.abrir_json("engine.ini"))
pantalla.set_caption(ModData.data['nombre'])
pantalla.set_icon(image.load(ModData.data['icono']))
fondo = pantalla.set_mode(tamanio)
#if mod['inicial']
ED.MODO = ModData.data['initial_mode']
ED.setear_mapa(ModData.data['inicial'], 'inicial')
#if Config.dato('mostrar_intro'): anim = intro(fondo)
#init = introduccion()
#init.ejecutar(fondo)

while True:
    T.FPS.tick(60)
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
    pantalla.update(cambios)

