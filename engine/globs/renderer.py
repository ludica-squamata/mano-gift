from pygame.sprite import LayeredUpdates
from pygame import Rect, draw
from .constantes import Constants as C

class Renderer:
    camara = None
    overlays = None
    use_focus = False

    def __init__(self):
        self.camara = Camara(self)
        self.overlays = LayeredUpdates()
        
    def clear(self):
        self.camara.clear()
        self.overlays.empty()
    
    def addOverlay(self,obj,_layer):
        self.overlays.add(obj,layer=_layer)
        
    def delOverlay(self,obj):
        if obj in self.overlays:
            self.overlays.remove(obj)
    
    def update(self, fondo):
        fondo.fill((125, 125, 125))
        self.camara.update(self.use_focus)
        
        for over in self.overlays:
            if over.active:              
                over.update()
        ret = self.camara.draw(fondo)
        ret += self.overlays.draw(fondo)
        return ret
    
class Camara:
    bg = None # el fondo
    bg_rect = None
    focus = None # objeto que la camara sigue.
    visible = None # objetos que se ven (incluye sombras)
    real = None # objetos reales del mundo (no incluye sombras)
    x,y,w,h = 0,0,0,0

    def __init__(self,parent):
        self.parent = parent
        self.visible = LayeredUpdates()
        self.real = LayeredUpdates()
        self.bgs = LayeredUpdates()
        self.w = C.ANCHO
        self.h = C.ALTO
        self.rect = Rect(self.x,self.y,self.w,self.h)
        self.camRect = Rect(-1,-1,self.w,self.h)
    
    def set_background(self,spr):
        if self.bg is None:
            self.bg = spr
            self.bg_rect = Rect((0,0),spr.rect.size)
            self.camRect.topleft = self.bg_rect.topleft
            self.bgs.add(spr)
        else:
            self.bgs.add(spr)
            self.bg_rect.union_ip(spr.rect)
            
    def add_real (self,obj):
        self.real.add(obj)
        if obj not in self.visible:
            self.visible.add(obj,layer = obj.z)
    
    def add_visible (self,obj):
        if obj not in self.visible:
            self.visible.add(obj,layer = obj.z)
            
    def remove_obj(self,obj):
        if obj in self.real:
            self.real.remove(obj)
        if obj in self.visible:
            self.visible.remove(obj)
            
    def set_focus(self,spr):
        self.focus = spr

    def isFocus(self,spr):
        if self.focus is not None and hasattr(spr,'nombre'):
            if self.focus.nombre == spr.nombre:
                return True
        return False
    
    def clear(self):
        self.real.empty()
        self.visible.empty()
        self.bgs.empty()
        self.bg = None
        self.camRect = Rect(-1,-1,self.w,self.h)
    
    def detectar_limites(self):
        from .engine_data import EngineData as ED
        
        newX = self.focus.rect.x - self.focus.mapX
        newY = self.focus.rect.y - self.focus.mapY
        self.camRect.topleft = -newX,-newY
        
        top,bottom,left,right = False,False,False,False
        cam = self.camRect # alias
        #A point along the right or bottom edge is not considered to be inside the rectangle.
        ##hence the -1s
        if self.bg_rect.collidepoint((cam.left,cam.top)):         top,left     = True,True
        if self.bg_rect.collidepoint((cam.right-1,cam.top)):      top,right    = True,True
        if self.bg_rect.collidepoint((cam.left,cam.bottom-1)):    bottom,left  = True,True
        if self.bg_rect.collidepoint((cam.right-1,cam.bottom-1)): bottom,right = True,True
        
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
        
        dx = newX - self.bg.rect.x
        dy = newY - self.bg.rect.y
       
        if not left or not right:   dx = 0 #descomentar para restringir
        if not top or not bottom:   dy = 0 #el movimiento fuera de borde

        return dx,dy
    
    def centrar(self):
        self.focus.rect.center = self.rect.center
    
    def update_sprites_layer(self):
        for spr in self.visible:
            self.visible.change_layer(spr, spr.z)

    def panear(self, dx, dy):
        self.bg.rect.x += dx
        self.bg.rect.y += dy

        for spr in self.bgs:
            if spr != self.bg:
                x = self.bg.rect.x + spr.offsetX
                y = self.bg.rect.y + spr.offsetY
                spr.ubicar(x,y)
            
        for spr in self.real:
            x = self.bg.rect.x + spr.mapX
            y = self.bg.rect.y + spr.mapY
            spr.ubicar(x,y,dy)

    def update(self, use_focus):
        self.bgs.update()
        self.visible.update()
        if use_focus:
            self.centrar()
            dx, dy = self.detectar_limites()
            focus_dx = self.focus.rect.x - self.focus.mapX - self.bg.rect.x
            focus_dy = self.focus.rect.y - self.focus.mapY - self.bg.rect.y
            if dx or dy:
                self.panear(dx,dy)
            else:
                x = self.bg.rect.x + self.focus.mapX
                y = self.bg.rect.y + self.focus.mapY
                self.focus.ubicar(x,y,dy)
            
        self.update_sprites_layer()

    def draw(self, fondo):
        ret = self.bgs.draw(fondo)
        ret += self.visible.draw(fondo)
        #draw.line(fondo,(0,100,255),(self.rect.centerx,0),(self.rect.centerx,self.h))
        #draw.line(fondo,(0,100,255),(0,self.rect.centery),(self.w,self.rect.centery))
        return ret