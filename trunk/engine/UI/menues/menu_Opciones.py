from pygame.sprite import LayeredDirty
from pygame.key import name as key_name
from pygame import Rect,font
from engine.UI.widgets import _boton, _opcion
from engine.globs.constantes import Constants as K
from engine.misc.config import Config as C
from engine.libs.textrect import render_textrect
from .menu_Pausa import Menu_Pausa
from .menu import Menu


class Menu_Opciones (Menu_Pausa,Menu):
    def __init__(self):
        Menu.__init__(self,'Opciones')
        self.data = C.cargar()

        self.botones = LayeredDirty()
        self.espacios = LayeredDirty()
        self.establecer_botones(self.crear_botones_config(),5)
        self.establecer_botones(self.crear_botones_teclas(),4)
        self.crear_espacios_config()
        self.funciones = {
            "arriba":self.selectOne,
            "abajo":self.selectOne,
            "izquierda":self.selectOne,
            "derecha":self.selectOne,
            "hablar":self.ejecutar_comando}
        
        self.keyup = {
            "hablar":self.ReleaseButton}
        
    def crear_botones_config(self):
        m,k,p,c = 'nombre','direcciones','pos','comando'
        a,b,i,d = 'arriba','abajo','izquierda','derecha'
        dy, f = 64,38 # constantes numéricas de posicion # f = fila
        cmd1 = self.cambiarBooleano
        cmd2 = self.PressButton
        botones = [
            {m:"Mostrar Intro", c:cmd1,p:[6,f*0+dy],k:{b:"Recordar Menus",a:"Salir"}},
            {m:"Recordar Menus",c:cmd1,p:[6,f*1+dy],k:{b:"Resolución",a:"Mostrar Intro"}},
            {m:"Resolución",    c:cmd2,p:[6,f*2+dy],k:{b:"Arriba",a:"Recordar Menus"}}
        ]
        
        return botones
    
    def crear_botones_teclas (self):
        #abreviaturas para hacer más legible el código
        m,k,p,c = 'nombre','direcciones','pos','comando'
        a,b,i,d = 'arriba','abajo','izquierda','derecha'
        x1,x2 = 6,226
        dy, f = 185,38 # constantes numéricas de posicion # f = fila
        cmd = self.setTecla
        botones = [
            # primera columna
            {m:"Arriba",    c:cmd,p:[x1,f*0+dy],k:{b:"Abajo",a:"Resolución",d:"Accion"}},
            {m:"Abajo",     c:cmd,p:[x1,f*1+dy],k:{b:"Derecha",a:"Arriba",d:"Hablar"}},
            {m:"Derecha",   c:cmd,p:[x1,f*2+dy],k:{b:"Izquierda",a:"Abajo",d:"Inventario"}},
            {m:"Izquierda", c:cmd,p:[x1,f*3+dy],k:{b:"Menu",a:"Derecha",d:"Cancelar"}},
            {m:"Menu",      c:cmd,p:[x1,f*4+dy],k:{b:"Debug",a:"Izquierda",d:"Posicion"}},
            {m:"Debug",     c:cmd,p:[x1,f*5+dy],k:{b:"Accion",a:"Menu",d:"Salir"}},
            # segunda columna
            {m:"Accion",    c:cmd,p:[x2,f*0+dy],k:{b:"Hablar",a:"Debug",i:"Arriba"}},
            {m:"Hablar",    c:cmd,p:[x2,f*1+dy],k:{b:"Inventario",a:"Accion",i:"Abajo"}},
            {m:"Inventario",c:cmd,p:[x2,f*2+dy],k:{b:"Cancelar",a:"Hablar",i:"Derecha"}},
            {m:"Cancelar",  c:cmd,p:[x2,f*3+dy],k:{b:"Posicion",a:"Inventario",i:"Izquierda"}},
            {m:"Posicion",  c:cmd,p:[x2,f*4+dy],k:{b:"Salir",a:"Cancelar",i:"Menu"}},
            {m:"Salir",     c:cmd,p:[x2,f*5+dy],k:{b:"Arriba",a:"Posicion",i:"Debug"}}]
        
        return botones
    
    def crear_espacios_config(self):
        for boton in self.botones:
            nom = boton.nombre.lower()
            x,y = boton.rect.topright
            if ' ' in nom:
                nom = nom.replace(' ','_')
                if self.data[nom]: opt = 'Sí'
                else: opt = 'No'
                esp = _opcion(opt,88,[x,y+9],14,1)
                self.espacios.add(esp)
            
            elif nom == 'resolución':
                nom = nom.replace('ó','o')
                ANCHO = self.data[nom]['ANCHO']
                ALTO = self.data[nom]['ALTO']
                esp = _opcion(str(ANCHO)+'x'+str(ALTO),88,[x,y+9],14,1)
            
            elif nom in self.data['teclas']:
                texto = self.data['teclas'][nom]
                nom = key_name(texto)
                esp = _opcion(nom,75,[x+3,y+9],14,1)
            
            self.espacios.add(esp)
    
    def elegir_botonYespacio(self):
        n = self.cur_btn
        tecla = self.espacios.get_sprite(n)
        boton = self.botones.get_sprite(n)
        return boton,tecla
    
    def cambiarBooleano(self):
        self.PressButton()
        boton,opcion = self.elegir_botonYespacio()
        if opcion.nombre == 'Sí':
            opcion.setText('No')
        else:
            opcion.setText('Sí')
        
        if boton.nombre == 'Mostrar Intro':
            C.asignar('mostrar_intro',not C.dato('mostrar_intro'))
        elif boton.nombre == 'Recordar Menus':
            C.asignar('recordar_menus',not C.dato('recordar_menus'))
    
    def setTecla (self):
        from engine.IO.modos import Modo
        '''Prepara la tecla elegida para ser cambiada'''
        
        boton,tecla = self.elegir_botonYespacio()
        boton.serPresionado()
        tecla.serElegido()
        
        Modo.setKey = True
        
    def cambiarTecla (self,tcl):
        '''Cambia la tecla elgida por el nuevo input'''
        
        boton,tecla = self.elegir_botonYespacio()        
        tecla.serDeselegido()
        tecla.setText(key_name(tcl))
        C.asignar('teclas/'+boton.nombre.lower(),tcl)
        self.mostrar_aviso()

    def mostrar_aviso(self):
        '''Muestra el aviso de que la configuración cambiará al reiniciar'''
        
        texto = 'Los cambios tendrán efecto al salir de este menú'
        fuente = font.SysFont('verdana',14)
        w,h = fuente.size(texto)
        x,y = self.canvas.get_width()-w-15,self.canvas.get_height()-h-15
        rect = Rect(x,y,w,h+1)
        render = render_textrect(texto,fuente,rect,self.font_low_color,self.bg_cnvs)
        self.canvas.blit(render,rect)
    
    def ejecutar_comando (self):
        self.current.comando()
        
    def cancelar(self):
        K.TECLAS.asignar(C.dato('teclas'))
        return True
    
    def update(self):
        self.botones.draw(self.canvas)
        self.espacios.draw(self.canvas)
        self.dirty = 1
