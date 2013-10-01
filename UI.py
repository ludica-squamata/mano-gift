from pygame import draw, sprite, font, Surface, Rect, Color
from libs.textrect import render_textrect
from globs import Constants as C, World as W
from base import _giftSprite
from misc import Resources as r

class Colores:
    button_bg_color = Color(100,100,100)
    font_high_color = Color(255,255,255)
    font_none_color = Color(0,0,0)
    bg_cnvs = Color(125,125,125)
    bg_bisel_bg = Color(175,175,175)
    bg_bisel_fg = Color(100,100,100)

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
    
class Dialog (Ventana):
    fuente = None
    posicion = 0,384
    filas = sprite.LayeredDirty()
    
    def __init__(self, texto):
        self.canvas = self.crear_canvas(int(C.ANCHO), int(C.ALTO/5))
        self.fuente = font.SysFont('verdana', 16)
        self.altura_del_texto = self.fuente.get_height()+1
        self.draw_space = Rect((3,3), (self.canvas.get_width()-7, int(self.canvas.get_height())-7))
        
        self.setText(texto)
        
        super().__init__(self.canvas)
        self.ubicar(*self.posicion)
        self.dirty = 1

    def setText(self, texto):
        h = self.altura_del_texto
        if W.onSelect:
            ops = texto.split('\n')
            self.opciones = len(ops)
            for i in range(len(ops)):
                opcion = _opcion(ops[i],self.draw_space.w,(3,(i*22)+1+(i-1)+2))
                self.filas.add(opcion)
            
            self.filas.draw(self.canvas)
            draw.line(self.canvas,self.font_high_color,(3,self.sel*h),(C.ANCHO-7,self.sel*h)) 
        else:
            render = render_textrect(texto,self.fuente,self.draw_space,self.font_none_color,self.bg_cnvs)
            self.canvas.blit(render,self.draw_space)
            
        self.image = self.canvas
    
    def update (self):
        self.dirty = 1
        
class Menu (Ventana):
    botones = []
    cur_btn = 0
    current = ''
    canvas = None
    _onVSel = {}
    
    def __init__(self,titulo,botones):
        self.botones = sprite.LayeredDirty()
        self.botones.empty()
        self.canvas = self.crear_canvas(C.ANCHO-20,C.ALTO-20)
        self.crear_titulo(titulo,self.font_high_color,self.bg_cnvs,C.ANCHO-20)
        self.establecer_botones(botones)
        self._onVSel = {
            "arriba":False,
            "abajo":False,
            "izquierda":False,
            "derecha":False}
        super().__init__(self.canvas)
        self.ubicar(10,10)
        self.dirty = 1
    
    def crear_titulo(self,titulo,fg_color,bg_color,ancho):
        ttl_fuente = font.SysFont('verdana', 16)
        ttl_fuente.set_underline(True)
        ttl_rect = Rect((3,3),(ancho-7,30))
        ttl_txt =  render_textrect(titulo,ttl_fuente,ttl_rect,fg_color,bg_color,1)
        self.canvas.blit(ttl_txt,ttl_rect.topleft)
        
    def establecer_botones(self,botones):
        for btn in botones:
            nombre = btn['boton']
            pos = btn['pos']
            boton = self._crear_boton(nombre,*pos)
            for direccion in ['arriba','abajo','izquierda','derecha']:
                if direccion in btn:
                    boton.direcciones[direccion] = btn[direccion]
            
            self.botones.add(boton)
        
        if len(self.botones) > 0:
            self.cur_btn = 0
            selected = self.botones.get_sprite(self.cur_btn)
            selected.serElegido()
            self.current = selected
            
            
        self.botones.draw(self.canvas)
        
    def _crear_boton(self,texto,x,y):
        rect = Rect((x,y),((C.CUADRO*6)-6,C.CUADRO-6))
        
        cnvs_pre = Surface(((C.CUADRO*6)+6,C.CUADRO+6))
        cnvs_pre.fill(self.bg_cnvs)
        cnvs_sel = cnvs_pre.copy()
        cnvs_uns = cnvs_pre.copy()
        
        fnd_pre = self.crear_inverted_canvas((C.CUADRO*6),C.CUADRO)
        fnd_uns = self.crear_canvas((C.CUADRO*6),C.CUADRO)
        
        for i in range(round(((C.CUADRO*6)+6)/3)):
            #linea punteada horizontal superior
            draw.line(cnvs_sel,self.font_high_color,(i*7,0),((i*7)+5,0),2)
            
            #linea punteada horizontal inferior
            draw.line(cnvs_sel,self.font_high_color,(i*7,C.CUADRO+4),((i*7)+5,C.CUADRO+4),2)
        
        for i in range(round((C.CUADRO+6)/3)):
            #linea punteada vertical derecha
            draw.line(cnvs_sel,self.font_high_color,(0,i*7),(0,(i*7)+5),2)
            
            #linea punteada vertical izquierda
            draw.line(cnvs_sel,self.font_high_color,((C.CUADRO*6)+4,i*7),((C.CUADRO*6)+4,(i*7)+5),2)
        
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
        
        return _boton(texto,cnvs_sel,cnvs_pre,cnvs_uns,rect.topleft)
    
    def DeselectAllButtons(self):
        if self.botones != []:
            for boton in self.botones:
                boton.serDeselegido()
                boton.dirty = 2
            self.botones.draw(self.canvas)
    
    def selectOne(self,direccion):
        self.DeselectAllButtons()
        self.current = self.botones.get_sprite(self.cur_btn)
        if direccion in self.current.direcciones:
            selected = self.current.direcciones[direccion]
        else:
            selected = self.current.nombre

        for i in range(len(self.botones)):
            boton = self.botones.get_sprite(i)
            if boton.nombre == selected:
                boton.serElegido()
                self.mover_cursor(boton)
                break
                    
        self.botones.draw(self.canvas)
    
    def PressOne(self):
        self.current.serPresionado()
        self.botones.draw(self.canvas)
        
    def mover_cursor(self,item):
        if type(item) == _boton:
            for i in range(len(self.botones)):
                spr = self.botones.get_sprite(i)
                if  spr.nombre == item.nombre:
                    self.cur_btn = i
                    self.current = spr
                    break
            W.onVSel = False
                    
        elif type(item) == _item_inv:
            for i in range(len(self.filas)):
                spr = self.filas.get_sprite(i)
                if item.nombre == spr.nombre:
                    self.cur_opt = self.filas.get_sprite(i)
                    self.current = spr#.nombre
                    break
            W.onVSel = True
    
    def _onVSel_(self,direccion):
        return self._onVSel[direccion]
    
    def update (self):
        self.dirty = 1
        if not W.onVSel:
            draw.line(self.image,self.bg_cnvs,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))
            
class Menu_Inventario (Menu):
    cur_opt = 0
    filas = sprite.LayeredDirty()
    descripcion_area = None
    fuente = ''
    altura_del_texto = 0 # altura de los glifos
    draw_space = None
    draw_space_rect = None
    
    def __init__(self,botones):
        self.fuente = font.SysFont('verdana', 16)
        self.altura_del_texto = self.fuente.get_height()+1
        super().__init__('Inventario',botones)
        self.draw_space_rect = Rect((10,44),(self.canvas.get_width()-19,270))
        self.crear_contenido(self.draw_space_rect)
        self.crear_espacio_descriptivo((self.canvas.get_width()-15),53)
        self.dirty = 1
        self.sel = 1
        self._onVSel = {
            "arriba":True,
            "abajo":True,
            "izquierda":False,
            "derecha":False}
        
    def crear_contenido(self,draw_area_rect):
        self.filas.empty()
        self.draw_space = Surface(draw_area_rect.size)
        self.draw_space.fill(self.bg_cnvs)
        self.canvas.blit(self.draw_space,draw_area_rect.topleft)

        for i in range(len(W.HERO.inventario)):
            fila = _item_inv(W.HERO.inventario[i],draw_area_rect.w-6,(3,(i*22)+1+(i-1)))
            
            self.filas.add(fila)
        
        if len(self.filas) > 0:
            h = self.altura_del_texto
            self.opciones = len(self.filas)
            self.elegir_fila(0)
            self.filas.draw(self.draw_space)
            draw.line(self.draw_space,self.font_high_color,(3,(self.sel*h)+1+(self.sel-2)),(draw_area_rect.w-4,(self.sel*h)+1+(self.sel-2)))
        
        self.canvas.blit(self.draw_space,draw_area_rect.topleft)
    
    def crear_espacio_descriptivo(self,ancho,alto):
        marco = self.crear_espacio_titulado(ancho,alto,'Efecto')
        rect = self.canvas.blit(marco,(7,340))
        self.descripcion_area = Rect((0,0),(rect.w-20,rect.h-42))
        
    def elegir_fila(self,j):
        if self.opciones > 0:
            h = self.altura_del_texto
            self.DeselectAllButtons()
            W.onVSel = True
            self.sel += j
            if self.sel < 1: self.sel = 1
            if self.sel > self.opciones: self.sel = self.opciones
            
            draw.line(self.draw_space,self.font_high_color,(3,(self.sel*h)+1+(self.sel-2)),(self.draw_space.get_width()-4,(self.sel*h)+1+(self.sel-2)))
            draw.line(self.draw_space,self.bg_cnvs,(3,((self.sel-j)*h)+1+((self.sel-j)-2)),(self.draw_space.get_width()-4,((self.sel-j)*h)+1+((self.sel-j)-2))) #
            
            self.mover_cursor(self.filas.get_sprite(self.sel-1))
            
            self.canvas.blit(self.draw_space,self.draw_space_rect.topleft)
            
    def confirmar_seleccion (self):
        cant = W.HERO.usar_item(self.current.item)
        if cant <= 0:
            self.opciones -= 1
            if self.opciones <= 0:
                self.current = self
                W.onVSel = False
                draw.line(self.image,self.bg_cnvs,(10,self.sel*22),(self.canvas.get_width()-10,self.sel*22))
        self.dirty = 1
    
    def update (self):
        self.crear_contenido(self.draw_space_rect)
        if self.opciones > 0:
            desc = render_textrect(self.cur_opt.item.efecto_des,
                                   self.fuente,self.descripcion_area,
                                   self.font_high_color,self.bg_cnvs)
            W.onVSel = True
        else:
            W.onVSel = False
            desc = Surface((32,32))
            desc.fill(self.bg_cnvs)
        
        self.canvas.blit(desc,(12,363))
        self.dirty = 1
    
class Inventario_rapido (Menu_Inventario,Ventana):
    posicion = 0,384
    canvas = ''
    sel = 0
    
    def __init__(self):
        self.canvas = self.crear_inverted_canvas(int(C.ANCHO), int(C.ALTO/5))
        self.draw_space_rect = Rect (3,3,int(C.ANCHO)-7,int(C.ALTO/5)-7)
        self.fuente = font.SysFont('verdana', 16)
        self.altura_del_texto = self.fuente.get_height()+1
        self.crear_contenido(self.draw_space_rect)
        Ventana.__init__(self,self.canvas)
        W.MAPA_ACTUAL.dialogs.add(self,layer=C.CAPA_OVERLAYS_DIALOGOS)
        self.rect = Rect((self.posicion, (C.ANCHO, int(C.ALTO/5))))
        self.dirty = 1
        W.onDialog = True
    
    def confirmar_seleccion (self):
        cant = W.HERO.usar_item(self.current.item)        
        if cant <= 0:
            self.opciones -= 1
            if self.opciones <= 0:
                W.MAPA_ACTUAL.endDialog()
        
    def update (self):
        self.crear_contenido(self.draw_space_rect)
        self.dirty = 1
    
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
        self.dirty = 2
    
    def serPresionado (self):
        self.image = self.img_pre
        self.isSelected = True
        self.rect = self.img_pre.get_rect(topleft=self.pos)
    
    def serElegido(self):
        self.image = self.img_sel
        self.isSelected = True
        self.rect = self.img_sel.get_rect(topleft=self.pos)
        
    def serDeselegido(self):
        self.image = self.img_uns
        self.isSelected = False
        self.rect = self.img_sel.get_rect(topleft=self.pos)
    
    def __repr__(self):
        return self.nombre+' _boton DirtySprite'

class _item_inv (Colores,_giftSprite):
    nombre = ''
    item = None
    
    def __init__(self,item,ancho,pos):
        self.item = item
        self.nombre = self.item.nombre.capitalize()
        cant = self.item.cantidad
        imagen = self.construir_fila(ancho,self.nombre,cant)
        super().__init__(imagen)
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1
        
    def construir_fila(self,ancho,nombre,cantidad):
        fuente = font.SysFont('verdana', 16)
        _rect = Rect((-1,-1),((C.CUADRO*6),fuente.get_height()+1))
        img_nmbr = render_textrect(nombre,fuente,_rect,self.font_high_color,self.bg_cnvs,1)
        img_cant = render_textrect('x'+str(cantidad),fuente,_rect,self.font_high_color,self.bg_cnvs,1)
        
        image = Surface((ancho,_rect.h))
        image.fill(self.bg_cnvs)
        image.blit(img_nmbr,(0,0))
        image.blit(img_cant,((ancho-(C.CUADRO*6)),0))
        
        return image
    
    def __repr__(self):
        return self.nombre+' _item_inv DirtySprite'
    
class _opcion (Colores,_giftSprite):
    def __init__(self,texto,ancho,pos):
        fuente = font.SysFont('verdana', 16)
        _rect = Rect((-1,-1),(ancho,fuente.get_height()+1))
        
        image = render_textrect(texto,fuente,_rect,self.font_none_color,self.bg_cnvs)
        super().__init__(image)
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1