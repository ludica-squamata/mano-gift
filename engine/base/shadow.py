from pygame import mask as MASK, PixelArray, Surface, transform
from pygame.sprite import DirtySprite
from .giftSprite import _giftSprite
from engine.globs import EngineData as ED

class _sombra (_giftSprite):
    def __init__(self,imagen,rect,x,y,obj):
        super().__init__(imagen=imagen, x=x,y=y)
        self.deltaRect = rect
        self.rect = self.set_pos(x,y)
        self.tipo = "sombra"
        self.obj = obj

    def set_pos(self,x,y):
        #obtiene la posicion final tomando como base la posicion del
        #sprite y la suya propia
        rect = self.image.get_rect()
        rect.x = x+self.deltaRect.x
        rect.y = y+self.deltaRect.y
        
        return rect
    
    def ubicar(self, x, y):
        '''Coloca al sprite en pantalla'''
        self.rect.x = x+self.deltaRect.x
        self.rect.y = y+self.deltaRect.y
        if self.image != None:
            self.dirty = 1

class _shadowSprite(_giftSprite):
    _sombras = None #list
    _sprSombra = None #sprite
    proyectaSombra = True
    _luces = None #list
   
    def __init__(self, *args,**kwargs):
        self._sombras = [0,0,0,0,0,0,0,0]
        self._luces = [0,1,0,0,1,0,1,0]
        
        super().__init__(*args,**kwargs)

        self.update()
        
    def crear_sombras(self,surface,sombra,img_rect):
            
        #Sombra Noreste
        if sombra == 0:
            img = self._crear_sombra(surface,"NE")
            rect = img.get_rect(topleft=img_rect.topleft)

        #Sombra Este
        elif sombra == 1:
            img = self._crear_sombra(surface,"E")
            rect = img.get_rect()
            rect.centery = img_rect.bottom-6
            rect.left = img_rect.centerx

        #Sombra Sureste
        elif sombra == 2:
            img = self._crear_sombra(surface,"SE")
            rect = img.get_rect()
            rect.top = img_rect.bottom-6
            rect.centerx = img_rect.centerx+img_rect.w//4+4

        #Sombra Sur
        elif sombra == 3:
            img = self._crear_sombra(surface,"S")
            rect = img.get_rect()
            rect.top = img_rect.bottom-6
            rect.left = img_rect.left
        
        #Sombra Suroeste
        elif sombra == 4:
            img = self._crear_sombra(surface,"SO")
            rect = img.get_rect()
            rect.top = img_rect.bottom-6
            rect.centerx = img_rect.centerx-img_rect.w//4-3
        
        #Sombra Oeste
        elif sombra == 5:
            img = self._crear_sombra(surface,"O")
            rect = img.get_rect()
            rect.centery = img_rect.bottom-4
            rect.right = img_rect.centerx
        
        #Sombra Noroeste
        elif sombra == 6:
            img = self._crear_sombra(surface,"NO")
            rect = img.get_rect()
            rect.top = img_rect.top
            rect.right = img_rect.right+2
        
        #Sombra Norte
        elif sombra == 7:
            img = self._crear_sombra(surface,"N")
            rect = img.get_rect(bottomleft = img_rect.bottomleft)
        
        return img,rect

    @staticmethod
    def _crear_sombra(surface,arg=None,mask=None):
        h = surface.get_height()
        w = surface.get_width()
        if mask == None:
            mask = MASK.from_surface(surface)
            
        if arg in ('N','S','E','O'):
            pxarray = PixelArray(Surface((w, h), 0,surface))
        else:
            pxarray = PixelArray(Surface((int(w+h/2), h), 0, surface))
        
        for x in range(w):
            for y in range(h):
                    if arg in ('N','S','E','O'):
                        if mask.get_at((x,y)):
                            pxarray[x,y] = 0,0,0,150
                    else:
                        if mask.get_at((x,y)):
                            pxarray[int(x+(h-y)/2),y] = (0,0,0,150)
        
        if arg == 'N':
            return transform.smoothscale(pxarray.make_surface().convert_alpha(),(w,h//2))
        elif arg =='S':
            return transform.flip(pxarray.make_surface().convert_alpha(),False,True)
        elif arg =='E':
            return transform.rotate(pxarray.make_surface().convert_alpha(),-90)
        elif arg =='O':
            return transform.rotate(pxarray.make_surface().convert_alpha(),90)
        elif arg == 'NO':
            return transform.flip(pxarray.make_surface().convert_alpha(),True,False)
        elif arg == 'SO':
            return transform.flip(pxarray.make_surface().convert_alpha(),True,True)
        elif arg == 'SE':
            return transform.flip(pxarray.make_surface().convert_alpha(),False,True)
        else: #NE
            return pxarray.make_surface().convert_alpha()
        
    def recibir_luz(self, source):
        tolerancia = 10
        luces = self._luces
        if self.proyectaSombra:
            #calcular direccion de origen
            dx = self.centerX - source.centerX
            dy = self.centerY - source.centerY
            
            #marcar direccion como iluminada
            if dx > 0:
                if dy > 0:    luces[0] = True # noreste
                elif dy <0: luces[2] = True # sureste
                else:                  luces[1] = True # este
            elif dx < 0:
                if dy > 0:    luces[6] = True # noroeste
                elif dy < 0: luces[4] = True # suroeste
                else:                  luces[5] = True # oeste
            else:
                if dy > 0:    luces[7] = True # norte
                else:                  luces[3] = True # sur

    def updateSombra(self):
        #generar sombra en direccion contraria a los slots iluminados
        #si cambio la lista,
        #actualizar imagen de sombra y centrar
      
        #para el calculo de sombras ha de usarse la imagen que veria la fuente de luz.
        #ej: si el personaje estuviera en posicion D, la sombra O se hace en base a la imagen R
        # si estuviera en posicion U, se usaria L
      
        #a resolver: que imagen usar para las diagonales

        for i in range(0,7):
            if (self._luces[(i+4) % 7] - self._luces[i]) == 1: #bool
                if self._sombras[i] == 0:
                    
                    img,rect = self.crear_sombras(self.image,i,self.rect)
                    x,y = self.mapX,self.mapY
                    self._sombras[i] = _sombra(img,rect,x,y,self)

                    #ED.RENDERER.addObj(self._sombras[i],self.rect.bottom-10)
                    #sombra = self._sombras[i]
                    #self._sprSombra = sombra
                    #rect = sombra.get_pos(self.rect)
                    #sombra.image.blit(self.image,rect)
                    #self.image = sombra.image
                