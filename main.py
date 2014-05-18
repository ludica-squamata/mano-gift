from pygame import display as pantalla,init as py_init,image,event as EVENT
from globs import Constants as C, World as W, Tiempo as T
from quests import QuestManager
from intro import introduccion, intro
from UI.modos import modo
from misc import Resources as r, Config
from script import run
tamanio = C.ANCHO, C.ALTO
py_init()
pantalla.set_caption('Proyecto Mano-Gift')
pantalla.set_icon(image.load('data/grafs/favicon.png'))
fondo = pantalla.set_mode(tamanio) # surface

if Config.dato('mostrar_intro'): anim = intro(fondo)
init = introduccion()
init.ejecutar(fondo)

while True:
    T.FPS.tick(60)
    T.contar_tiempo()
    run()
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

