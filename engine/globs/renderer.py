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
    
    def addSld(self,obj):
        self.camara.salidas.append(obj)
    
    def update(self,fondo):
        fondo.fill((125,125,125))
        self.camara.update(self.use_focus)
        
        for over in self.overlays:
            if over.active:              
                over.update()
        ret = self.camara.draw(fondo)
        ret += self.overlays.draw(fondo)
        return ret
    
class Camara:
    bg = None # el fondo
    focus = None # objeto que la camara sigue.
    contents = None # objetos del frente
    x,y,w,h = 0,0,0,0
    
    def __init__(self,parent):
        self.parent = parent
        self.contents = LayeredUpdates()
        self.bgs = LayeredUpdates()
        self.salidas = []
        self.w = C.ANCHO
        self.h = C.ALTO
        self.rect = Rect(self.x,self.y,self.w,self.h)
    
    def setBackground(self,spr):
        if self.bg is None:
            self.bg = spr
        self.bgs.add(spr)
        
    def addFgObj(self,spr,_layer=0):
        if spr not in self.contents:
            self.contents.add(spr,layer=_layer)
    
    def delObj(self,obj):
        if obj in self.contents:
            self.contents.remove(obj)
    
    def setFocus(self,spr):
        self.focus = spr

    def isFocus(self,spr):
        if self.focus is not None and hasattr(spr,'nombre'):
            if self.focus.nombre == spr.nombre:
                return True
        return False
    
    def clear(self):
        self.contents.empty()
        self.bgs.empty()
        self.bg = None
    
    def detectar_limites(self):
        top,bottom,left,right = True,True,True,True
        topleft,topright = True,True
        bottomleft,bottomright = True,True
        _tl,_tr,_bl,_br = True,True,True,True
        
        if not len(self.bgs.get_sprites_at((1,1))):   _tl,topleft  = False,False
        if not len(self.bgs.get_sprites_at((640,1))): _tr,topright = False,False
        if not len(self.bgs.get_sprites_at((1,480))): _bl,bottomleft = False,False
        if not len(self.bgs.get_sprites_at((640,480))): _br,bottomright = False,False
        
        if not _tl and not _tr: top = False       
        if not _bl and not _br: bottom = False
        if not _tl and not _bl: left = False
        if not _tr and not _br: right = False
       
        adys = []
        if not top:         adys.append('sup')
        if not bottom:      adys.append('inf')
        if not left:        adys.append('izq')
        if not right:       adys.append('der')
        if not topleft:     adys.append('supizq')
        if not topright:    adys.append('supder')
        if not bottomleft:  adys.append('infizq')
        if not bottomright: adys.append('infder')

        self.bg.checkear_adyacencias(adys)
        if 'sup' in adys: top = True
        if 'inf' in adys: bottom = True
        if 'izq' in adys: left = True
        if 'der' in adys: right = True
        
        newX = self.focus.rect.x - self.focus.mapX
        newY = self.focus.rect.y - self.focus.mapY
        dx = newX - self.bg.rect.x
        dy = newY - self.bg.rect.y
        
        if not left or not right:
            dx = 0 #descomentar para restringir
        if not top or not bottom:
            dy = 0 #el movimiento fuera de borde

        return dx,dy
    
    def centrar(self):
        self.focus.rect.center = self.rect.center
    
    def panear(self,dx,dy):
        self.bg.rect.x += dx
        self.bg.rect.y += dy

        colliderect = self.rect.colliderect

        for spr in self.bgs:
            if spr != self.bg:
                x = self.bg.rect.x + spr.offsetX
                y = self.bg.rect.y + spr.offsetY
                spr.ubicar(x,y)
                # if colliderect(spr.rect):
                    # spr.dirty = 1
        
        for spr in self.salidas:
            x = self.bg.rect.x + spr.mapX
            y = self.bg.rect.y + spr.mapY
            spr.ubicar(x,y)
            
        for spr in self.contents:
            if 0 < spr._layer_ < 7:
                x = self.bg.rect.x + spr.mapX
                y = self.bg.rect.y + spr.mapY
                spr.ubicar(x,y)
                # if colliderect(spr.rect):
                    # spr.dirty = 1
                if y:
                    self.contents.change_layer(spr, spr._layer_+spr.rect.bottom)

    def update(self,use_focus):
        self.bgs.update()
        self.contents.update()
        if use_focus:
            self.centrar()
            dx, dy = self.detectar_limites()
            focus_dx = self.focus.rect.x - self.focus.mapX - self.bg.rect.x
            focus_dy = self.focus.rect.y - self.focus.mapY - self.bg.rect.y
            if focus_dx or focus_dy:
                self.panear(dx,dy)

    def draw(self,fondo):
        ret = self.bgs.draw(fondo)
        ret += self.contents.draw(fondo)
        #draw.line(fondo,(0,100,255),(self.rect.centerx,0),(self.rect.centerx,self.h))
        #draw.line(fondo,(0,100,255),(0,self.rect.centery),(self.w,self.rect.centery))
        return ret
       