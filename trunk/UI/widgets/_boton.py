from base import _giftSprite

class _boton (_giftSprite):
    nombre = ''
    img_uns = None
    img_sel = None
    isSelected = False
    pos = 0,0
    direcciones = {}
    
    def __init__(self,nombre,sel,pre,uns,pos):
        self.direcciones = {}
        self.nombre = nombre
        self.img_sel = sel
        self.img_pre = pre
        self.img_uns = uns
        self.pos = pos
        super().__init__(self.img_uns)
        self.rect = self.img_sel.get_rect(topleft=self.pos)
    
    def serPresionado (self):
        self.image = self.img_pre
        self.isSelected = True
        self.rect = self.img_pre.get_rect(topleft=self.pos)
        self.dirty = 1
    
    def serElegido(self):
        self.image = self.img_sel
        self.isSelected = True
        self.rect = self.img_sel.get_rect(topleft=self.pos)
        self.dirty = 1
        
    def serDeselegido(self):
        self.image = self.img_uns
        self.isSelected = False
        self.rect = self.img_sel.get_rect(topleft=self.pos)
        self.dirty = 1
    
    def __repr__(self):
        return self.nombre+' _boton DirtySprite'