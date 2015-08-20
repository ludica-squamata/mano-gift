from .menu import Menu
from engine.UI.widgets import _base_fila
from engine.globs import EngineData as ED
from engine.libs.textrect import render_textrect
from pygame import sprite, font, Rect, draw, Surface

class Menu_Items (Menu):
    cur_opt = 0
    slots = [0 for i in range(10)]
    filas = sprite.LayeredUpdates()
    descripcion_area = None
    altura_del_texto = 0 # altura de los glifos
    draw_space = None
    draw_space_rect = None
    
    def __init__(self):
        self.altura_del_texto = self.fuente_M.get_height()+1
        super().__init__('Items')
        self.draw_space_rect = Rect((10,44),(self.canvas.get_width()-19,270))
        self.draw_space = Surface(self.draw_space_rect.size)
        self.crear_contenido(self.draw_space_rect)
        self.crear_espacio_descriptivo((self.canvas.get_width()-15),93)
        self.funciones = {
            "arriba":self.elegir_fila,
            "abajo":self.elegir_fila,
            "izquierda":self.indicar_espacio, 
            "derecha":self.indicar_espacio,   
            "hablar":self.confirmar_seleccion}
        
    def crear_contenido(self,draw_area_rect):
        self.actualizar_filas()
        
        if len(self.filas) > 0:
            self.elegir_fila()
    
    def actualizar_filas(self):
        h = self.altura_del_texto
        filas = self.filas.sprites()
        
        for idxItemCant in ED.HERO.inventario():
            i,item,cant = idxItemCant #no estamos usando Cant
            if item.tipo == 'equipable':
                color = self.font_high_color
            else:
                color = self.font_none_color
                
            if not (i <= len(filas)-1): #si el item no está ya representado en una fila
                fila = _fila(item,self.draw_space_rect.w,self.fuente_M,color,(3,i*h+i))
                self.filas.add(fila)
        
        self.opciones = len(self.filas)
        self.filas.update()
        
    def crear_espacio_descriptivo(self,ancho,alto):
        marco = self.crear_espacio_titulado(ancho,alto,'Efecto')
        rect = self.canvas.blit(marco,(7,340))
        self.descripcion_area = Rect((12,363),(rect.w-20,rect.h-42))
        
    def indicar_espacio(self,direccion=None):
        if direccion == 'izquierda': j=-1
        elif direccion =='derecha': j=+1
        else: j = 0
        slots = self.slots
        if self.opciones > 0:
            
            if self.current.slot == "-":
                if j > 0:
                    slot = 0
                    _slot = -1
                elif j < 0:
                    slot = 11
                    _slot = 10
            else:
                slot = self.current.slot
                _slot = self.current.slot-1
                
            if slot + j <= 0:
                self.current.slot = '-'
                self.slots[_slot] = 0
            elif slot + j > 10:
                self.current.slot = '-'
                self.slots[_slot] = 0
            elif j > 0:
                
                while _slot+j <= 9:
                    if self.slots[_slot+j]:
                        j+= 1
                    else:
                        break

                if _slot != -1:  
                    self.slots[_slot] = 0
                _slot += j
                if _slot != 10:
                    self.slots[_slot] = 1
                    slot += j
                    self.current.slot = slot
                else:
                    self.current.slot = '-'

                self.current.hasChangedSlot = True

            elif j < 0:
                while self.slots[_slot+j]:
                    j -= 1
                    
                if _slot != 10: #no me gusta, pero no le encuentro
                    self.slots[_slot] = 0 # otra solución
                _slot += j
                if _slot != -1:
                    self.slots[_slot] = 1
                    slot += j
                    self.current.slot = slot
                else:
                    self.current.slot = '-'
                self.current.hasChangedSlot = True
    
    def elegir_fila(self,direccion=None):
        if direccion == 'arriba': j=-1
        elif direccion =='abajo': j=+1
        else: j = 0
        
        if self.opciones > 0:
##            if hasattr(self.current,'slot'):
##                if self.current.hasChangedSlot:
##                    print('ha cambiado')
##                    self.current.hasChangedSlot = False
##                    self.slots[(self.current.slot-1)] = 1
##                print(self.slots)
            for fila in self.filas:
                fila.serDeselegido()
            self.posicionar_cursor(j)
            self.mover_cursor(self.filas.get_sprite(self.sel))
            self.current.isSelected = True
            
    def confirmar_seleccion (self):
        if self.opciones > 0:
            if ED.HERO.usar_item(self.current.item) <= 0:
                self.filas.remove(self.current)
                self.opciones -= 1
                if self.opciones <= 0:
                    self.current = self

    def update (self):
        self.draw_space.fill(self.bg_cnvs)
        self.actualizar_filas()
        self.filas.draw(self.draw_space)
        self.canvas.blit(self.draw_space,self.draw_space_rect)
        if self.opciones > 0:
            desc = render_textrect(self.cur_opt.item.efecto_des,
                                   self.fuente_M,self.descripcion_area,
                                   self.font_high_color,self.bg_cnvs)
        else:
            desc = Surface(self.descripcion_area.size)
            desc.fill(self.bg_cnvs)
        
        self.canvas.blit(desc,self.descripcion_area.topleft)

class _fila(_base_fila): # menu_item
    
    hasChangedSlot = False
    
    def construir_fila(self,bg):
        _rect = Rect((-1,-1),(int(self.ancho//3),self.fuente.get_height()+1))
        img_nmbr = render_textrect(self.nombre,self.fuente,_rect,self.color,bg,1)
        img_cant = render_textrect('x'+str(self.cantidad),self.fuente,_rect,self.color,bg,1)
        img_slot = render_textrect(str(self.slot),self.fuente,_rect,self.color,bg,1)
        image = Surface((self.ancho,_rect.h))
        image.fill(self.bg_cnvs)
        image.blit(img_nmbr,(3,0))
        image.blit(img_cant,(self.ancho//3+1,0))
        image.blit(img_slot,(self.ancho//3*2+1,0))
        
        return image