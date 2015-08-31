﻿from engine.globs import EngineData as ED, Constants as C
from pygame import Surface, Rect, draw, SRCALPHA
from engine.misc import Resources as r
from engine.base import _giftSprite

class LightSource(_giftSprite): #o combinar esto con prop?, no estoy seguro. probablemente de esta forma pueda tener mas flexibilidad
    '''Los objetos de esta clase tienen un area de luz, que permite ver y genera sombras'''
    color = 0,0,0,0
    origen = None #una coordenada desde donde se calcula el area. por ejemplo para un poste con iluminacion en la punta? por defecto center
    
    estatico = False #para simular luces lejanas, como el sol. no les cambia el rect.pos
    encendido = True #apaguen esas luces!
    #animacion???
    nombre = 'luz'
    
    def __init__ (self,imagen,x,y):
        super().__init__(imagen)
        self.ubicar(x,y)
        # self.color = color
        # self.forma = forma
        # self.origen = self.rect.center
        
        # imagen = self._crear(40)
        # self.rect = imagen.get_rect(center = self.origen)
        # super().__init__(imagen,x = self.rect.x,y=self.rect.y)
        # ED.RENDERER.addFgObj(self)
        #setear el resto de las propiedades del area de luz
        #registrarse en Stage como fuente de luz para recibir actualizaciones
    
    @staticmethod
    def _crear_base(tamanio):
        surf = Surface((tamanio,tamanio), SRCALPHA)
        #este es el color para las secciones que no se renderean,
        surf.fill(C.COLOR_IGNORADO)#sino siempre se borra un cuadrado. el alpha no importa
        #deberiamos definirlo en documentacion
        
        return surf
    
    def update(self):
        #revisar todos los Mob y Prop con sombra dentro del area de luz y setearles sus respectivas sombras
        pass

class ImageLight(LightSource):
    def __init__(self,ruta):
        img = r.cargar_imagen(ruta)
        super().__init__(img,x,y)

class SpotLight(LightSource):
    """Para luces circulares que no ocupan toda la pantalla"""
    def __init__(self,radio,color,x,y):
        img = self._crear(radio,color)
        super().__init__(img,x,y)
    
    def _crear(self,radio,color):
        base = self._crear_base(radio*2)
        if len(color) <4:
            raise ValueError('el color debe ser rgba')        
        draw.circle(base, color, (radio,radio) ,radio)
        return base

class GradientSpotLight(LightSource):
    def __init__(self,radio,color):
        img = self._crear(radio,color)
        super().__init__(img,x,y)
    
    def _crear(self,radio,color,step=1):
        base = self._crear_base(radio*2)
        if len(color) <4:
            raise ValueError('el color debe ser rgba')
        else:
            r,g,b,a = color
        _a = -step
        _r = radio
        while _r >= 0: 
            _a += step #cuanto más bajo el radio, más alto tiene que ser el step. 255=>1; 50=>5
            if _a > a: # este máximo es seteable hasta 255
                _a = a # cuanto más bajo esté, menos degradé
            color = r,g,b,_a
            draw.circle(base, (color), (radio,radio) ,_r)
            _r -= 1
        return base

class SquareLight(LightSource):
    """Para luces cuadradas que no ocupan toda la pantalla"""
    def __init__(self,lado,color,x,y):
        img = self._crear(lado,color)
        super().__init__(img,x,y)
    
    @staticmethod
    def _crear(lado,color):
        base = Surface((lado,lado),SRCALPHA)
        if len(color) < 4:
            raise ValueError('el color debe ser rgba')
        base.fill(color)
        return base

class GradientSquareLight(LightSource):
    def __init__(self,radio,color):
        img = self._crear(lado,color)
        super().__init__(img)
    
    @staticmethod
    def __crear(lado,color,step=1):
        pass
        
class DayLight:
    """Luz de día, ocupa toda la pantalla"""
    def __init__(self,tamanio): #el tamanio podría ser fijo de 1024
        self.rect = Rect(0,0,tamanio,tamanio) #la posición podría ser variable.
        self.color = 0,0,0,0 #el color podría ser una constante.
        self.estatico = True
        self.nombre = 'sol'
