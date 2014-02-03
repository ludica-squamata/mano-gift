from .Menu import Menu
from UI.Colores import Colores as C
from UI._item_inv import _item_inv
from globs import World as W
from libs.textrect import render_textrect
from pygame import sprite, font, Rect, draw, Surface

class Menu_Items (Menu):
    cur_opt = 0
    filas = sprite.LayeredDirty()
    descripcion_area = None
    fuente = ''
    altura_del_texto = 0 # altura de los glifos
    draw_space = None
    draw_space_rect = None
    
    def __init__(self):
        self.fuente = font.SysFont('verdana', 16)
        self.altura_del_texto = self.fuente.get_height()+1
        super().__init__('Items')
        self.draw_space_rect = Rect((10,44),(self.canvas.get_width()-19,270))
        self.crear_contenido(self.draw_space_rect)
        self.crear_espacio_descriptivo((self.canvas.get_width()-15),93)
        self.dirty = 1
        self.sel = 1
        self.funciones = {
            "arriba":self.elegir_fila,
            "abajo":self.elegir_fila,
            "izquierda":lambda dummy: None, # no hay ninguna funcionalidad
            "derecha":lambda dummy: None,   # aún para estas teclas.
            "hablar":self.confirmar_seleccion}
        
    def crear_contenido(self,draw_area_rect):
        self.filas.empty()
        h = self.altura_del_texto
        self.draw_space = Surface(draw_area_rect.size)
        self.draw_space.fill(self.bg_cnvs)
        self.canvas.blit(self.draw_space,draw_area_rect.topleft)

        for i in range(len(W.HERO.inventario)):
            item = W.HERO.inventario[i]
            if item.esEquipable: color = C.font_low_color
            else: color = C.font_high_color
            fila = _item_inv(item,draw_area_rect.w-6,(3,i*h+i),self.fuente,color)
            
            self.filas.add(fila)
        
        if len(self.filas) > 0:
            self.opciones = len(self.filas)
            self.elegir_fila(0)
            self.filas.draw(self.draw_space)
            draw.line(self.draw_space,self.font_high_color,(3,(self.sel*h)+1+(self.sel-2)),(draw_area_rect.w-4,(self.sel*h)+1+(self.sel-2)))
        
        self.canvas.blit(self.draw_space,draw_area_rect.topleft)
    
    def crear_espacio_descriptivo(self,ancho,alto):
        marco = self.crear_espacio_titulado(ancho,alto,'Efecto')
        rect = self.canvas.blit(marco,(7,340))
        self.descripcion_area = Rect((0,0),(rect.w-20,rect.h-42))
        
    def elegir_fila(self,direccion):
        if direccion == 'arriba': j=-1
        elif direccion =='abajo': j=+1
        else: j = 0
        if self.opciones > 0:
            self.DeselectAll(self.botones)
            self.sel = self.dibujar_lineas_cursor(j,self.draw_space,
                                       self.draw_space.get_width()-4,
                                       self.sel,self.opciones)

            self.mover_cursor(self.filas.get_sprite(self.sel-1))
            
            self.canvas.blit(self.draw_space,self.draw_space_rect.topleft)
            
    def confirmar_seleccion (self):
        h = self.altura_del_texto
        if self.opciones > 0:
            cant = W.HERO.usar_item(self.current.item)
            if cant <= 0:
                self.opciones -= 1
                if self.opciones <= 0:
                    self.current = self
                    draw.line(self.image,self.bg_cnvs,(10,self.sel*h),(self.canvas.get_width()-10,self.sel*h))
            self.dirty = 1
    
    def update (self):
        self.crear_contenido(self.draw_space_rect)
        if self.opciones > 0:
            desc = render_textrect(self.cur_opt.item.efecto_des,
                                   self.fuente,self.descripcion_area,
                                   self.font_high_color,self.bg_cnvs)
        else:
            desc = Surface(self.descripcion_area.size)
            desc.fill(self.bg_cnvs)
        
        self.canvas.blit(desc,(12,363))
        self.dirty = 1