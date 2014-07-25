from pygame import time, Surface, draw, PixelArray, SRCALPHA
from engine.base import _giftSprite
from engine.misc import Resources as r

class Noche(_giftSprite):
    def __init__(self,size):
        #############################
        if 1: #cambiar a 0 para prueba de luces
            img = Surface(size)
            img.fill((0,0,125))
            img.set_alpha(230)
            self.rect = img.get_rect()
            super().__init__(img)
        #############################
        else:
            from engine.misc import Resources as r
            img = Surface(size, SRCALPHA)
            img.fill((0,0,0,230)) #llenamos con color rgba. como es srcalpha funciona bien
            pxArray = PixelArray(img)
            
            lights = []
            colorIgnorado = (1,1,1) #este es el color para las secciones que no se renderean, sino siempre se borra un cuadrado. el alpha no importa
                                    #deberiamos definirlo en documentacion
            surf = Surface((80,80), SRCALPHA)
            surf.fill(colorIgnorado)
            draw.circle(surf, (127,0,127,127), (40,40) ,40)
            
            lights.append([{"x":400,"y":600}, surf])
            
            surf = r.cargar_imagen('degrade.png')
            rect = surf.get_rect()
            rect.x = 600
            rect.y = 600
            
            lights.append([rect, surf])
            
            surf = Surface((100,100), SRCALPHA) #luz de dia, 0,0,0,0. probe y sin SRCALPHA no funciona
            surf.set_alpha(0)
            lights.append([{"x":500,"y":800}, surf])
            
            def clamp(n):
                return 0 if n<0 else 255 if n>255 else n
            
            imap = img.unmap_rgb #cache para velocidad
            
            for l in lights:
                lightArray = PixelArray(l[1])
                if type(l[0]) is dict:
                    lx = l[0]["x"]
                    ly = l[0]["y"]
                else: #suponemos Rect
                    lx = l[0].x
                    ly = l[0].y
                lmap = l[1].unmap_rgb
                for y in range(0, l[1].get_width()):
                    for x in range(0, l[1].get_height()):
                        ox, oy = lx + x, ly + y
                        r,g,b,a = lmap(lightArray[x,y]) #hay que usar el motodo unmap_rgb de la instancia de surface que corresponde
                        if ((r,g,b) != colorIgnorado):
                            _r,_g,_b,_a = imap(pxArray[ox, oy])
                            r = clamp(r+_r)
                            g = clamp(g+_g)
                            b = clamp(b+_b)
                            a = clamp(_a -(255-a))
                            pxArray[ox,oy] = r,g,b,a
            nch = pxArray.make_surface()
            self.rect = nch.get_rect()
            super().__init__(nch)
        ##############################
        
        self.ubicar(0,0)
        self.dirty = 2

class Tiempo:
    FPS = time.Clock()
    _frames,_segs,_mins = 0,0,0 # valores internos
    hora,dia = 0,0 # valores con efecto en el juego.
    angulo_sol = 0
    esNoche = False
    noche = None
    
    @staticmethod
    def setear_momento(dia,hora):
        Tiempo.dia = dia
        Tiempo.hora = hora
        Tiempo._mins = hora
    
    @staticmethod
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
                    Tiempo._mins = 0
    
    @staticmethod
    def oscurecer(limite):
        alpha = Tiempo.noche.image.get_alpha()
        if alpha < limite:
            Tiempo.noche.image.set_alpha(alpha+1)

    @staticmethod
    def aclarar():
        alpha = Tiempo.noche.image.get_alpha()
        Tiempo.noche.image.set_alpha(alpha-1)
            
    @staticmethod
    def crear_noche(tamanio):
        Tiempo.noche = Noche(tamanio)
    
