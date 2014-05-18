from pygame import time, Surface
from base import _giftSprite

class Tiempo:
    FPS = time.Clock()
    _frames,_segs,_mins = 0,0,0 # valores internos
    hora,dia = 0,0 # valores con efecto en el juego.
    angulo_sol = 0
    esNoche = False
    
    nch_img = Surface((480,480))
    nch_img.set_alpha(125)
    noche = _giftSprite(nch_img)
    noche.ubicar(0,0)
    noche.dirty = 2
    noche.visible = False
        
    def contar_tiempo ():
        Tiempo._frames += 1
        if Tiempo._frames == 60:
            Tiempo._segs += 1
            Tiempo._frames = 0
            if Tiempo._segs == 60:
                Tiempo._mins += 1
                Tiempo.hora += 1
                Tiempo._segs = 0
                if Tiempo.hora < 12:
                    Tiempo.angulo_sol = Tiempo.hora*15
                    # 15 = 90º/6; 6 = 12 horas de luz/2 por el abs de sombra
                if Tiempo.hora == 24:
                    Tiempo.dia += 1
                    Tiempo.hora = 0
    
    def anochece(duracion):
        t = Tiempo.esNoche #debug
        if not Tiempo.esNoche:
            if Tiempo._mins == duracion:
                Tiempo.esNoche = True
                Tiempo.noche.visible = True
                Tiempo._mins = 0
        else:
            if Tiempo._mins == duracion:
                Tiempo.esNoche = False
                Tiempo.noche.visible = False
                Tiempo._mins = 0
        
        return Tiempo.esNoche
