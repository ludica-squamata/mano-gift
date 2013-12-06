# intro.py
# módulo de introducción y selección de modo.
from pygame import Surface, Rect, QUIT, KEYDOWN, KEYUP, sprite, Color
from pygame import display as pantalla, event as EVENT,quit as py_quit,font
from globs import Tiempo as T, Constants as C, World as W
from misc import Resources as r
from UI import Menu_Pausa, _opcion
from libs.textrect import render_textrect
import sys,os,os.path

###TODO###
# menu de selección (opciones):
# # game (deshabilitada)
# # configuracion (deshabilitada)
# # debug screen
# # # seleccion de mapa.
# # # play.

class introduccion (Menu_Pausa):
    canvas = ''
    running = True
    sel = 0
    opciones = 0
    mapas = []
    filas = None
    def __init__ (self,ANCHO,ALTO):
        self.botones = sprite.LayeredDirty()
        self.filas = sprite.LayeredDirty()
        self.botones.empty()
        self.canvas = self.crear_canvas(ANCHO,ALTO)
        self.crear_espacio_de_seleccion_de_mapas(ANCHO-17)
        self.crear_titulo("Mano-Gift:Debug Screen",self.font_high_color,self.bg_cnvs,ANCHO)
        botones = {"Cargar":{"pos":[7,270],"direcciones":{"derecha":"Salir"}},
                  "Salir":{"pos":[254,270],"direcciones":{"izquierda":"Cargar"}}}
        self.establecer_botones(botones,6)
    
    def cargar_mapas_iniciales(self):
        ok = []
        for mapa in os.listdir('maps'):
            ar = r.abrir_json('maps/'+mapa)
            if 'inicial' in ar['entradas']:
                ok.append(mapa[0:-5])
        
        return ok
    
    def crear_espacio_de_seleccion_de_mapas (self,ancho):
        mapas = self.crear_espacio_titulado(ancho,200,'Elija un mapa')
        rect = self.canvas.blit(mapas,(7,40))
        self.image = Surface((rect.w-8,rect.h-30))
        self.image.fill(self.bg_cnvs)
        self.draw_space = self.image.get_rect(topleft=(8,120))
        
        fuente = font.SysFont('verdana', 16)
        self.altura_del_texto = fuente.get_height()+1
        self.mapas = self.cargar_mapas_iniciales() # lista
        self.opciones = len(self.mapas)
        for i in range(len(self.mapas)):
            opcion = _opcion(self.mapas[i],self.draw_space.w,(3,(i*22)+1+(i-1)))
            self.filas.add(opcion)
        
        self.filas.draw(self.image)
    
    def elegir_opcion(self,i):
        return self.dibujar_lineas_cursor (i,self.image,self.draw_space.w,self.sel,self.opciones)
    
    def ejecutar (self,fondo):
        elegir_uno = False
        while self.running:
            T.FPS.tick(60)
            for event in EVENT.get():
                if event.type == QUIT:
                    py_quit()
                    sys.exit()
                    
                elif event.type == KEYDOWN:                 
                    if event.key == C.TECLAS.SALIR:
                        py_quit()
                        print('Saliendo...')
                        sys.exit()
                    
                    elif event.key == C.TECLAS.IZQUIERDA:
                        self.selectOne('izquierda')
                        
                    elif event.key == C.TECLAS.DERECHA:
                        self.selectOne('derecha')
                    
                    elif event.key == C.TECLAS.ARRIBA:
                        self.DeselectAll(self.botones)
                        self.sel = self.elegir_opcion(-1)
                        elegir_uno = True
                    
                    elif event.key == C.TECLAS.ABAJO:
                        self.DeselectAll(self.botones)
                        self.sel = self.elegir_opcion(+1)
                        elegir_uno = True
                    
                    elif event.key == C.TECLAS.HABLAR:
                        if self.current.nombre == "Cargar":
                            if elegir_uno:
                                self.PressOne()
                        else:
                            self.PressOne()
                        
                    
                elif event.type == KEYUP:
                    if event.key == C.TECLAS.HABLAR:
                        if self.current.nombre == "Cargar":
                            if elegir_uno:
                                self.running = False
                                W.cargar_hero()
                                W.setear_mapa(self.mapas[self.sel-1], 'inicial')
                            
                        elif self.current.nombre ==  "Salir":
                            py_quit()
                            print('Saliendo...')
                            sys.exit()
            
            self.canvas.blit(self.image,(10,66))
            fondo.blit(self.canvas,(10,10))
            pantalla.update()

class intro_animation:
    timer = 0
    def __init__(self):        
        self.fuente_1 = font.SysFont('Verdana',24,bold=True)
        self.nombre = 'Lúdica Squamata'
        w,h = self.fuente_1.size(self.nombre)
        self.nom_rect = Rect((0,0),(w,h+10))
        
        self.fuente_2 = font.SysFont('Verdana',16,italic=True)
        self.presenta ='Presenta...'
        w,h = self.fuente_2.size(self.presenta)
        self.pre_rect = Rect((0,0),(w,h+10))
        
        self.fuente_3 = font.SysFont('Verdana',16)
        self.produccion = 'una producción de\nZeniel Danaku & Einacio Spiegel'
        w,h = self.fuente_3.size(self.produccion)
        self.pro_rect = Rect((0,0),(w,h+40))
        
        self.fuente_4 = font.SysFont('Verdana',30,bold=True)
        self.titulo = 'Proyecto\nMano-Gift'
        w,h = self.fuente_4.size(self.titulo)
        self.ttl_rect = Rect((0,0),(C.ANCHO,h+40))
        
        self.continuar = '< Presione una tecla para continuar >'
        w,h = self.fuente_3.size(self.continuar)
        self.cont_rect = Rect(0,0,C.ANCHO,h+10)
        
        self.rojo = Color(255,0,0)
        self.verde = Color(0,255,0)
        self.azul = Color(0,0,255)
        self.negro = Color(0,0,0)
        self.blanco = Color(255,255,255)
        self.gris = Color(125,125,125)
    
    def go(self,fondo):
        running = 1
        j = 0
        while running == 1:
            T.FPS.tick(60)
            for event in EVENT.get():
                if event.type == QUIT: running = 0
                
                if event.type == KEYDOWN:
                    if event.key == C.TECLAS.SALIR:
                        py_quit()
                        print('Saliendo...')
                        sys.exit()
                    else:
                        running = 0
            self.timer += 1
            timer = self.timer
            if self.timer <= 60:
                fondo.fill(self.negro)
            
            # Lúdica Squamata
            i = 0
            render = render_textrect(self.nombre,self.fuente_1,self.nom_rect,self.azul,self.negro)
            if 61 <= self.timer <180:
                i+=10
                render.set_alpha(i)
                fondo.blit(render,(192,192))
            
            # Presenta...
            i = 0
            render = render_textrect(self.presenta,self.fuente_2,self.pre_rect,self.verde,self.negro)
            if 181 <= self.timer < 300:
                i += 10
                render.set_alpha(i)
                fondo.blit(render,(288,230))
            
            # Una producción de Zeniel Danaku & Einacio Spiegel    
            i = 0
            render = render_textrect(self.produccion,self.fuente_3,self.pro_rect,self.rojo,self.negro,1)
            if 301 <= self.timer < 600:
                i += 10
                render.set_alpha(i)
                fondo.blit(render,(32,192))
            
            # Proyecto Mano-Gift 
            render = render_textrect(self.titulo,self.fuente_4,self.ttl_rect,self.negro,self.blanco,1)
            if 601 <= self.timer < 661:
                fondo.fill(self.blanco)
            
            if 662 <= self.timer < 900:
                fondo.blit(render,(0,96))
            
            # <Presione una tecla para continuar>
            if self.timer > 1200:
                j += 1
                h = self.fuente_3.get_height()
                render = render_textrect(self.continuar,self.fuente_3,self.cont_rect,self.rojo,self.blanco,1)
                
                if j <= 32:
                    fondo.blit(render,(0,332))
                elif j <= 64:
                    fondo.fill(self.blanco,(0,332,C.ANCHO,h+10))
                else:
                    j = 0
                
            pantalla.flip()


