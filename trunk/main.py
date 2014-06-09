from pygame import display as pantalla,init as py_init,image,event as EVENT
from engine.globs import Constants as C, Tiempo as T, EngineData as ED, ModData as MD
from engine.quests import QuestManager
from engine.UI.modos import modo
from engine.misc import Resources as r, Config, Util as U

py_init()
tamanio = C.ANCHO, C.ALTO
ini = r.abrir_json("engine.ini")
if not MD.find_mod_folder(ini):
    U.salir("la ruta no existe")

mod = MD.get_file_data('mod.json')
pantalla.set_caption(mod['nombre'])
pantalla.set_icon(image.load(mod['icono']))
fondo = pantalla.set_mode(tamanio)
#if mod['inicial']
ED.setear_mapa(mod['inicial'], 'inicial')
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

