from .Menu_Items import Menu_Items
from pygame import Surface, Rect, font, draw
from pygame.sprite import LayeredDirty
from misc import Resources as r
from base.base import _giftSprite
from libs.textrect import render_textrect
from .Colores import Colores as  C
from globs import World as W
from ._item_inv import _item_inv

class Menu_Equipo(Menu_Items):
    espacios = None
    filas = None
    current = ''
    cur_esp = 0
    cur_itm = 0
    foco = None
    
    def __init__(self):
        super(Menu_Items,self).__init__('Equipo',[])
        self.espacios = LayeredDirty()
        self.filas = LayeredDirty()
        self.fuente = font.SysFont('Verdana',16)
        self.altura_del_texto = self.fuente.get_height()+1
        self.foco = 'espacios'
        #crear los espacios equipables.
        esp = {
            'yelmo':{       'e_pos':[96,64],  't_pos':[93,48],  'direcciones':{'izquierda':'aro 1','derecha':'cuello'}},
            'aro 1':{       'e_pos':[32,64],  't_pos':[32,48],  'direcciones':{'abajo':'peto','derecha':'yelmo'}},
            'aro 2':{       'e_pos':[224,64], 't_pos':[224,48], 'direcciones':{'abajo':'faldar','izquierda':'cuello'}},
            'cuello':{      'e_pos':[160,64], 't_pos':[157,48], 'direcciones':{'izquierda':'yelmo','derecha':'aro 2'}},
            'peto':{        'e_pos':[32,128], 't_pos':[34,112], 'direcciones':{'arriba':'aro 1','abajo':'guardabrazos','derecha':'faldar'}},
            'guardabrazos':{'e_pos':[32,192], 't_pos':[7,176],  'direcciones':{'arriba':'peto','abajo':'brazales','derecha':'quijotes'}},
            'brazales':{    'e_pos':[32,256], 't_pos':[23,240], 'direcciones':{'arriba':'guardabrazos','abajo':'capa','derecha':'grebas'}},
            'faldar':{      'e_pos':[224,128],'t_pos':[222,112],'direcciones':{'arriba':'aro 2','abajo':'quijotes','izquierda':'peto'}},
            'quijotes':{    'e_pos':[224,192],'t_pos':[213,176],'direcciones':{'arriba':'faldar','abajo':'grebas','izquierda':'guardabrazos'}},
            'grebas':{      'e_pos':[224,256],'t_pos':[217,240],'direcciones':{'arriba':'quijotes','abajo':'cinto','izquierda':'brazales'}},
            'mano buena':{  'e_pos':[96,352], 't_pos':[50,320], 'direcciones':{'arriba':'capa','abajo':'anillo 1','izquierda':'capa','derecha':'mano mala'}},
            'mano mala':{   'e_pos':[160,352],'t_pos':[165,320],'direcciones':{'arriba':'cinto','abajo':'anillo 2','izquierda':'mano buena','derecha':'cinto'}},
            'botas':{       'e_pos':[224,384],'t_pos':[223,368],'direcciones':{'arriba':'cinto','abajo':'anillo 2','izquierda':'anillo 2'}},
            'capa':{        'e_pos':[32,320], 't_pos':[32,304], 'direcciones':{'arriba':'brazales','abajo':'guantes','derecha':'mano buena'}},
            'cinto':{       'e_pos':[224,320],'t_pos':[224,304],'direcciones':{'arriba':'grebas','abajo':'botas','izquierda':'mano mala',}},
            'guantes':{     'e_pos':[32,384], 't_pos':[22,368], 'direcciones':{'arriba':'capa','abajo':'anillo 1','derecha':'anillo 1'}},
            'anillo 1':{    'e_pos':[96,416], 't_pos':[90,400], 'direcciones':{'arriba':'mano buena','izquierda':'guantes','derecha':'anillo 2'}},
            'anillo 2':{    'e_pos':[160,416],'t_pos':[154,400],'direcciones':{'arriba':'mano mala','izquierda':'anillo 1','derecha':'botas'}},
        }
        
        for e in esp:
            cuadro = _espacio_equipable(e,esp[e]['direcciones'],*esp[e]['e_pos'])
            titulo = self.titular(e)
            self.canvas.blit(titulo,esp[e]['t_pos'])
            self.espacios.add(cuadro)
        
        # seleccionar uno por default
        self.cur_esp = 5
        selected = self.espacios.get_sprite(self.cur_esp)
        selected.serElegido()
        self.current = selected
        
        #dibujar todo
        self.espacios.draw(self.canvas)
        self.hombre = r.cargar_imagen('hombre_mimbre.png')
        self.canvas.blit(self.hombre,(96,96))
        self.crear_espacio_selectivo(188,self.canvas.get_height()-64)
        
        #determinar qué tecla activa qué función.
        self.funciones_espacios = {
            "arriba":self.selectOne,
            "abajo":self.selectOne,
            "izquierda":self.selectOne,
            "derecha":self.selectOne,
            "hablar":self.cambiar_foco}
        
        self.funciones_lista = {
            "arriba":self.elegir_fila,
            "abajo":self.elegir_fila,
            "izquierda":lambda dummy: False,
            "derecha":lambda dummy: False,
            "hablar":lambda: False}
        
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
    
    def selectOne(self,direccion):
        self.DeselectAll(self.espacios)
        self.draw_space.fill(self.bg_cnvs)
        self.current = self.espacios.get_sprite(self.cur_esp)
        if direccion in self.current.direcciones:
            selected = self.current.direcciones[direccion]
        else:
            selected = self.current.nombre

        for i in range(len(self.espacios)):
            espacio = self.espacios.get_sprite(i)
            if espacio.nombre == selected:
                espacio.serElegido()
                self.current = espacio
                self.cur_esp = i
                break
                    
        self.espacios.draw(self.canvas)
    
    def crear_espacio_selectivo(self,ancho,alto):
        marco = self.crear_espacio_titulado(ancho,alto,'Inventario')
        rect = self.canvas.blit(marco,(266,39))
        self.draw_space_rect = Rect((rect.x+4,rect.y+26),(rect.w-9,rect.h-31))
        self.draw_space = Surface(self.draw_space_rect.size)
        self.draw_space.fill(C.bg_cnvs)
        self.opciones = len(self.filas)
        self.llenar_espacio_selectivo(self.draw_space_rect)    
        self.canvas.blit(self.draw_space,self.draw_space_rect.topleft)
    
    def llenar_espacio_selectivo(self,draw_area_rect):
        i = -1
        self.filas.empty()
        for item in W.HERO.inventario:
            if item.esEquipable and item.esEquipable == self.current.nombre:
                i += 1
                fila = _item_inv(item,188,(0,(i*22)+1+(i-1)))
                self.filas.add(fila)
                
        self.opciones = len(self.filas)
        self.filas.draw(self.draw_space)
        self.canvas.blit(self.draw_space,self.draw_space_rect.topleft)
        self.dirty = 1
    
    def cambiar_foco(self):
        if self.foco == 'espacios':
            self.foco = 'items'
            h = self.altura_del_texto
            draw.line(self.draw_space,self.font_high_color,(3,(self.sel*h)),(self.draw_space_rect.w-4,(self.sel*h)))

        elif self.foco == 'items':
            self.foco = 'espacios'

        return False
    
    def usar_funcion(self,tecla):
        if self.foco == 'espacios':
            funciones = self.funciones_espacios
        elif self.foco == 'items':
            funciones = self.funciones_lista
            
        if tecla in ('arriba','abajo','izquierda','derecha'):
            return funciones[tecla](tecla)
        else:
            return funciones[tecla]()
    
    def update(self):
        self.dirty = 1
        self.llenar_espacio_selectivo(self.draw_space_rect)
        
class _espacio_equipable (_giftSprite):
    isSelected = False
    direcciones = {}
    
    def __init__(self,nombre,direcciones,x,y):
        self.img_uns = self.crear(False)
        self.img_sel = self.crear(True)
        self.direcciones = {}
        self.direcciones.update(direcciones)
        super().__init__(self.img_uns)
        self.nombre = nombre
        self.rect = self.image.get_rect(topleft = (x,y))
        self.dirty = 1
    
    def crear(self,seleccionar):
        macro = Rect(0,0,36,36)
        img = Surface(macro.size)
        img.fill(C.bg_cnvs)
        
        rect = Rect(2,2,28,28)
        base = Surface((32,32))
        base.fill((153,153,153),rect)
        
        img.blit(base,(2,2))
        
        if seleccionar:
            sel = img.copy()
            w,h = sel.get_size()
            for i in range(round(38/3)):
                #linea punteada horizontal superior
                draw.line(sel,C.font_high_color,(i*7,0),((i*7)+5,0),2)
                
                #linea punteada horizontal inferior
                draw.line(sel,C.font_high_color,(i*7,h-2),((i*7)+5,h-2),2)
            
            for i in range(round(38/3)):
                #linea punteada vertical derecha
                draw.line(sel,C.font_high_color,(w-2,i*7),(w-2,(i*7)+5),2)
                
                #linea punteada vertical izquierda
                draw.line(sel,C.font_high_color,(0,i*7),(0,(i*7)+5),2)
            return sel
        
        return img
    
    def serElegido(self):
        self.image = self.img_sel
        self.isSelected = True
        self.dirty = 1
    
    def serDeselegido(self):
        self.image = self.img_uns
        self.isSelected = False
        self.dirty = 1