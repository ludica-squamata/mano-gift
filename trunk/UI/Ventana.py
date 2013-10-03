from .Colores import Colores
from base.base import _giftSprite
from pygame import Surface, Rect, font, draw
from libs.textrect import render_textrect

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
    
    def dibujar_lineas_cursor (self,i,img_dest,ancho,cursor,max_opciones):
        h = self.altura_del_texto
        cursor += i
        if cursor < 1: cursor = 1
        elif cursor > max_opciones: cursor = max_opciones
        
        y1 = (cursor*h)+1+(cursor-2)
        y2 = ((cursor-i)*h)+1+((cursor-i)-2)
        
        draw.line(img_dest,self.font_high_color,(3,y1),(ancho,y1))
        draw.line(img_dest,self.bg_cnvs,(3,y2),(ancho,y2))
        
        return cursor

    def crear_titulo(self,titulo,fg_color,bg_color,ancho):
        ttl_fuente = font.SysFont('verdana', 16)
        ttl_fuente.set_underline(True)
        ttl_rect = Rect((3,3),(ancho-7,30))
        ttl_txt =  render_textrect(titulo,ttl_fuente,ttl_rect,fg_color,bg_color,1)
        self.canvas.blit(ttl_txt,ttl_rect.topleft)