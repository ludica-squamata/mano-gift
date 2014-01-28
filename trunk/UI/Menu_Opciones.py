from .Menu import Menu
from .Menu_Pausa import Menu_Pausa
from .Colores import Colores
from misc import Config as c
from ._boton import _boton
from ._opcion import _opcion
from globs.constantes import Constants as K
from pygame.sprite import LayeredDirty
from pygame import key

class Menu_Opciones (Menu_Pausa,Menu):
    def __init__(self):
        Menu.__init__(self,'Opciones')
        self.funciones = {
            "arriba":self.selectOne,
            "abajo":self.selectOne,
            "izquierda":self.selectOne,
            "derecha":self.selectOne,
            "hablar":self.PressButton}
        
        self.keyup = {
            "hablar":self.ReleaseButton}
        
        self.botones = LayeredDirty()
        self.esp_teclas = LayeredDirty()
        #las imagenes del boton y la tecla estan vinculados por index
        self.establecer_botones(self.crear_botones_teclas(),4)
        self.esp_teclas.add(self.crear_espacios_teclas())
        self.esp_teclas.draw(self.canvas)
        
        print(self.botones.get_sprite(1).nombre,
              self.esp_teclas.get_sprite(1).nombre)
    
    def crear_botones_teclas (self):
        #abreviaturas para hacer más legible el código
        m, k,p = 'nombre','direcciones','pos'
        a,b,i,d = 'arriba','abajo','izquierda','derecha'
        dx, dy, n = 226,220,38 # constantes numéricas de posicion
        botones = [
            {m:"Arriba",p:[5,n*0+dy],k:{b:"Abajo",d:"Cancelar"}},
            {m:"Abajo",p:[5,n*1+dy],k:{b:"Derecha",a:"Arriba",d:"Inventario"}},
            {m:"Derecha",p:[5,n*2+dy],k:{b:"Izquierda",a:"Abajo",d:"Posicion"}},
            {m:"Izquierda",p:[5,n*3+dy],k:{b:"Accion",a:"Derecha",d:"Menu"}},
            {m:"Accion",p:[5,n*4+dy],k:{b:"Hablar",a:"Izquierda",d:"Debug"}},
            {m:"Hablar",p:[5,n*5+dy],k:{b:"Cancelar",a:"Accion",d:"Salir"}},
            {m:"Cancelar",p:[dx,n*0+dy],k:{b:"Inventario",a:"Hablar",i:"Arriba"}},
            {m:"Inventario",p:[dx,n*1+dy],k:{b:"Posicion",a:"Cancelar",i:"Abajo"}},
            {m:"Posicion",p:[dx,n*2+dy],k:{b:"Menu",a:"Inventario",i:"Derecha"}},
            {m:"Menu",p:[dx,n*3+dy],k:{b:"Debug",a:"Posicion",i:"Izquierda"}},
            {m:"Debug",p:[dx,n*4+dy],k:{b:"Salir",a:"Menu",i:"Accion"}},
            {m:"Salir",p:[dx,n*5+dy],k:{a:"Debug",i:"Hablar"}}]
        
        return botones
    
    def crear_espacios_teclas (self):
        TECLAS = []
        teclas = ["ARRIBA","ABAJO","DERECHA","IZQUIERDA",
                  "ACCION","HABLAR","CANCELAR_DIALOGO","INVENTARIO",
                  "POSICION_COMBATE","MENU","DEBUG","SALIR"]
        x, y, n = 144,230,38 # constantes numéricas de posicion
        dx = x+32*7
        for t in range(len(teclas)):
            texto = key.name(eval('K.TECLAS.'+teclas[t]))
            if t > 5:
                t -= 6
                x = dx
            TECLAS.append(_opcion(texto,32*2,[x,n*t+y],14,1))
        
        return TECLAS
    
    