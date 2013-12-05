from .Menu import Menu
from pygame import Surface, Rect, font
from pygame.sprite import LayeredDirty
from misc import Resources as r
from base.base import _giftSprite
from libs.textrect import render_textrect

class Menu_Equipo(Menu):
    espacios = None
    
    def __init__(self):
        super().__init__('Equipo',[])
        self.espacios = LayeredDirty()
        e_pos = {
            "yelmo":[96,64],"peto":[32,128], "guardabrazos":[32,192],
            "brazales":[32,256], "faldar":[224,128], "quijotes":[224,192],
            "grebas":[224,256], "mano buena":[96,352],"mano mala":[160,352],
            "botas":[224,384], "capa":[32,320], "cinto":[224,320],
            "cuello":[160,64], "guantes":[32,384], "anillo 1":[96,416],
            "anillo 2":[160,416], "aro 1":[32,64], "aro 2":[224,64]
        }
        t_pos = {
            "yelmo":[93,48],"peto":[34,112], "guardabrazos":[7,176],
            "brazales":[23,240], "faldar":[222,112], "quijotes":[213,176],
            "grebas":[217,240], "mano buena":[50,320],"mano mala":[165,320],
            "botas":[223,368], "capa":[32,304], "cinto":[224,304],
            "cuello":[157,48], "guantes":[22,368], "anillo 1":[90,400],
            "anillo 2":[154,400], "aro 1":[32,48], "aro 2":[224,48]
        }        
        for e in e_pos:
            cuadro = _espacio(e,*e_pos[e])
            titulo = self.titular(e)
            self.canvas.blit(titulo,t_pos[e])
            self.espacios.add(cuadro)
        
        self.espacios.draw(self.canvas)
        self.hombre = r.cargar_imagen('hombre_mimbre.png')
        self.canvas.blit(self.hombre,(96,96))
    
    def titular(self,titulo):
        fuente = font.SysFont('Verdana',12)
        w,h = fuente.size(titulo)
        just = 0
        if ' ' in titulo:
            titulo = titulo.split(' ')
            if not titulo[1].isnumeric():
                titulo = '\n'.join(titulo)
                h *=2
                just = 1
            else:
                titulo = ' '.join(titulo)
        
        rect = Rect(-1,-1,w+5,h+1)
        render = render_textrect(titulo.title(),fuente,rect,self.font_none_color,self.bg_cnvs,just)
        
        return render
        
class _espacio(_giftSprite):
    def __init__(self,nombre,x,y):
        imagen = self.crear()
        super().__init__(imagen)
        self.nombre = nombre
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def crear(self):
        rect = Rect(2,2,28,28)
        base = Surface((32,32))
        base.fill((153,153,153),rect)
        return base