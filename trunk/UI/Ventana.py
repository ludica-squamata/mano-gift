from .Colores import Colores
from base.base import _giftSprite
from pygame import Surface, Rect, font, draw

class Ventana (Colores,_giftSprite):
    canvas = None
    posicion = x,y = 0,0
    tamanio = ancho,alto = 0,0
    sel = 1
    opciones = 0
    
    def __init__(self,image):
        super().__init__(image)

    def crear_canvas(self,ancho,alto):
        canvas = Surface((ancho,alto))
        
        clip = Rect(0,0,ancho, alto)
        canvas.fill(self.bg_bisel_bg,rect=clip)
        
        clip = Rect(3,3,ancho, alto)
        canvas.fill(self.bg_bisel_fg,rect=clip)
        
        clip = Rect(3,3,ancho-7, alto-7)
        canvas.fill(self.bg_cnvs,rect=clip)
        
        return canvas
    
    def crear_inverted_canvas (self,ancho,alto):
        canvas = Surface((ancho, alto))
        
        clip = Rect(0,0,ancho, alto)
        canvas.fill(self.bg_bisel_fg,rect=clip)
        
        clip = Rect(3,3,ancho, alto)
        canvas.fill(self.bg_bisel_bg,rect=clip)
        
        clip = Rect(3,3,ancho-7, alto-7)
        canvas.fill(self.bg_cnvs,rect=clip)
        
        return canvas

    def crear_espacio_titulado(self,ancho,alto,titulo):
        marco = self.crear_inverted_canvas(ancho,alto)
        megacanvas = Surface((marco.get_width(),marco.get_height()+17))
        megacanvas.fill(self.bg_cnvs)
        fuente = font.SysFont('verdana', 14)
        texto = fuente.render(titulo,True,self.font_none_color,self.bg_cnvs)
        megacanvas.blit(marco,(0,17))
        megacanvas.blit(texto,(3,7))
        
        return megacanvas
    
    def elegir_opcion(self,i):
        h = self.altura_del_texto
        self.sel += i
        if self.sel < 1: self.sel = 1
        elif self.sel > self.opciones: self.sel = self.opciones
        
        draw.line(self.image,self.font_high_color,(3,(self.sel*h)+1+(self.sel-2)),(self.draw_space.w-4,(self.sel*h)+1+(self.sel-2)))
        draw.line(self.image,self.bg_cnvs,(3,((self.sel-i)*h)+1+((self.sel-i)-2)),(self.draw_space.w-4,((self.sel-i)*h)+1+((self.sel-i)-2))) #

        return self.sel