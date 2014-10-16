from pygame.sprite import LayeredDirty
from pygame import Rect, draw
from .constantes import Constants as C

class Renderer:
    camara = None
    overlays = None
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
        self.camara.update()
        
        self.Lsu = self.camara.LimSup
        self.Lin = self.camara.LimInf
        self.Liz = self.camara.LimIzq
        self.Lde = self.camara.LimDer
        # self.Lsi = self.camara.LimSupI
        # self.Lsd = self.camara.LimSupD
        # self.Lii = self.camara.LimInfI
        # self.Lid = self.camara.LimInfD
        
        for over in self.overlays:
            if over.active:              
                over.update()
        ret = self.camara.draw(fondo) + self.overlays.draw(fondo)
        
        return ret
    
class Camara:
    bg = None # el fondo
    focus = None # objeto que la camara sigue.
    contents = None # objetos del frente
    x,y,w,h = 0,0,0,0
    LimSup = False
    LimInf = False
    LimDer = False
    LimIzq = False
    #LimSupD = False
    #LimInfD = False
    #LimSupI = False
    #LimInfI = False
    
    def __init__(self):
        self.contents = LayeredDirty()
        self.w = C.ANCHO
        self.h = C.ALTO
        self.rect = Rect(self.x,self.y,self.w,self.h)
    
    def setBackground(self,spr):
        self.bg = spr
        self.contents.add(self.bg)
    
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
        
    def paneolibre(self,dx,dy):
        
        newPosX = self.bg.rect.x + dx
        newPosY = self.bg.rect.y + dy
        
        if newPosX > 0 or newPosX < -(self.bg.rect.w - self.w): dx = 0
        if newPosY > 0 or newPosY < -(self.bg.rect.h - self.h): dy = 0
        
        #esta función sí panea porque mueve el fondo y los sprites.
        self.bg.rect.x += dx
        self.bg.rect.y += dy
        for spr in self.contents:
            if spr != self.bg:
                spr.rect.x += dx
                spr.rect.y += dy
                self.contents.change_layer(spr, spr.rect.bottom)
            spr.dirty = 1
            
    def centrar(self):
        self.focus.rect.center = self.rect.center
        
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
        self.bg.rect.x = newPosX
        
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
        self.bg.rect.y = newPosY
        
        for spr in self.contents:
            if spr != self.bg: #porque bg no tiene mapX,mapY
                if spr != self.focus:#porque al focus ya lo movimos antes
                    x = self.bg.rect.x + spr.mapX
                    y = self.bg.rect.y + spr.mapY
                    spr.ubicar(x,y)
            if spr.tipo != 'mapa':
                self.contents.change_layer(spr, spr.rect.bottom)
            spr.dirty = 1
        
    def update(self):
        self.bg.update()
        self.contents.update()
        self.centrar()
                
    def draw(self,fondo):
        ret = self.contents.draw(fondo)
        draw.line(fondo,(0,100,255),(self.rect.centerx,0),(self.rect.centerx,self.h))
        draw.line(fondo,(0,100,255),(0,self.rect.centery),(self.w,self.rect.centery))
        return ret
    
    