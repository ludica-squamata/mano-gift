from pygame.sprite import LayeredDirty
from pygame import Rect, draw
from .constantes import Constants as C

class Renderer:
    camara = None
    overlays = None
    use_focus = False

    def __init__(self):
        self.camara = Camara(self)
        self.overlays = LayeredDirty()
        
    def clear(self):
        self.camara.contents.empty()
        self.overlays.empty()
    
    def setBackground(self,bg):
        self.camara.setBackground(bg)

    def addObj(self,obj,layer):
        self.camara.addFgObj(obj,layer)
    
    def delObj(self,obj):
        self.camara.delObj(obj)
    
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
    contents = None # objetos del frente
    x,y,w,h = 0,0,0,0

    def __init__(self,parent):
        self.parent = parent
        self.contents = LayeredDirty()
        self.bgs = LayeredDirty()
        self.w = C.ANCHO
        self.h = C.ALTO
        self.rect = Rect(self.x,self.y,self.w,self.h)
        self.camRect = Rect(-1,-1,self.w,self.h)
    
    def setBackground(self,spr):
        if self.bg == None:
            self.bg = spr
            self.bg_rect = spr.rect.copy()
            self.camRect.topleft = self.bg_rect.topleft
            self.bgs.add(spr)
        else:
            self.bgs.add(spr)
            self.bg_rect.union_ip(spr.rect)
        
    def addFgObj(self,spr,_layer=0):
        if spr not in self.contents:
            self.contents.add(spr,layer=_layer)
    
    def delObj(self,obj):
        if obj in self.contents:
            self.contents.remove(obj)
    
    def setFocus(self,spr):
        self.focus = spr

    def isFocus(self,spr):
        if self.focus != None and hasattr(spr,'nombre'):
            if self.focus.nombre == spr.nombre:
                return True
        return False
    
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
    
    def panear(self, dx, dy):
        self.bg.rect.x += dx
        self.bg.rect.y += dy

        colliderect = self.rect.colliderect

        for spr in self.bgs:
            if spr != self.bg:
                x = self.bg.rect.x + spr.offsetX
                y = self.bg.rect.y + spr.offsetY
                spr.ubicar(x,y)
                if colliderect(spr.rect):
                    spr.dirty = 1
    
        for spr in self.contents:
            if 0 < spr._layer_ < 7:
                x = self.bg.rect.x + spr.mapX
                y = self.bg.rect.y + spr.mapY
                spr.ubicar(x,y)
                if colliderect(spr.rect):
                    spr.dirty = 1
                    if y:
                        self.contents.change_layer(spr, spr._layer_+spr.rect.bottom)

    def update(self, use_focus):
        self.bgs.update()
        self.contents.update()
        if use_focus:
            self.centrar()
            dx, dy = self.detectar_limites()
            focus_dx = self.focus.rect.x - self.focus.mapX - self.bg.rect.x
            focus_dy = self.focus.rect.y - self.focus.mapY - self.bg.rect.y
            if focus_dx or focus_dy:
                self.panear(dx,dy)

    def draw(self, fondo):
        ret = self.bgs.draw(fondo)
        ret += self.contents.draw(fondo)
        #draw.line(fondo,(0,100,255),(self.rect.centerx,0),(self.rect.centerx,self.h))
        #draw.line(fondo,(0,100,255),(0,self.rect.centery),(self.w,self.rect.centery))
        return ret
       