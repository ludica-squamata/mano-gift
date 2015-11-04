from pygame.sprite import LayeredUpdates
from .constantes import Constants as C
from pygame import Rect, draw

class Camara:
    bg = None # el fondo
    bg_rect = None
    focus = None # objeto que la camara sigue.
    x,y = 0,0
    w,h = C.ANCHO,C.ALTO
    visible = LayeredUpdates() # objetos que se ven (incluye sombras)
    real = LayeredUpdates() # objetos reales del mundo (no incluye sombras)
    bgs = LayeredUpdates()
    rect = Rect(x,y,w,h)
    camRect = Rect(-1,-1,w,h)
    
    @classmethod
    def set_background(cls,spr):
        if cls.bg is None:
            cls.bg = spr
            cls.bg_rect = Rect((0,0),spr.rect.size)
            cls.camRect.topleft = cls.bg_rect.topleft
            cls.bgs.add(spr)
        else:
            cls.bgs.add(spr)
            cls.bg_rect.union_ip(spr.rect)
    
    @classmethod        
    def add_real (cls,obj):
        cls.real.add(obj)
        if obj not in cls.visible:
            cls.visible.add(obj,layer = obj.z)
    
    @classmethod
    def add_visible (cls,obj):
        if obj not in cls.visible:
            cls.visible.add(obj,layer = obj.z)
    
    @classmethod
    def remove_obj(cls,obj):
        if obj in cls.real:
            cls.real.remove(obj)
        if obj in cls.visible:
            cls.visible.remove(obj)
    
    @classmethod
    def set_focus(cls,spr):
        cls.focus = spr
    
    @classmethod
    def isFocus(cls,spr):
        if cls.focus is not None and hasattr(spr,'nombre'):
            if cls.focus.nombre == spr.nombre:
                return True
        return False
    
    @classmethod
    def clear(cls):
        cls.real.empty()
        cls.visible.empty()
        cls.bgs.empty()
        cls.bg = None
        cls.camRect = Rect(-1,-1,cls.w,cls.h)
    
    @classmethod
    def detectar_limites(cls):
        from .engine_data import EngineData as ED
        
        newX = cls.focus.rect.x - cls.focus.mapX
        newY = cls.focus.rect.y - cls.focus.mapY
        cls.camRect.topleft = -newX,-newY
        
        top,bottom,left,right = False,False,False,False
        cam = cls.camRect # alias
        #A point along the right or bottom edge is not considered to be inside the rectangle.
        ##hence the -1s
        if cls.bg_rect.collidepoint((cam.left,cam.top)):         top,left     = True,True
        if cls.bg_rect.collidepoint((cam.right-1,cam.top)):      top,right    = True,True
        if cls.bg_rect.collidepoint((cam.left,cam.bottom-1)):    bottom,left  = True,True
        if cls.bg_rect.collidepoint((cam.right-1,cam.bottom-1)): bottom,right = True,True
        
        d = ''
        if not top:    d+='sup'
        if not bottom: d+='inf'
        if not left:   d+='izq'
        if not right:  d+='der'
        
        if ED.checkear_adyacencias(d):
            if 'sup' in d: top = True
            if 'inf' in d: bottom = True
            if 'izq' in d: left = True
            if 'der' in d: right = True
        
        dx = newX - cls.bg.rect.x
        dy = newY - cls.bg.rect.y
       
        if not left or not right:   dx = 0 #descomentar para restringir
        if not top or not bottom:   dy = 0 #el movimiento fuera de borde

        return dx,dy
    
    @classmethod
    def centrar(cls):
        cls.focus.rect.center = cls.rect.center
    
    @classmethod
    def update_sprites_layer(cls):
        for spr in cls.visible:
            cls.visible.change_layer(spr, spr.z)
    
    @classmethod
    def panear(cls, dx, dy):
        cls.bg.rect.x += dx
        cls.bg.rect.y += dy

        for spr in cls.bgs:
            if spr != cls.bg:
                x = cls.bg.rect.x + spr.offsetX
                y = cls.bg.rect.y + spr.offsetY
                spr.ubicar(x,y)
            
        for spr in cls.real:
            x = cls.bg.rect.x + spr.mapX
            y = cls.bg.rect.y + spr.mapY
            spr.ubicar(x,y,dy)
    
    @classmethod
    def update(cls, use_focus):
        cls.bgs.update()
        cls.visible.update()
        if use_focus:
            cls.centrar()
            dx, dy = cls.detectar_limites()
            if dx or dy:
                cls.panear(dx,dy)
            else:
                x = cls.bg.rect.x + cls.focus.mapX
                y = cls.bg.rect.y + cls.focus.mapY
                cls.focus.ubicar(x,y,dy)
            
        cls.update_sprites_layer()
    
    @classmethod
    def draw(cls, fondo):
        ret = cls.bgs.draw(fondo)
        ret += cls.visible.draw(fondo)
        #draw.line(fondo,(0,100,255),(cls.rect.centerx,0),(cls.rect.centerx,cls.h))
        #draw.line(fondo,(0,100,255),(0,cls.rect.centery),(cls.w,cls.rect.centery))
        return ret


class Renderer:
    use_focus = False
    camara = Camara()
    overlays = LayeredUpdates()
    
    @classmethod
    def clear(cls):
        cls.camara.clear()
        cls.overlays.empty()
    
    @classmethod
    def addOverlay(cls,obj,_layer):
        cls.overlays.add(obj,layer=_layer)
        
    @classmethod
    def delOverlay(cls,obj):
        if obj in cls.overlays:
            cls.overlays.remove(obj)
    
    @classmethod
    def update(cls, fondo):
        fondo.fill((125, 125, 125))
        cls.camara.update(cls.use_focus)
        
        for over in cls.overlays:
            if over.active:              
                over.update()
        ret = cls.camara.draw(fondo)
        ret += cls.overlays.draw(fondo)
        return ret
