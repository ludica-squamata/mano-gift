from pygame import time, Surface, draw, PixelArray, SRCALPHA
from engine.base import _giftSprite
from engine.misc import Resources as r
from engine.globs.eventDispatcher import GiftEvent

class _clock:
    _h = 0
    _m = 0
    _s = 0
    day_flag = False
    hour_flag = False
    def __init__(self,h=0,m=0,s=0):
        self._h = h
        self._m = m
        self._s = s
        self.day_flag = False
        self.hour_flag = False
    
    def __repr__(self):
        return ':'.join([str(self._h),str(self._m).rjust(2,'0')])
    
    @property
    def h(self):
        return self._h
    @h.setter
    def h(self,value):
        self.hour_flag = True
        if value > 23:
            self._h = 0
            self.day_flag = True
        else:
            self._h = value
    @h.deleter
    def h(self):
        self._h = 0
    
    @property
    def m(self):
        return self._m
    @m.setter
    def m(self,value):
        if value > 59:
            self.h += 1
            value = 0
        self._m = value
    @m.deleter
    def m(self):
        self._m = 0

    @property
    def s(self):
        return self._s
    @s.setter
    def s(self,value):
        if value > 59:
            self._m += 1
            value = 0
        self._s = value
    @s.deleter
    def s(self):
        self._s = 0
        
    def timestamp(self,h=0,m=0,s=0):
        if h==0 and m==0 and s==0:
            return timestamp(self._h,self._m,self._s)
        else:
            return timestamp(h,m,s)
        
    def update(self,dm=1):
        self.day_flag = False
        self.hour_flag = False
        self.m += dm

class timestamp:
    def __init__(self,h=0,m=0,s=0):
        self._h = h
        self._m = m
        self._s = s
    
    #read-only properties
    @property
    def h(self):
        """Read-only hour value"""
        return self._h
    @property
    def m(self):
        """Read-only minute value"""
        return self._m
    @property
    def s(self):
        """Read-only second value"""
        return self._s  
    
    #rich comparison methods
    def __lt__(self, other): 
        if hasattr(other,'_h') and hasattr(other,'_m') and hasattr(other,'_s'):
            if self._h < other._h: 
                return True
                
            if self._m < other._m: 
                return True
            
            if self._s < other._s:
                return True
            
        return False
    def __le__(self, other): 
        if hasattr(other,'_h') and hasattr(other,'_m') and hasattr(other,'_s'):
            if self._h <= other._h:
                if self._m <= other._m:
                    if self._s <= other._s:
                        return True
        return False
    def __eq__(self, other): 
        if hasattr(other,'_h') and hasattr(other,'_m') and hasattr(other,'_s'):
            return self._h == other._h and self._m == other._m and self._s == other._s
        return False
    def __ne__(self, other): 
        if hasattr(other,'_h') and hasattr(other,'_m') and hasattr(other,'_s'):
            if self._h != other._h:
                if self._m != other._m :
                    if self._s != other._s:
                        return True
            return False
        return True
    def __gt__(self, other): 
        if hasattr(other,'_h') and hasattr(other,'_m') and hasattr(other,'_s'):
            if self._h > other._h:
                return True
            if self._m > other._m:
                return True
            if self._s > other._s:
                return True
        return False
    def __ge__(self, other):
        if hasattr(other,'_h') and hasattr(other,'_m') and hasattr(other,'_s'):
            if self._h >= other._h:
                if self._m >= other._m:
                    if self._s >= other._s:
                        return True
        return False

        if hasattr(other,'_time'):
            return self._time >= other._time
        else:
            return False
    
    #operations, add, sub, mul
    @staticmethod
    def _convert(s):
        m = 0
        h = 0
        if s > 59:
            m += s//60
            s = s%60
        if m > 59:
            h += m//60
            m = m%60
            
        return timestamp(h,m,s)
    
    def __add__(self,other):
        s = (self._h*3600+self._m*60+self._s)+(other._h*3600+other._m*60+other._s)
        return self._convert(s)

    def __sub__(self,other):
        s = (self._h*3600+self._m*60+self._s)-(other._h*3600+other._m*60+other._s)
        return self._convert(s)
    
    def __mul__(self,factor):
        if isinstance(factor,timestamp):
            raise NotImplementedError('Solo puede multiplicarse por un factor')
        s = (self._h*3600+self._m*60+self._s)*factor
        return self._convert(s)
    
    def __repr__(self):
        return ':'.join([str(self._h),str(self._m).rjust(2,'0')])
    
class Noche(_giftSprite):
    def __init__(self,size):
        #############################
        if 1: #cambiar a 0 para prueba de luces
            img = Surface(size)
            img.fill((0,0,125))
            img.set_alpha(0)
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
    dia,_frames = 0,0
    clock = _clock()
    esNoche = False
    noche = None
    
    @classmethod
    def setear_momento(cls,dia,hora,mins=0):
        cls.dia = dia
        cls.clock.h = hora
        cls.clock.m = mins
        
    @classmethod
    def contar_tiempo (cls):
        from engine.globs.engine_data import EngineData as ED

        cls._frames += 1
        if cls._frames == 60:
            cls.clock.update()
            cls._frames = 0
            if cls.clock.day_flag:
                cls.dia += 1
            if cls.clock.hour_flag:
                ED.EVENTS.trigger(GiftEvent('hora', 'Tiempo', {"hora": cls.clock.h}))
    
    @classmethod
    def oscurecer(cls,limite):
        alpha = cls.noche.image.get_alpha()
        if alpha < limite:
            cls.noche.image.set_alpha(alpha+1)
        else:
            return True

    @classmethod
    def aclarar(cls):
        alpha = cls.noche.image.get_alpha()
        cls.noche.image.set_alpha(alpha-1)
            
    @classmethod
    def crear_noche(cls,tamanio):
        cls.noche = Noche(tamanio)