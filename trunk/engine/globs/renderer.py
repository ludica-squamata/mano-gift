from pygame.sprite import LayeredDirty
from pygame import Rect, draw
from .constantes import Constants as C

class Renderer:
    camara = None
    overlays = None
    use_focus = True
    Lsu = None
    Lin = None
    Lde = None
    Liz = None

    def __init__(self):
        self.camara = Camara()
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

    def update(self,fondo):
        fondo.fill((125,125,125))
        self.camara.update(self.use_focus)
        
        self.Lsu = self.camara.LimSup
        self.Lin = self.camara.LimInf
        self.Liz = self.camara.LimIzq
        self.Lde = self.camara.LimDer
        
        for over in self.overlays:
            if over.active:              
                over.update()
        ret = self.camara.draw(fondo) + self.overlays.draw(fondo)
        
        return ret
    
class Camara:
    bg = None # el fondo
    bg_rect = None
    focus = None # objeto que la camara sigue.
    contents = None # objetos del frente
    x,y,w,h = 0,0,0,0
    LimSup = False
    LimInf = False
    LimDer = False
    LimIzq = False
    
    def __init__(self):
        self.contents = LayeredDirty()
        self.bgs = LayeredDirty()
        self.w = C.ANCHO
        self.h = C.ALTO
        self.rect = Rect(self.x,self.y,self.w,self.h)
    
    def setBackground(self,spr):
        if self.bg == None:
            self.bg = spr
            self.bg_rect = spr.rect.copy()
            self.bgs.add(spr)
        else:
            self.bgs.add(spr)
            self.bg_rect.union_ip(spr.rect)
    
    def setAdyBg(self,bg):
        self.contents.add(bg,layer=0)
    
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
    
    def mover (self,dx,dy):
        self.rect.move_ip(dx,dy)
        print(self.rect)
    
    def paneolibre(self,dx,dy):
        
        newPosX = self.bg.rect.x + dx
        newPosY = self.bg.rect.y + dy
        
        #if newPosX > 0 or newPosX < -(self.bg.rect.w - self.w): dx = 0
        #if newPosY > 0 or newPosY < -(self.bg.rect.h - self.h): dy = 0
        
        #esta función sí panea porque mueve el fondo y los sprites.
        self.bg.rect.x += dx
        self.bg.rect.y += dy
        for spr in self.bgs:
            if spr != self.bg:
                x = self.bg.rect.x + spr.offsetX
                y = self.bg.rect.y + spr.offsetY
                spr.ubicar(x,y)
            spr.dirty = 1
            
        for spr in self.contents:
            x = self.bg.rect.x + spr.mapX
            y = self.bg.rect.y + spr.mapY
            spr.ubicar(x,y)
            self.contents.change_layer(spr, spr.rect.bottom)
            spr.dirty = 1
            
    def detectar_limites(self):
        newPosX = self.focus.rect.x - self.focus.mapX
        offsetX = self.w - newPosX - self.bg.rect.w
        if offsetX <= 0:
            if newPosX > 0: # limite izquierdo
                #self.focus.rect.x -= newPosX
                self.LimIzq = True
            else:           # entre limites
                #self.bg.rect.x = newPosX
                self.LimDer = False
                self.LimIzq = False
        else:               # limite derecho
            #self.bg.rect.x = newPosX+offsetX
            #self.focus.rect.x += offsetX
            if not self.LimDer:
                self.LimDer = True
        
        newPosY = self.focus.rect.y - self.focus.mapY 
        offsetY = self.h - newPosY - self.bg.rect.h 
        if offsetY <= 0:
            if newPosY > 0: # limite superior
                #self.focus.rect.y -= newPosY
                if not self.LimSup:
                    self.LimSup = True
            else:           # entre limites
                #self.bg.rect.y = newPosY
                self.LimSup = False
                self.LimInf = False
        else:               # limite inferior
            #self.bg.rect.y = newPosY+offsetY
            #self.focus.rect.y += offsetY
            if not self.LimInf:
                self.LimInf = True
        
        return newPosX,newPosY
    
    def centrar(self):
        self.focus.rect.center = self.rect.center
    
    def panear(self,dx,dy):
        _rect = Rect((-dx,-dy),self.rect.size)
        #la idea es que si el rect del mapa contiene al de la camara
        if self.bg_rect.contains(_rect): 
            pass #entonces la camara se mueve (panea)
        else: # pero si no la contiene
            pass # no deberia moverse (para no salirse de los bordes)
        
        self.bg.rect.x = dx
        self.bg.rect.y = dy
        for spr in self.bgs:
            if spr != self.bg:
                x = self.bg.rect.x + spr.offsetX
                y = self.bg.rect.y + spr.offsetY
                spr.ubicar(x,y)
            spr.dirty = 1
        
        for spr in self.contents:
            if spr != self.focus:#porque al focus ya lo movimos antes
                x = self.bg.rect.x + spr.mapX
                y = self.bg.rect.y + spr.mapY
                spr.ubicar(x,y)
            self.contents.change_layer(spr, spr.rect.bottom)
            spr.dirty = 1
        
    def update(self,use_focus):
        self.bgs.update()
        self.contents.update()
        if use_focus:
            self.centrar()
            dx,dy = self.detectar_limites()
            self.panear(dx,dy)
            
                
    def draw(self,fondo):
        ret = ret = self.bgs.draw (fondo) + self.contents.draw(fondo)
        draw.line(fondo,(0,100,255),(self.rect.centerx,0),(self.rect.centerx,self.h))
        draw.line(fondo,(0,100,255),(0,self.rect.centery),(self.w,self.rect.centery))
        return ret
    
    