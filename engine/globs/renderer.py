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
        map_at_top = False
        map_at_bottom = False
        map_at_left = False
        map_at_right = False
        map_at_topleft  = False
        map_at_topright = False
        map_at_bottomleft = False
        map_at_bottomright = False
        
        if not len(self.bgs.get_sprites_at((1,1))):   _tl,map_at_topleft  = False,False
        if not len(self.bgs.get_sprites_at((640,1))): _tr,map_at_topright = False,False
        if not len(self.bgs.get_sprites_at((1,480))): _bl,map_at_bottomleft = False,False
        if not len(self.bgs.get_sprites_at((640,480))): _br,map_at_bottomright = False,False
        
        if not _tl and not _tr: map_at_top = False       
        if not _bl and not _br: map_at_bottom = False
        if not _tl and not _bl: map_at_left = False
        if not _tr and not _br: map_at_right = False
       
        adyacent_map_keys = []
        if not map_at_top:         adyacent_map_keys.append('sup')
        if not map_at_bottom:      adyacent_map_keys.append('inf')
        if not map_at_left:        adyacent_map_keys.append('izq')
        if not map_at_right:       adyacent_map_keys.append('der')
        if not map_at_topleft:     adyacent_map_keys.append('supizq')
        if not map_at_topright:    adyacent_map_keys.append('supder')
        if not map_at_bottomleft:  adyacent_map_keys.append('infizq')
        if not map_at_bottomright: adyacent_map_keys.append('infder')

        self.bg.checkear_adyacencias(adyacent_map_keys)
        if 'sup' in adyacent_map_keys: top = True
        if 'inf' in adyacent_map_keys: bottom = True
        if 'izq' in adyacent_map_keys: left = True
        if 'der' in adyacent_map_keys: right = True
        
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