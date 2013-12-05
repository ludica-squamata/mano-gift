from pygame import display as pantalla,font,image,event as EVENT
from globs import Constants as C, World as W, Tiempo as T, QuestManager
from intro import introduccion,intro_animation
from UI.modos import modo

tamanio = C.ALTO, C.ANCHO
font.init()
pantalla.set_caption('Proyecto Mano-Gift')
pantalla.set_icon(image.load('grafs/favicon.png'))
fondo = pantalla.set_mode(tamanio) # surface

anim = intro_animation()
anim.go(fondo)

init = introduccion(C.ANCHO-20,C.ALTO-20)
init.ejecutar(fondo)

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

