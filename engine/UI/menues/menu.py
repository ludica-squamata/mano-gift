from engine.globs import EngineData, ANCHO, ALTO, CAPA_OVERLAYS_MENUS, TEXT_SEL, CANVAS_BG
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.event_aware import EventAware
from engine.libs.textrect import render_textrect
from engine.UI.widgets import Boton, BaseWidget
from pygame.sprite import LayeredUpdates
from pygame import Rect, font


class Menu(EventAware, BaseWidget):
    botones = None
    filas = None
    cur_btn = 0
    cur_opt = 0
    current = ''
    canvas = None
    newMenu = False
    active = True
    layer = CAPA_OVERLAYS_MENUS
    opciones = 0
    sel = 0

    def __init__(self, nombre, titulo=None):
        self.nombre = nombre
        self.canvas = self.create_raised_canvas(ANCHO - 20, ALTO - 20)
        if titulo is None:
            titulo = nombre
        self.crear_titulo(titulo, ANCHO - 20)
        self.botones = LayeredUpdates()
        super().__init__(self.canvas, center=True)
        self.functions['tap'].update({'contextual': self.cancelar})
        self.functions['release'].update({'contextual': self.cancelar})
        EngineData.MENUS[nombre] = self

    def crear_titulo(self, titulo, ancho):
        fuente = font.Font('engine/libs/Verdana.ttf', 16)
        fuente.set_underline(True)
        ttl_rect = Rect((3, 3), (ancho - 7, 30))
        ttl_txt = render_textrect(titulo, fuente, ttl_rect, TEXT_SEL, CANVAS_BG, 1)
        self.canvas.blit(ttl_txt, ttl_rect.topleft)

    @staticmethod
    def deselect_all(lista):
        if len(lista) > 0:
            for item in lista:
                item.ser_deselegido()

    def mover_cursor(self, item):
        if item.tipo == 'boton':
            for i in range(len(self.botones)):
                spr = self.botones.get_sprite(i)
                if spr.nombre == item.nombre:
                    self.cur_btn = i
                    self.current = spr
                    break

        elif item.tipo == 'fila':
            for i in range(len(self.filas)):
                spr = self.filas.get_sprite(i)
                if item.nombre == spr.nombre:
                    self.cur_opt = i
                    self.current = spr
                    break

    def cancelar(self):
        """Esta funcion es un hook para otras funciones del mismo nombre."""
        self.deregister()
        EventDispatcher.trigger('OpenMenu', self.nombre, {'value': 'Previous'})

    def press_button(self):
        if len(self.botones) > 0:
            self.current.ser_presionado()
    
    def mantener_presion(self):
        self.current.mantener_presion()

    def liberar_presion(self):
        self.current.liberar_presion()

    def reset(self):
        """Resetea el estado de la ventana. Esta función es solo un hook."""
        self.active = True

    def select_one(self, direccion):
        self.deselect_all(self.botones)
        if len(self.botones) > 0:
            current = self.botones.get_sprite(self.cur_btn)
            if direccion in current.direcciones:
                selected = current.direcciones[direccion]
            else:
                selected = current.nombre

            for i in range(len(self.botones)):
                boton = self.botones.get_sprite(i)
                if boton.nombre == selected:
                    boton.ser_elegido()
                    self.mover_cursor(boton)
                    break

            self.botones.draw(self.canvas)

    def establecer_botones(self, botones, ancho_mod):
        for btn in botones:
            boton = Boton(btn['nombre'], ancho_mod, btn['comando'], btn['pos'])
            for direccion in ['arriba', 'abajo', 'izquierda', 'derecha']:
                if direccion in btn['direcciones']:
                    boton.direcciones[direccion] = btn['direcciones'][direccion]

            self.botones.add(boton)

        self.cur_btn = 0
        self.select_one(0)
        self.reset()

    def posicionar_cursor(self, i):
        self.sel += i
        if self.sel < 0:
            self.sel = self.opciones - 1

        elif self.sel > self.opciones - 1:
            self.sel = 0

    def __repr__(self):
        return 'Menu_' + self.nombre + ' (en ' + str(len(self.groups())) + ' grupos)'
