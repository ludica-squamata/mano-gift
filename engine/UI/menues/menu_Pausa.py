from pygame.sprite import LayeredUpdates
from .menu import Menu
from engine.globs import Constants as C
from engine.misc import Config as cfg
from engine.UI.widgets import _boton
from engine.libs.textrect import render_textrect

class Menu_Pausa (Menu):
    def __init__(self):
        super().__init__("Pausa")
        x = self.canvas.get_width()-(C.CUADRO*6)-14 # 460-192-14 = 254
        m,k,p,c = 'nombre','direcciones','pos','comando'
        a,b,i,d = 'arriba','abajo','izquierda','derecha'
        cmd = lambda:print('anda')
        botones = [
            {m:"Items",   p:[x,93] ,k:{b:"Equipo"},             c:self.PressOne},
            {m:"Equipo",  p:[x,132],k:{a:"Items",b:"Status"},   c:self.PressOne},
            {m:"Status",  p:[x,171],k:{a:"Equipo",b:"Grupo"},   c:self.PressOne},
            {m:"Grupo",   p:[x,210],k:{a:"Status",b:"Opciones"},c:self.PressOne},
            {m:"Opciones",p:[x,249],k:{a:"Grupo",b:"Debug"},    c:self.PressOne},
            {m:"Debug",   p:[x,288],k:{a:'Opciones'},           c:self.PressOne}]
        
        self.botones = LayeredUpdates()
        self.establecer_botones(botones,6)
        self.selectOne('arriba')
        self.funciones = {
            "arriba":self.selectOne,
            "abajo":self.selectOne,
            "izquierda":self.selectOne,
            "derecha":self.selectOne,
            "hablar":self.current.comando}

    def establecer_botones(self,botones,ancho_mod):
        for btn in botones:
            boton = _boton(btn['nombre'],ancho_mod,btn['comando'],btn['pos'])
            for direccion in ['arriba','abajo','izquierda','derecha']:
                if direccion in btn['direcciones']:
                    boton.direcciones[direccion] = btn['direcciones'][direccion]
            
            self.botones.add(boton)

        self.cur_btn = 0
        self.Reset()
                
    def selectOne(self,direccion):
        self.DeselectAll(self.botones)
        if len(self.botones) > 0:
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
    
    def cancelar(self):
        return False
        
    def PressOne(self):
        from engine.IO.modos import Modo
        super().PressButton()
        Modo.newMenu = True
    
    def Reset(self):
        '''Reseta el presionado de todos los botones, y deja seleccionado
        el que haya sido elegido anteriormente.'''
        self.DeselectAll(self.botones)
        if not cfg.dato('recordar_menus'):
            self.cur_btn = 0
        selected = self.botones.get_sprite(self.cur_btn)
        selected.serElegido()
        self.current = selected
        self.botones.draw(self.canvas)
        self.active = True