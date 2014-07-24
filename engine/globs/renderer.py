from pygame.sprite import LayeredDirty
from pygame import Rect, draw
from .constantes import Constants as C

class Renderer:
    camara = None
    overlays = None

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
        #fondo.fill((0,0,0))
        self.camara.update()
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
    
    def __init__(self):
        self.contents = LayeredDirty()
        self.w = C.ANCHO
        self.h = C.ALTO
        self.rect = Rect(self.x,self.y,self.w,self.h)
    
    def setBackground(self,spr):
        self.bg = spr
        self.contents.add(self.bg)
    
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
            if newPosX > 0: #limite 
                self.focus.rect.x -= newPosX
            else:           # entre limites
                self.bg.rect.x = newPosX
        else:               # limite 
            self.bg.rect.x = newPosX+offsetX
            self.focus.rect.x += offsetX
        
        newPosY = self.focus.rect.y - self.focus.mapY 
        offsetY = self.h - newPosY - self.bg.rect.h 
        if offsetY <= 0:
            if newPosY > 0: # limite superior
                self.focus.rect.y -= newPosY
            else:           # entre limites
                self.bg.rect.y = newPosY
        else:               # limite inferior
            self.bg.rect.y = newPosY+offsetY
            self.focus.rect.y += offsetY
        
        for spr in self.contents:
            if spr != self.bg: #porque bg no tiene mapX,mapY
                if spr != self.focus:#porque al focus ya lo movimos antes
                    spr.rect.x = self.bg.rect.x + spr.mapX
                    spr.rect.y = self.bg.rect.y + spr.mapY
                self.contents.change_layer(spr, spr.rect.bottom)
            spr.dirty = 1
    
    def update(self):
        self.bg.update()
        self.contents.update()
        self.centrar()
                
    def draw(self,fondo):
        ret = self.contents.draw(fondo)
        #draw.line(fondo,(0,100,255),(self.rect.centerx,0),(self.rect.centerx,self.h))
        #draw.line(fondo,(0,100,255),(0,self.rect.centery),(self.w,self.rect.centery))
        return ret
    
    