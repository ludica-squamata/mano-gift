from .Menu import Menu
from globs import Constants as C
from ._boton import _boton
from pygame import Rect, Surface, font, draw
from pygame.sprite import LayeredDirty
from libs.textrect import render_textrect

class Menu_Pausa (Menu):
    def __init__(self):
        super().__init__("Pausa")
        x = self.canvas.get_width()-(C.CUADRO*6)-14 # 460-192-14 = 254
        botones = {"Items": {"pos":[x,93] ,"direcciones":{"abajo":"Equipo"}},
                   "Equipo":{"pos":[x,132],"direcciones":{"arriba":"Items","abajo":"Status"}},
                   "Status":{"pos":[x,171],"direcciones":{"arriba":"Equipo","abajo":"Grupo"}},
                   "Grupo": {"pos":[x,210],"direcciones":{"arriba":"Status","abajo":"Opciones"}},
                   "Opciones":{"pos":[x,249],"direcciones":{"arriba":"Grupo","abajo":"Debug"}},
                   "Debug":{"pos":[x,288],"direcciones":{'arriba':'Opciones'}}}        
        self.funciones = {
            "arriba":self.selectOne,
            "abajo":self.selectOne,
            "izquierda":self.selectOne,
            "derecha":self.selectOne,
            "hablar":self.PressOne}
        self.botones = LayeredDirty()
        self.establecer_botones(botones,6)
        
    def establecer_botones(self,botones,ancho_mod):
        for btn in botones:
            boton = self._crear_boton(btn,ancho_mod,*botones[btn]['pos'])
            for direccion in ['arriba','abajo','izquierda','derecha']:
                if direccion in botones[btn]['direcciones']:
                    boton.direcciones[direccion] = botones[btn]['direcciones'][direccion]
            
            self.botones.add(boton)

        self.cur_btn = 2
        self.Reset()
                
    def _crear_boton(self,texto,ancho_mod,x,y):
        ancho = C.CUADRO*ancho_mod
        
        rect = Rect((x,y),((ancho)-6,C.CUADRO-6))
        
        cnvs_pre = Surface(((ancho)+6,C.CUADRO+6))
        cnvs_pre.fill(self.bg_cnvs)
        cnvs_sel = cnvs_pre.copy()
        cnvs_uns = cnvs_pre.copy()
        
        fnd_pre = self.crear_inverted_canvas(ancho,C.CUADRO)
        fnd_uns = self.crear_canvas((ancho),C.CUADRO)
        
        for i in range(round(((C.CUADRO*ancho)+6)/3)):
            #linea punteada horizontal superior
            draw.line(cnvs_sel,self.font_high_color,(i*7,0),((i*7)+5,0),2)
            
            #linea punteada horizontal inferior
            draw.line(cnvs_sel,self.font_high_color,(i*7,C.CUADRO+4),((i*7)+5,C.CUADRO+4),2)
        
        for i in range(round((C.CUADRO+6)/3)):
            #linea punteada vertical derecha
            draw.line(cnvs_sel,self.font_high_color,(0,i*7),(0,(i*7)+5),2)
            
            #linea punteada vertical izquierda
            draw.line(cnvs_sel,self.font_high_color,(ancho+4,i*7),(ancho+4,(i*7)+5),2)
        
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

    def PressOne(self):
        if len(self.botones) > 0:
            self.current.serPresionado()
            self.botones.draw(self.canvas)
        
        self.newMenu = True
    
    def Reset(self,recordar=False):
        '''Reseta el presionado de todos los botones, y deja seleccionado
        el que haya sido elegido anteriormente. Esto deberia ser seteable.'''
        self.DeselectAll(self.botones)
        if not recordar: # podría ser W.recordar.. o un seteo de config
            self.cur_btn = 2
        selected = self.botones.get_sprite(self.cur_btn)
        selected.serElegido()
        self.current = selected
        self.botones.draw(self.canvas)
        self.dirty = 1