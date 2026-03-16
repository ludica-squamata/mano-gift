from engine.globs.event_dispatcher import EventDispatcher
from engine.libs.textrect import render_textrect
from pygame import Rect, Surface, draw, font
from engine.globs import CUADRO, Colores
from .base_widget import BaseWidget


class Boton(BaseWidget):
    img_pre = None
    img_dis = None

    comando_1 = None
    comando_2 = None
    pos = 0, 0

    timer = 0
    animar = False

    held = 0
    enable_holding = False

    def __init__(self, parent, nombre, ancho_mod, comando, pos, texto=None):
        self.tipo = 'boton'
        self.comando = None
        self.direcciones = {}
        self.nombre = nombre
        self.texto = texto
        self.ancho_mod = ancho_mod
        if self.texto is None:
            self.img_sel, self.img_pre, self.img_uns, self.img_dis = self.crear(self.nombre, ancho_mod)
        else:
            self.img_sel, self.img_pre, self.img_uns, self.img_dis = self.crear(self.texto, ancho_mod)
        self.pos = pos
        super().__init__(parent, imagen=self.img_uns)
        self.rect = self.img_sel.get_rect(topleft=self.pos)

        if type(comando) is list:
            self.comando_1, self.comando_2 = comando
        else:
            self.comando_1 = comando

        EventDispatcher.register(self.recolor, 'AlterColor')

    def rewrite(self):
        if self.texto is None:
            self.img_sel, self.img_pre, self.img_uns, self.img_dis = self.crear(self.nombre, self.ancho_mod)
        else:
            self.img_sel, self.img_pre, self.img_uns, self.img_dis = self.crear(self.texto, self.ancho_mod)

        if self.isSelected:
            self.image = self.img_sel
        else:
            self.image = self.img_uns

    def set_comando2(self, comando):
        self.comando_2 = comando

    def ser_presionado(self):
        self.animar = True

    def ser_deshabilitado(self):
        self.image = self.img_dis
        self.enabled = False

    def ser_habilitado(self):
        self.image = self.img_uns
        self.enabled = True

    def mantener_presion(self):
        self.held += 1
        if self.comando_2 is not None:
            self.comando_2()
        self.image = self.img_pre

    def liberar_presion(self):
        self.image = self.img_sel
        if self.enabled:
            if not self.enable_holding:
                self.comando_1()
            else:
                self.comando_2()

    def presionar(self, lt):
        if self.enabled:
            self.timer += 1
            if self.timer <= lt:
                self.image = self.img_pre

            elif lt + 1 <= self.timer <= lt * 2:
                self.image = self.img_sel

            elif self.timer == lt * 2 + 1:
                self.comando_1()

            else:
                self.timer = 0
                self.animar = False

    def crear(self, texto, ancho_mod):
        ancho = CUADRO * ancho_mod

        rect = Rect((-1, -1), (ancho - 6, CUADRO - 6))

        cnvs_pre = Surface((ancho + 6, CUADRO + 6))
        cnvs_pre.fill(Colores.CANVAS_BG)
        cnvs_sel = cnvs_pre.copy()
        cnvs_uns = cnvs_pre.copy()
        cnvs_dis = cnvs_pre.copy()

        fnd_pre = self.create_sunken_canvas(ancho, CUADRO)
        fnd_uns = self.create_raised_canvas(ancho, CUADRO)

        for i in range(round((ancho + 6) / 3)):
            # linea punteada horizontal superior
            draw.line(cnvs_sel, Colores.BOX_SEL_BACK, (i * 7, 0), ((i * 7) + 5, 0), 2)

            # linea punteada horizontal inferior
            draw.line(cnvs_sel, Colores.BOX_SEL_BACK, (i * 7, CUADRO + 4), ((i * 7) + 5, CUADRO + 4), 2)

        for i in range(round((CUADRO + 6) / 3)):
            # linea punteada vertical derecha
            draw.line(cnvs_sel, Colores.BOX_SEL_BACK, (0, i * 7), (0, (i * 7) + 5), 2)

            # linea punteada vertical izquierda
            draw.line(cnvs_sel, Colores.BOX_SEL_BACK, (ancho + 4, i * 7), (ancho + 4, (i * 7) + 5), 2)

        cnvs_sel.blit(fnd_uns, (3, 3))
        cnvs_uns.blit(fnd_uns, (3, 3))
        cnvs_dis.blit(fnd_uns, (3, 3))
        cnvs_pre.blit(fnd_pre, (3, 3))

        bold = font.Font('engine/libs/Verdanab.ttf', 16)
        fuente = font.Font('engine/libs/Verdana.ttf', 16)

        btn_sel = render_textrect(texto, bold, rect, Colores.TEXT_SEL, Colores.CANVAS_BG, 1)
        btn_uns = render_textrect(texto, fuente, rect, Colores.TEXT_FG, Colores.CANVAS_BG, 1)
        btn_dis = render_textrect(texto, fuente, rect, Colores.BISEL_BG, Colores.CANVAS_BG, 1)

        cnvs_uns.blit(btn_uns, (6, 6))
        cnvs_sel.blit(btn_sel, (6, 6))
        cnvs_pre.blit(btn_sel, (6, 6))
        cnvs_dis.blit(btn_dis, (6, 6))

        return cnvs_sel, cnvs_pre, cnvs_uns, cnvs_dis

    def __repr__(self):
        return self.nombre + ' _boton Sprite'

    def recolor(self, event):
        if event.data['name'] in ['CANVAS_BG', 'BOX_SEL_BACK', 'TEXT_SEL', 'TEXT_FG', 'BISEL_BG']:
            if self.texto is None:
                self.img_sel, self.img_pre, self.img_uns, self.img_dis = self.crear(self.nombre, self.ancho_mod)
            else:
                self.img_sel, self.img_pre, self.img_uns, self.img_dis = self.crear(self.texto, self.ancho_mod)

        if self.isSelected:
            self.image = self.img_sel
        else:
            self.image = self.img_uns

    def update(self):
        if self.animar:
            self.presionar(5)
