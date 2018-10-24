from .base_widget import BaseWidget
from engine.globs import CUADRO, TEXT_FG, BOX_SEL_BACK, TEXT_SEL, BISEL_BG, CANVAS_BG
from pygame import Rect, Surface, draw, font
from engine.libs.textrect import render_textrect


class Boton(BaseWidget):
    img_pre = None
    img_dis = None

    comando = None
    pos = 0, 0

    timer = 0
    animar = False

    def __init__(self, nombre, ancho_mod, comando, pos):
        self.tipo = 'boton'
        self.comando = None
        self.direcciones = {}
        self.nombre = nombre
        sel, pre, uns, dis = self.crear(nombre, ancho_mod)
        self.img_sel = sel
        self.img_pre = pre
        self.img_uns = uns
        self.img_dis = dis
        self.pos = pos
        super().__init__(self.img_uns)
        self.rect = self.img_sel.get_rect(topleft=self.pos)

        self.comando = comando

    def ser_presionado(self):
        self.animar = True

    def ser_deshabilitado(self):
        self.image = self.img_dis
        self.enabled = False

    def ser_habilitado(self):
        self.image = self.img_uns
        self.enabled = True

    def mantener_presion(self):
        self.image = self.img_pre

    def liberar_presion(self):
        self.image = self.img_sel
        self.comando()

    def presionar(self, lt):
        self.timer += 1
        if self.timer <= lt:
            self.image = self.img_pre

        elif lt + 1 <= self.timer <= lt * 2:
            self.image = self.img_sel

        elif self.timer == lt * 2 + 1:
            self.comando()

        else:
            self.timer = 0
            self.animar = False

    def crear(self, texto, ancho_mod):
        ancho = CUADRO * ancho_mod

        rect = Rect((-1, -1), (ancho - 6, CUADRO - 6))

        cnvs_pre = Surface((ancho + 6, CUADRO + 6))
        cnvs_pre.fill(CANVAS_BG)
        cnvs_sel = cnvs_pre.copy()
        cnvs_uns = cnvs_pre.copy()
        cnvs_dis = cnvs_pre.copy()

        fnd_pre = self.create_sunken_canvas(ancho, CUADRO)
        fnd_uns = self.create_raised_canvas(ancho, CUADRO)

        for i in range(round((ancho + 6) / 3)):
            # linea punteada horizontal superior
            draw.line(cnvs_sel, BOX_SEL_BACK, (i * 7, 0), ((i * 7) + 5, 0), 2)

            # linea punteada horizontal inferior
            draw.line(cnvs_sel, BOX_SEL_BACK, (i * 7, CUADRO + 4), ((i * 7) + 5, CUADRO + 4), 2)

        for i in range(round((CUADRO + 6) / 3)):
            # linea punteada vertical derecha
            draw.line(cnvs_sel, BOX_SEL_BACK, (0, i * 7), (0, (i * 7) + 5), 2)

            # linea punteada vertical izquierda
            draw.line(cnvs_sel, BOX_SEL_BACK, (ancho + 4, i * 7), (ancho + 4, (i * 7) + 5), 2)

        cnvs_sel.blit(fnd_uns, (3, 3))
        cnvs_uns.blit(fnd_uns, (3, 3))
        cnvs_dis.blit(fnd_uns, (3, 3))
        cnvs_pre.blit(fnd_pre, (3, 3))

        bold = font.Font('engine/libs/Verdanab.ttf', 16)
        fuente = font.Font('engine/libs/Verdana.ttf', 16)

        btn_sel = render_textrect(texto, bold, rect, TEXT_SEL, CANVAS_BG, 1)
        btn_uns = render_textrect(texto, fuente, rect, TEXT_FG, CANVAS_BG, 1)
        btn_dis = render_textrect(texto, fuente, rect, BISEL_BG, CANVAS_BG, 1)

        cnvs_uns.blit(btn_uns, (6, 6))
        cnvs_sel.blit(btn_sel, (6, 6))
        cnvs_pre.blit(btn_sel, (6, 6))
        cnvs_dis.blit(btn_dis, (6, 6))

        return cnvs_sel, cnvs_pre, cnvs_uns, cnvs_dis

    def __repr__(self):
        return self.nombre + ' _boton Sprite'

    def update(self):
        if self.animar:
            self.presionar(5)
