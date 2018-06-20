from engine.globs import ANCHO, ALTO, CAPA_OVERLAYS_DIALOGOS, Item_Group, Deleted_Items, CANVAS_BG, SCROLL_BG, Tiempo
from engine.misc.tagloader import load_tagarrayfile
from engine.libs import render_tagged_text
from engine.globs.renderer import Renderer
from pygame import Rect, Surface
from .widgets import BaseWidget
from itertools import cycle


class DialogInterface(BaseWidget):
    text_rect = None
    rendered_text = None
    active = True
    loc_img = None
    loc_rect = None
    menu = None
    w, h = 0, 0
    sel_mode = False
    opciones = 0
    marco = None
    draw_space_rect = None
    erase_area = None
    arrow_width = 0
    drawn = False
    ticks = 0
    sel = 0
    custom_tags = ''

    timer_animacion = 0
    frame_animacion = 0

    cycler = None  # itertools.cycle

    def __init__(self, parent, custom_tags=''):
        image = Surface((int(ANCHO), int(ALTO / 5)))
        image.fill(CANVAS_BG)
        self.parent = parent
        super().__init__(image)
        if custom_tags != '':
            self.custom_tags = load_tagarrayfile('data/dialogs/' + custom_tags)
        self.marco = self.crear_marco(*self.rect.size)
        self.w, self.h = self.image.get_size()
        self.draw_space_rect = Rect((3, 3), (self.w - 6, self.h - 7))
        self.erase_area = Rect(3, 3, self.w - 7, self.h - 7)
        self.text_rect = Rect(0, 3, 0, 0)
        self.loc_rect = Rect(0, 0, 0, 0)
        self.arrow_width = 16
        self.ubicar(0, ALTO - int(ALTO / 5))

        self.timer_animacion = 0
        self.frame_animacion = 1000 / 6

        Renderer.add_overlay(self, CAPA_OVERLAYS_DIALOGOS)

    def ubicar(self, x=0, y=0, z=0):
        assert x > 0 or y > 0, 'Coordenadas inválidas'
        self.rect.move_ip(x, y)

    def set_text(self, texto, omitir_tags=None):
        width = self.draw_space_rect.width
        if not self.loc_rect.x:
            self.text_rect.x = 6
        else:
            width -= self.loc_rect.w + self.arrow_width + 1

        self.rendered_text = render_tagged_text(texto, width,
                                                custom_tags=self.custom_tags,
                                                omitted_tags=omitir_tags)

        self.text_rect.size = self.rendered_text.get_size()
        if self.text_rect.h < self.draw_space_rect.h:
            self.text_rect.y = 3  # reset scrolling
        self.drawn = True

    def set_sel_mode(self, opciones):
        self.menu.supress_all()

        for i in range(len(sorted(opciones, key=lambda o: o.indice))):
            opt = opciones[i]
            icon = str(opt.indice)
            name = str(opt.leads)
            if opt.reqs is not None and 'objects' in opt.reqs:
                objeto = opt.reqs['objects'][0]
                # la alternativa a este embrollo es que el branch especifique nombre e icono
                item = None
                existing_items = Item_Group + Deleted_Items
                if objeto in existing_items:
                    item = existing_items[objeto]

                icon = item.image
                name = item.nombre

            obj = {'idx': i + 1, 'icon': icon, 'name': name, 'item': opciones[i]}
            self.menu.add_element('inicial', obj)

        self.opciones = len(opciones)
        self.menu.actual = self.menu.cubos.get_sprite(0)
        self.set_text(opciones[0].texto)
        self.sel_mode = True
        self.drawn = False

    def set_menu(self, menu):
        self.menu = menu
        self.menu.deregister()

    def rotar_menu(self, delta):
        self.menu.turn(delta)
        self.drawn = False

    def detener_menu(self):
        self.menu.stop()

    def has_stopped(self):
        return self.menu.stopped

    def exit_sel_mode(self):
        self.sel_mode = False
        Renderer.clear_overlays_from_layer(self.menu.layer)
        self.menu.cubos.empty()

    def set_loc_img(self, locutor):
        """carga y dibuja la imagen de quien está hablando. También setea
        la posición del texto a izquierda o derecha según la "cara" del hablante"""
        self.cycler = cycle(locutor.diag_face)
        self.loc_img = next(self.cycler)
        self.loc_rect = self.loc_img.get_rect(y=3)
        if locutor.direccion == 'derecha' or locutor.direccion == 'abajo':
            self.loc_rect.x = 3
            self.text_rect.x = self.loc_rect.w + 6
            self.draw_space_rect.x = self.loc_rect.w + 6
        else:
            self.loc_rect.x = self.w - self.loc_rect.w
            self.text_rect.x = 6
            self.draw_space_rect.x = 6

    def scroll(self, dy):
        if self.ticks > 10:
            if not self.draw_space_rect.contains(self.text_rect):
                if self.text_rect.top + dy < self.draw_space_rect.top:
                    if self.text_rect.bottom + dy > self.draw_space_rect.bottom:
                        self.text_rect.y += dy * 3  # "3" podría ser un setting
            self.ticks = 0

    def borrar_todo(self):
        self.image.fill(CANVAS_BG)
        self.rendered_text = None
        self.sel = 0
        self.text_rect.y = 3  # reset scrolling

    def update(self):
        self.ticks += 1
        self.image.fill(CANVAS_BG, self.erase_area)
        if self.loc_img is not None:
            self.timer_animacion += Tiempo.FPS.get_time()
            if self.timer_animacion >= self.frame_animacion:
                self.timer_animacion = 0
                self.loc_img = next(self.cycler)

            self.image.blit(self.loc_img, self.loc_rect)

        if self.sel_mode and self.menu.stopped and not self.drawn:
            self.set_text(self.menu.actual.item.texto)
            self.sel = self.menu.actual.item

            # actualizar el dialogo
            self.parent.update(self.sel)

        self.image.blit(self.rendered_text, self.text_rect)
        if not self.draw_space_rect.contains(self.text_rect):
            x, y = self.text_rect.right + 1, 0
            w, h = self.arrow_width, self.draw_space_rect.h + 3

            # pintar el area de la flecha, si es que hay más contenido que ver.
            self.image.fill(SCROLL_BG, (x, y, w, h))

        # dibujar el marco biselado.
        self.image.blit(self.marco, (0, 0))
