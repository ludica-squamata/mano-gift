from engine.globs import ANCHO, ALTO, CAPA_OVERLAYS_DIALOGOS
from engine.libs import render_tagged_text
from engine.globs.renderer import Renderer
from pygame import Rect, Surface
from .widgets import Ventana


class DialogInterface(Ventana):
    text_rect = None
    rendered_text = None
    active = True
    loc_img = None
    loc_rect = None
    menu = None
    w, h = 0, 0
    sel_mode = False

    def __init__(self, parent):
        image = Surface((int(ANCHO), int(ALTO / 5)))
        image.fill(self.bg_cnvs)
        self.parent = parent
        super().__init__(image)

        self.marco = self.crear_marco(*self.rect.size)
        self.w, self.h = self.image.get_size()
        self.draw_space_rect = Rect((3, 3), (self.w - 6, self.h - 7))
        self.erase_area = Rect(3, 3, self.w - 7, self.h - 7)
        self.text_rect = Rect(0, 3, 0, 0)
        self.loc_rect = Rect(0, 0, 0, 0)
        self.arrow_width = 16

        self.fuente = self.fuente_M
        self.altura_del_texto = self.fuente.get_height()
        self.ubicar(0, ALTO - int(ALTO / 5))
        Renderer.add_overlay(self, CAPA_OVERLAYS_DIALOGOS)

    def ubicar(self, x=0, y=0, z=0):
        if x < 0 or y < 0:
            raise ValueError('Coordenadas inválidas')
        self.rect.move_ip(x, y)

    def set_text(self, texto):
        self.text_rect.y = 3
        width = self.draw_space_rect.width
        if not self.loc_rect.x:
            self.text_rect.x = 6
        else:
            width -= self.loc_rect.w+self.arrow_width+1
        self.rendered_text = render_tagged_text(texto, self.tags, width, bgcolor=self.bg_cnvs)
        self.text_rect.size = self.rendered_text.get_size()

    def set_sel_mode(self, opciones):
        self.menu.supress_all()

        for i in range(len(sorted(opciones, key=lambda o: o.indice))):
            opt = opciones[i]
            obj = {'idx': i + 1, 'icon': str(opt.indice), 'name': str(opt.leads), 'item': opciones[i]}
            self.menu.add_element(0, obj)
            # Este overwrite es necesario porque si no do_action() hace otra cosa.
            self.menu.cubos.get_sprite(i).do_action = lambda: True

        self.opciones = len(opciones)
        self.menu.actual = self.menu.cubos.get_sprite(0)
        self.set_text(opciones[0].texto)
        self.sel_mode = True

    def set_menu(self, menu):
        self.menu = menu

    def rotar_menu(self, delta):
        self.menu.turn(delta)

    def detener_menu(self):
        self.menu.stop()

    def exit_sel_mode(self):
        self.sel_mode = False
        Renderer.clear_overlays_from_layer(self.menu.layer)
        self.menu.cubos.empty()

    def set_loc_img(self, locutor):
        """carga y dibuja la imagen de quien está hablando. También setea
        la posición del texto a izquierda o derecha según la "cara" del hablante"""
        self.loc_img = locutor.diag_face
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
                        self.text_rect.y += dy * 3  # TODO: "3" podría ser un setting
            self.ticks = 0

    def borrar_todo(self):
        self.image.fill(self.bg_cnvs)
        self.rendered_text = None
        self.sel = 0

    def update(self):
        self.ticks += 1
        self.image.fill(self.bg_cnvs, self.erase_area)
        if self.loc_img is not None:
            self.image.blit(self.loc_img, self.loc_rect)

        if self.sel_mode and self.menu.stopped:
            self.set_text(self.menu.actual.item.texto)
            self.sel = self.menu.actual.item

        self.image.blit(self.rendered_text, self.text_rect)
        if not self.draw_space_rect.contains(self.text_rect):
            color = self.bg_bisel_fg
            x, y = self.text_rect.right + 1, 0
            w, h = self.arrow_width, self.draw_space_rect.h + 3

            # pintar el area de la flecha, si es que hay más contenido que ver.
            self.image.fill(color, (x, y, w, h))

        # dibujar el marco biselado.
        self.image.blit(self.marco, (0, 0))
