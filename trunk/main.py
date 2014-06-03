from pygame import display as pantalla,init as py_init,image,event as EVENT
from engine.globs import Constants as C, World as W, Tiempo as T
from engine.quests import QuestManager
from engine.UI.modos import modo
from engine.misc import Resources as r, Config, Util as U
from os import getcwd as cwd, path

py_init()
tamanio = C.ANCHO, C.ALTO
ini = r.abrir_json("engine.ini")
folder = path.normpath(path.join(cwd(),ini['folder']))
if not path.exists(folder):
    folder = path.normpath(ini['folder'])
    if not path.exists(folder):
        U.salir("la ruta no existe")
W.m = folder
mod = r.abrir_json(folder+'/mod.json')

pantalla.set_caption(mod['nombre'])
pantalla.set_icon(image.load(mod['icono']))
fondo = pantalla.set_mode(tamanio)
W.setear_mapa(mod['inicial'], 'inicial')
#if Config.dato('mostrar_intro'): anim = intro(fondo)
#init = introduccion()
#init.ejecutar(fondo)

while True:
    T.FPS.tick(60)
    T.contar_tiempo()
    QuestManager.update()
    events = EVENT.get()
    modo.Juego(events)
    if W.MODO == 'Aventura':
        cambios = modo.Aventura(events,fondo)
    elif W.MODO == 'Dialogo':
        cambios = modo.Dialogo(events,fondo)
    elif W.MODO == 'Menu':
        cambios = modo.Menu(events,fondo) 
    
    if W.onPause:
        W.menu_actual.update()
    pantalla.update(cambios)

