from UI.Ventana import Ventana
from globs import Constants as C
from pygame import Rect, Surface, font, draw
from libs.textrect import render_textrect

class _boton (Ventana):
    nombre = ''
    img_uns = None
    img_sel = None
    isSelected = False
    comando = None
    pos = 0,0
    direcciones = {}
    
    def __init__(self,nombre,ancho_mod,comando,pos):
        self.comando = None
        self.direcciones = {}
        self.nombre = nombre
        sel,pre,uns = self.crear(nombre,ancho_mod)
        self.img_sel = sel
        self.img_pre = pre
        self.img_uns = uns
        self.pos = pos
        super().__init__(self.img_uns)
        self.rect = self.img_sel.get_rect(topleft=self.pos)
        
        self.comando = comando
    
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
    
    def crear(self,texto,ancho_mod):
        ancho = C.CUADRO*ancho_mod
        
        rect = Rect((-1,-1),((ancho)-6,C.CUADRO-6))
        
        cnvs_pre = Surface(((ancho)+6,C.CUADRO+6))
        cnvs_pre.fill(self.bg_cnvs)
        cnvs_sel = cnvs_pre.copy()
        cnvs_uns = cnvs_pre.copy()
        
        fnd_pre = self.crear_inverted_canvas(ancho,C.CUADRO)
        fnd_uns = self.crear_canvas((ancho),C.CUADRO)
        
        for i in range(round(((C.CUADRO*ancho)+6)/3)):
            #linea punteada horizontal superior
            draw.line(cnvs_sel,self.font_high_color,(i*7,0),((i*7)+5,0),2)
            
            #linea punteada horizontal inferior
            draw.line(cnvs_sel,self.font_high_color,(i*7,C.CUADRO+4),((i*7)+5,C.CUADRO+4),2)
        
        for i in range(round((C.CUADRO+6)/3)):
            #linea punteada vertical derecha
            draw.line(cnvs_sel,self.font_high_color,(0,i*7),(0,(i*7)+5),2)
            
            #linea punteada vertical izquierda
            draw.line(cnvs_sel,self.font_high_color,(ancho+4,i*7),(ancho+4,(i*7)+5),2)
        
        cnvs_sel.blit(fnd_uns,(3,3))
        cnvs_uns.blit(fnd_uns,(3,3))
        cnvs_pre.blit(fnd_pre,(3,3))
        
        font_se = font.SysFont('verdana', 16, bold = True)
        font_un = font.SysFont('verdana', 16)
        
        btn_sel = render_textrect(texto,font_se,rect,self.font_high_color,self.bg_cnvs,1)
        btn_uns = render_textrect(texto,font_un,rect,self.font_none_color,self.bg_cnvs,1)        
        
        cnvs_uns.blit(btn_uns,(6,6))
        cnvs_sel.blit(btn_sel,(6,6))
        cnvs_pre.blit(btn_sel,(6,6))
        
        return cnvs_sel,cnvs_pre,cnvs_uns
    
    def __repr__(self):
        return self.nombre+' _boton DirtySprite'