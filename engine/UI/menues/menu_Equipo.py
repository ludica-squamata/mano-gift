from .menu_Items import Menu_Items
from pygame import Surface, Rect, font, draw
from pygame.sprite import LayeredDirty
from engine.misc import Resources as r
from engine.libs.textrect import render_textrect
from engine.globs import EngineData as ED
from engine.UI.widgets import _base_fila, _espacio_equipable

class Menu_Equipo(Menu_Items):
    espacios = None
    filas = None
    current = ''
    cur_esp = 0
    cur_itm = 0
    foco = None
    cambio = False
    def __init__(self):
        '''Crea e inicaliza las varibales del menú Equipo.'''
        
        super(Menu_Items,self).__init__('Equipo')
        self.espacios = LayeredDirty() # grupo de espacios equipables.
        self.filas = LayeredDirty() # grupo de items del espacio de selección.
        self.altura_del_texto = self.fuente_MP.get_height()+1 # se utiliza para trazar lineas
        self.foco = 'espacios' # setea el foco por default
        # Crear los espacios equipables.
        # "e_pos" es la posicion del espacio. "t_pos" es la posicion de su titulo.
        # "direcciones" indica a qué espacio se salta cuando se presiona qué tecla de dirección.
        n,e,t,k = 'nom','e_pos','t_pos','direcciones'
        a,b,i,d = 'arriba','abajo','izquierda','derecha' 
        esp = [
            {n:'yelmo',      e:[96,64]  ,t:[93,48]  ,k:{i:'aro 1',d:'cuello'}},
            {n:'aro 1',      e:[32,64]  ,t:[32,48]  ,k:{b:'peto',d:'yelmo'}},
            {n:'aro 2',      e:[224,64] ,t:[224,48] ,k:{b:'faldar',i:'cuello'}},
            {n:'cuello',     e:[160,64] ,t:[157,48] ,k:{i:'yelmo',d:'aro 2'}},
            {n:'peto',       e:[32,128] ,t:[34,112] ,k:{a:'aro 1',b:'guardabrazos',d:'faldar'}},
            {n:'guardabrazos',e:[32,192],t:[7,176]  ,k:{a:'peto',b:'brazales',d:'quijotes'}},
            {n:'brazales',   e:[32,256] ,t:[23,240] ,k:{a:'guardabrazos',b:'capa',d:'grebas'}},
            {n:'faldar',     e:[224,128],t:[222,112],k:{a:'aro 2',b:'quijotes',i:'peto'}},
            {n:'quijotes',   e:[224,192],t:[213,176],k:{a:'faldar',b:'grebas',i:'guardabrazos'}},
            {n:'grebas',     e:[224,256],t:[217,240],k:{a:'quijotes',b:'cinto',i:'brazales'}},
            {n:'mano buena', e:[96,352] ,t:[50,320] ,k:{a:'capa',b:'anillo 1',i:'capa',d:'mano mala'}},
            {n:'mano mala',  e:[160,352],t:[165,320],k:{a:'cinto',b:'anillo 2',i:'mano buena',d:'cinto'}},
            {n:'botas',      e:[224,384],t:[223,368],k:{a:'cinto',b:'anillo 2',i:'anillo 2'}},
            {n:'capa',       e:[32,320] ,t:[32,304] ,k:{a:'brazales',b:'guantes',d:'mano buena'}},
            {n:'cinto',      e:[224,320],t:[224,304],k:{a:'grebas',b:'botas',i:'mano mala',}},
            {n:'guantes',    e:[32,384] ,t:[22,368] ,k:{a:'capa',b:'anillo 1',d:'anillo 1'}},
            {n:'anillo 1',   e:[96,416] ,t:[90,400] ,k:{a:'mano buena',i:'guantes',d:'anillo 2'}},
            {n:'anillo 2',   e:[160,416],t:[154,400],k:{a:'mano mala',i:'anillo 1',d:'botas'}},
        ]
        
        for e in esp:
            item = ED.HERO.equipo[e['nom']]
            cuadro = _espacio_equipable(e['nom'],item,e['direcciones'],*e['e_pos'])
            titulo = self.titular(e['nom'])
            self.canvas.blit(titulo,e['t_pos'])
            self.espacios.add(cuadro)
        
        # seleccionar un espacio por default
        self.cur_esp = 1
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
            "izquierda":lambda dummy: None,
            "derecha":lambda dummy: None,
            "hablar":self.equipar_item}
        
    def titular(self,titulo):
        '''Agrega un titulo descriptivo a cada espacio equipable.
        
        Si el nombre tiene dos partes de texto (por ejemplo 'mano buena'),
        se separa en dos lineas mediante un \\n. Si, en cambio, tras el espacio
        hay un numero (como en 'aro 1') se deja como está.'''
        
        w,h = self.fuente_MP.size(titulo)
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
        render = render_textrect(titulo.title(),self.fuente_MP,rect,self.font_none_color,self.bg_cnvs,just)
        
        return render
    
    def selectOne(self,direccion):
        '''Desplaza la selección al espacio equipable actual, y lo resalta.'''
        
        self.DeselectAll(self.espacios)
        self.draw_space.fill(self.bg_cnvs)
        self.current = self.espacios.get_sprite(self.cur_esp)
        if direccion in self.current.direcciones:
            selected = self.current.direcciones[direccion]
            self.cambio = True
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
        '''Crea el marco donde aparecerán las listas de items que se correspondan
        con el espacio actualmente seleccionado'''
        
        marco = self.crear_espacio_titulado(ancho,alto,'Inventario')
        rect = self.canvas.blit(marco,(266,39))
        self.draw_space_rect = Rect((rect.x+4,rect.y+26),(rect.w-9,rect.h-31))
        self.draw_space = Surface(self.draw_space_rect.size)
        self.draw_space.fill(self.bg_cnvs)
    
    def llenar_espacio_selectivo(self,draw_area_rect):
        '''Llena el espacio selectivo con los items que se correspondan con el espacio
        actualmente seleccionado. Esta función se llama cuando se cambia el espacio.'''
        
        h = self.altura_del_texto
        self.filas.empty()
        espacio = self.espacios.get_sprite(self.cur_esp) # por ejemplo: peto
        for idxItemCant in ED.HERO.inventario('equipable',espacio.nombre):
            i,item,cant = idxItemCant
            fila = _fila(item,188,self.fuente_MP,self.font_high_color,(0,i*h+i))
            self.filas.add(fila)
        
        self.opciones = len(self.filas)
   
    def cambiar_foco(self):
        '''Cambia el foco (las funciones que se utilizarán segun el imput)
        variando entre los espacios equipables y la lista de selección.'''
        
        if self.current.item == None:
            if self.opciones > 0:
                h = self.altura_del_texto
                self.foco = 'items'
                self.opciones = len(self.filas)
                self.elegir_fila()
        else:
            self.desequipar_espacio()
    
    def equipar_item(self):
        '''Cuando un espacio esta seleccionado, y el foco está en la lista de items
        usar esta función traslada el item de la lista al espacio seleccionado.'''
        
        espacio = self.espacios.get_sprite(self.cur_esp)
        item = self.current.item
        if espacio.nombre == item.espacio:
            espacio.ocupar(item)
            ED.HERO.equipar_item(item)
            self.draw_space.fill(self.bg_cnvs)
            self.espacios.draw(self.canvas)
            self.foco = 'espacios'
            self.current = espacio
    
    def desequipar_espacio(self):
        espacio = self.espacios.get_sprite(self.cur_esp)
        item = self.current.item
        espacio.desocupar()
        ED.HERO.desequipar_item(item)
        self.espacios.draw(self.canvas)
    
    def cancelar(self):
        if self.foco == 'espacios':
            return super().cancelar()
        else:
            h = self.altura_del_texto
            self.current.serDeselegido()
            self.foco = 'espacios'
        
    def usar_funcion(self,tecla):
        '''Determina qué grupo de funciones se van a usar según el foco actual.'''
        
        if self.foco == 'espacios':
            funciones = self.funciones_espacios
        elif self.foco == 'items':
            funciones = self.funciones_lista
            
        if tecla in ('arriba','abajo','izquierda','derecha'):
            funciones[tecla](tecla)
        else:
            funciones[tecla]()
    
    def update(self):
        if self.cambio:
            self.llenar_espacio_selectivo(self.draw_space_rect)
            self.cambio = False
        self.filas.update()
        self.filas.draw(self.draw_space)
        self.canvas.blit(self.draw_space,self.draw_space_rect)
        self.dirty = 1

class _fila(_base_fila): # menu_equipo
    def construir_fila(self,bg):
        _rect = Rect((-1,-1),(int(self.ancho//2),self.fuente.get_height()+1))
        img_nmbr = render_textrect(self.nombre,self.fuente,_rect,self.color,bg,1)
        img_cant = render_textrect('x'+str(self.cantidad),self.fuente,_rect,self.color,bg,1)
        image = Surface((self.ancho,_rect.h))
        image.fill(self.bg_cnvs)
        image.blit(img_nmbr,(3,0))
        image.blit(img_cant,(self.ancho//2,0))
        
        return image