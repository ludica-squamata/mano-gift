from engine.libs import render_tagged_text
from .widgets import Fila, Ventana
from pygame import Rect, Surface
from pygame.sprite import LayeredUpdates
from engine.globs import EngineData as Ed, ANCHO, ALTO, CAPA_OVERLAYS_DIALOGOS
from engine.globs.renderer import Renderer


class DialogInterface(Ventana):
    text_rect = None
    rendered_text = None
    active = True
    loc_img = None
    loc_rect = None
    w, h = 0, 0

    def __init__(self):
        image = Surface((int(ANCHO), int(ALTO / 5)))
        image.fill(self.bg_cnvs)
        super().__init__(image)

        self.filas = LayeredUpdates()
        self.marco = self.crear_marco(*self.rect.size)
        self.w, self.h = self.image.get_size()
        self.draw_space_rect = Rect((3, 3), (self.w - 115, self.h - 7))
        self.erase_area = Rect(3, 3, self.w - 7, self.h - 7)
        self.text_rect = Rect(0, 3, 0, 0)

        self.fuente = self.fuente_M
        self.altura_del_texto = self.fuente.get_height()
        self.ubicar(0, ALTO - int(ALTO / 5))
        Renderer.add_overlay(self, CAPA_OVERLAYS_DIALOGOS)

    def destruir(self):
        Ed.end_dialog(CAPA_OVERLAYS_DIALOGOS)

    def ubicar(self, x=0, y=0, z=0):
        if x < 0 or y < 0:
            raise ValueError('Coordenadas inválidas')
        self.rect.move_ip(x, y)

    def set_text(self, texto):
        self.text_rect.y = 3
        width = self.draw_space_rect.width
        self.rendered_text = render_tagged_text(texto, self.tags, width, bgcolor=self.bg_cnvs)
        self.text_rect.size = self.rendered_text.get_size()

    def set_sel_mode(self, opciones):
        self.opciones = len(opciones)
        h = self.altura_del_texto
        x = self.draw_space_rect.x
        w = self.draw_space_rect.w
        for i in range(self.opciones):
            opcion = Fila(opciones[i], w, x, i * h + i + 3)
            self.filas.add(opcion)
        self.elegir_opcion(0)

    def set_loc_img(self, locutor):
        """carga y dibuja la imagen de quien está hablando. También setea
        la posición del texto a izquierda o derecha según la "cara" del hablante"""
        self.loc_img = locutor.diag_face
        if locutor.direccion == 'derecha' or locutor.direccion == 'abajo':
            self.loc_rect = 3, 3
            self.text_rect.x = 96
            self.draw_space_rect.x = 96
        else:
            self.loc_rect = self.w - 93, 3
            self.text_rect.x = 3
            self.draw_space_rect.x = 3

    def elegir_opcion(self, dy):
        if self.ticks > 10:
            # get the option's position
            self.posicionar_cursor(dy)

            # get current's sprite, self.sel is current's ID
            current = self.filas.get_sprite(self.sel)
            h = self.altura_del_texto
            if not self.draw_space_rect.contains(current.rect):
                if current.rect.y < 0:
                    for op in self.filas.sprites():
                        op.rect.y += h + 1
                elif current.rect.y < self.draw_space_rect.bottom:
                    for op in self.filas.sprites():
                        op.rect.y -= h + 1

            # deselect all and select the chosen one
            for fila in self.filas:
                fila.ser_deselegido()
            current.ser_elegido()

            self.ticks = 0
            return current.item

    def scroll(self, dy):
        if self.ticks > 10:
            if not self.draw_space_rect.contains(self.text_rect):
                if self.text_rect.top + dy < self.draw_space_rect.top:
                    if self.text_rect.bottom + dy > self.draw_space_rect.bottom:
                        self.text_rect.y += dy * 3  # TODO: "3" podría ser un setting
            self.ticks = 0

    def borrar_todo(self):
        self.image.fill(self.bg_cnvs)
        self.filas.empty()
        self.rendered_text = None
        self.sel = 0

    def update(self):
        self.ticks += 1
        self.image.blit(self.loc_img, self.loc_rect)

        color = self.bg_cnvs  # TODO: estos colores deberían ser otros

        if len(self.filas):
            filas = [fila for fila in self.filas if self.draw_space_rect.contains(fila.rect)]
            if len(self.filas) > len(filas):
                color = self.bg_bisel_bg
            for fila in filas:
                self.image.blit(fila.image, fila.rect)

        else:
            # si no hay filas, la imagen es lo que sale de set_text.
            self.image.blit(self.rendered_text, self.text_rect)
            if not self.draw_space_rect.contains(self.text_rect):
                color = self.bg_bisel_fg

        # pintar el area de la flecha, si es que hay más contenido que ver.
        self.image.fill(color, (self.text_rect.right + 1, 0, 16, self.draw_space_rect.h + 3))

        # dibujar el marco biselado.
        self.image.blit(self.marco, (0, 0))
