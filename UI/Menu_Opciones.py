from .Menu import Menu
from .modos import modo
from .Menu_Pausa import Menu_Pausa
from ._boton import _boton
from ._opcion import _opcion
from globs.constantes import Constants as K
from pygame.sprite import LayeredDirty
from pygame.key import name as  key_name

class Menu_Opciones (Menu_Pausa,Menu):
    def __init__(self):
        Menu.__init__(self,'Opciones')
        self.funciones = {
            "arriba":self.selectOne,
            "abajo":self.selectOne,
            "izquierda":self.selectOne,
            "derecha":self.selectOne,
            "hablar":self.setTecla}
        
        self.keyup = {
            "hablar":self.ReleaseButton}
        
        self.botones = LayeredDirty()
        self.esp_teclas = LayeredDirty()
        #las imagenes del boton y la tecla estan vinculados por index
        self.establecer_botones(self.crear_botones_teclas(6,228),4)
        self.esp_teclas.add(self.crear_espacios_teclas(140,362,2.75))
        self.esp_teclas.draw(self.canvas)
        
    def crear_botones_teclas (self,x1,x2):
        #abreviaturas para hacer más legible el código
        m, k,p = 'nombre','direcciones','pos'
        a,b,i,d = 'arriba','abajo','izquierda','derecha'
        dy, f = 185,38 # constantes numéricas de posicion # f = fila
        botones = [
            # primera columna
            {m:"Arriba",    p:[x1,f*0+dy],k:{b:"Abajo",a:"Salir",d:"Cancelar"}},
            {m:"Abajo",     p:[x1,f*1+dy],k:{b:"Derecha",a:"Arriba",d:"Inventario"}},
            {m:"Derecha",   p:[x1,f*2+dy],k:{b:"Izquierda",a:"Abajo",d:"Posicion"}},
            {m:"Izquierda", p:[x1,f*3+dy],k:{b:"Accion",a:"Derecha",d:"Menu"}},
            {m:"Accion",    p:[x1,f*4+dy],k:{b:"Hablar",a:"Izquierda",d:"Debug"}},
            {m:"Hablar",    p:[x1,f*5+dy],k:{b:"Cancelar",a:"Accion",d:"Salir"}},
            # segunda columna
            {m:"Cancelar",  p:[x2,f*0+dy],k:{b:"Inventario",a:"Hablar",i:"Arriba"}},
            {m:"Inventario",p:[x2,f*1+dy],k:{b:"Posicion",a:"Cancelar",i:"Abajo"}},
            {m:"Posicion",  p:[x2,f*2+dy],k:{b:"Menu",a:"Inventario",i:"Derecha"}},
            {m:"Menu",      p:[x2,f*3+dy],k:{b:"Debug",a:"Posicion",i:"Izquierda"}},
            {m:"Debug",     p:[x2,f*4+dy],k:{b:"Salir",a:"Menu",i:"Accion"}},
            {m:"Salir",     p:[x2,f*5+dy],k:{b:"Arriba",a:"Debug",i:"Hablar"}}]
        
        return botones
    
    def crear_espacios_teclas (self,x,x1,ancho_mod):
        TECLAS = []
        teclas = ["ARRIBA","ABAJO","DERECHA","IZQUIERDA",
                  "ACCION","HABLAR","CANCELAR_DIALOGO","INVENTARIO",
                  "POSICION_COMBATE","MENU","DEBUG","SALIR"]
        y, n =195,38 # constantes numéricas de posicion
        for t in range(len(teclas)):
            texto = key_name(eval('K.TECLAS.'+teclas[t]))
            if t > 5:
                t -= 6
                x = x1
            TECLAS.append(_opcion(texto,int(32*ancho_mod),[x,n*t+y],14,1))
        
        return TECLAS
    
    def setTecla (self):
        '''Prepara la tecla elegida para ser cambiada'''
        
        for tcl in self.esp_teclas:
            tcl.serDeselegido()
            
        n = self.cur_btn
        tecla = self.esp_teclas.get_sprite(n)
        boton = self.botones.get_sprite(n)
        
        boton.serPresionado()
        tecla.serElegido()
        
        modo.setKey = True
    
    def cambiarTecla (self,tcl):
        '''Cambia la tecla elgida por el nuevo input'''
        
        tecla = self.esp_teclas.get_sprite(self.cur_btn)
        tecla.serDeselegido()
        tecla.setText(key_name(tcl))
    
    def update(self):
        self.botones.draw(self.canvas)
        self.esp_teclas.draw(self.canvas)
        self.dirty = 1