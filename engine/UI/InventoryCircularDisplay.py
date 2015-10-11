from engine.IO.menucircular import CircularMenu, BaseElement
from engine.globs import EngineData as Ed, Constants as Cs
from pygame import font, Surface, SRCALPHA

class InventoryElement(BaseElement):
    active = True
    delta = 0
    def __init__(self,parent,nombre,icono,cascada=None):
        super().__init__(parent,nombre)
        
        if type(icono) is str:
            self.img_uns = self._crear_icono_texto(icono,21,21)
            self.img_sel = self._crear_icono_texto(icono,33,33)
        else:
            self.img_uns = self._crear_icono_image(icono,21,21)
            self.img_sel = self._crear_icono_image(icono,33,33)
            
        self.rect_uns = self.img_uns.get_rect()
        self.rect_sel = self.img_sel.get_rect()
        
        if self.inplace:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns
        if cascada is not None:
            for item in cascada:
                if type(item) is dict:
                    self.cascada.append(InventoryElement(self.parent,item['nombre'],item['icono'],item.get('cascada')))
                else:
                    self.cascada.append(InventoryElement(self.parent,item.nombre,item.image))
        
        
    @staticmethod
    def _crear_icono_texto(icono,w,h):
        image = Surface((w,h),SRCALPHA)
        image.fill((125,125,125,200))
        _rect = image.get_rect()
        
        fuente = font.SysFont('Verdana',15, bold = True)
        render = fuente.render(icono, 1, (0,0,0))
        renderect = render.get_rect(center=_rect.center)
        image.blit(render,renderect)
        return image
    
    @staticmethod
    def _crear_icono_image(icono,w,h):
        image = Surface((w,h),SRCALPHA)
        image.fill((125,125,125,200))
        _rect = image.get_rect()
        iconrect = icono.get_rect(center=_rect.center)
        image.blit(icono,iconrect)
        return image

class InventoryCircularDisplay (CircularMenu):
    radius = 20
    def __init__(self):
        cx,cy = Ed.RENDERER.camara.rect.center
        n,c,i = 'nombre','cascada','icono'
        
        opciones = [
            {n:'Consumibles',c:Ed.HERO.inventario('consumible'),i:'C'},
            {n:'Equipables',c:Ed.HERO.inventario('equipable'),i:'E'}
            ]
            
        cascadas = {'inicial':[]}
        for opt in opciones:
            obj = InventoryElement(self,opt[n],opt[i],opt[c])
            Ed.RENDERER.addOverlay(obj,Cs.CAPA_OVERLAYS_INVENTARIO)
            cascadas['inicial'].append(obj)
            cascadas[obj.nombre] = obj.cascada
        
        super().__init__(cascadas,cx,cy)
    
    def _change_cube_list(self):
        super()._change_cube_list()
        Ed.RENDERER.overlays.remove_sprites_of_layer(Cs.CAPA_OVERLAYS_INVENTARIO)
        for cuadro in self.cubos:
            Ed.RENDERER.addOverlay(cuadro, Cs.CAPA_OVERLAYS_INVENTARIO)
    
    def back(self):       
        if self.cascadaActual == 'inicial':
            Ed.RENDERER.overlays.remove_sprites_of_layer(Cs.CAPA_OVERLAYS_INVENTARIO)
            Ed.DIALOGO = None
            Ed.MODO = 'Aventura'
        else:
            super().back()