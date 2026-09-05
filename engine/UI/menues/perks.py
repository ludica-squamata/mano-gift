from engine.globs.event_dispatcher import EventDispatcher
from engine.libs.textrect import render_textrect
from engine.misc.resources import cargar_imagen
from engine.globs.azoe_group import AzoeGroup
from engine.globs import ModData,Colores
from pygame import Rect, Surface, font
from pygame.sprite import Sprite
from csv import DictReader
from .menu import Menu
from random import choice


class PerksMenu(Menu):

    px, py = 0, 128

    def __init__(self, parent):
        super().__init__(parent,'Perks','Perks')
        self.images = AzoeGroup('Imagenes')
        self.perk_descrip_area = self.create_sunken_canvas(self.w, 125)
        self.perk_descrip_rect = self.perk_descrip_area.get_rect(x=0, bottom=self.h)
        self.image.blit(self.perk_descrip_area,self.perk_descrip_rect)
        self.perks = PerksImage(self)
        self.area_rect = Rect(3,self.h-128, self.w-7, self.h)
        self.right = self.w-3
        self.marco = self.crear_marco(self.w, self.h)
        self.perks_area = Rect(3, 32, 617, 300)

        self.functions['tap'].update({'arriba':lambda: self.select_adjacent('arriba'),
                                      'abajo':lambda: self.select_adjacent('abajo'),
                                      'izquierda':lambda: self.select_adjacent('izquierda'),
                                      'derecha':lambda: self.select_adjacent('derecha')
                                      })
        self.functions['hold'].update({'arriba':lambda: self.scroll_image('arriba'),
                                      'abajo':lambda: self.scroll_image('abajo'),
                                      'izquierda':lambda: self.scroll_image('izquierda'),
                                      'derecha':lambda: self.scroll_image('derecha')
                                      })

    def scroll_image(self, key):
        x, y = 0, 0

        if key == 'arriba':
            y = +3
        elif key == 'abajo':
            y = -3
        if key == 'derecha':
            x =-3
        elif key == 'izquierda':
            x = +3

        rect = self.perks.rect
        if rect.top + y <= 30 and rect.bottom + y >= 332 and rect.left + x <=3 and rect.right + x >=610:
            self.perks.scroll(dx=x, dy=y)

    def update(self, *args, **kwargs):
        self.image.fill(Colores.CANVAS_BG,[0,0,self.w,32])
        self.images.draw(self.image)
        self.image.blit(self.perk_descrip_area, self.perk_descrip_rect)
        selected = self.perks.selected
        if selected is not None:
            self.image.blit(selected.text, selected.text_rect)
        self.crear_titulo(self.nombre)

    def select_adjacent(self, direccion):
        if self.perks.selected is None:
            self.perks.select_one(0)
        else:
            self.perks.selected.select_adjacent(direccion)



class PerksImage(Sprite):
    selected = None

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.perks = []
        self.img_fnd = cargar_imagen(ModData.graphs + 'gameplay/arbol - Fondo.png')
        self.img_neu = cargar_imagen(ModData.graphs + 'gameplay/arbol - Neutral.png')
        self.img_sel = cargar_imagen(ModData.graphs + 'gameplay/arbol - Seleccion.png')
        self.img_adq = cargar_imagen(ModData.graphs + 'gameplay/arbol - Adquirido.png')

        self.image = self.img_fnd
        self.rect = self.image.get_rect(bottom=self.parent.h-128, x=3)
        self.parent.px, self.parent.py = self.rect.topleft
        self.parent.images.add(self)

        with open(ModData.game_fd+'/perk_grid_tilled.csv') as file:
            reader = DictReader(file,delimiter=';')
            rows = list(reader)
            for row in rows:
                id = int(row['id'])
                nombre = row['nombre']
                ar = int(row['arriba']) if row['arriba'] != 'null' else None
                ab = int(row['abajo']) if row['abajo'] != 'null' else None
                iz = int(row['izquierda']) if row['izquierda'] != 'null' else None
                de = int(row['derecha']) if row['derecha'] != 'null' else None
                des = row['notes']

                rect = Rect([int(i) for i in row['rect'].split(',')])
                img_uns = self.img_neu.subsurface(rect).copy()
                img_sel = self.img_sel.subsurface(rect).copy()
                img_adq = self.img_adq.subsurface(rect).copy()

                spr = IndividualPerk(self,id,nombre, img_uns, img_sel,img_adq,[ar,ab,iz,de],
                                     rect.move(self.rect.x, self.rect.y).copy(),des)
                self.perks.append(spr)
                spr.show()

    def scroll(self, dx=0, dy=0):

        self.rect.x += dx
        self.rect.y += dy

        for perk in self.perks:
            perk.rect.x += dx
            perk.rect.y += dy

    def deselect_all(self):
        self.selected = None
        for perk in self.perks:
            perk.deselect()

    def select_one(self, the_one):
        selected = self.perks[the_one]
        if not self.parent.perks_area.contains(selected.rect):
            dx = 0
            dy = 0

            if selected.rect.left < self.parent.perks_area.left:
                dx = -(selected.rect.left - self.parent.perks_area.left)

            elif selected.rect.right > self.parent.perks_area.right:
                dx = -(selected.rect.right - self.parent.perks_area.right)

            if selected.rect.top < self.parent.perks_area.top:
                dy = -(selected.rect.top - self.parent.perks_area.top)

            elif selected.rect.bottom > self.parent.perks_area.bottom:
                dy = -(selected.rect.bottom - self.parent.perks_area.bottom)

            self.scroll(dx=dx, dy=dy)
        selected.select()
        self.selected = selected


class IndividualPerk(Sprite):
    selected = False
    text = None
    text_rect = None

    def __init__(self, parent, id, nombre, img_uns, img_sel, img_adq, direcciones, rect, text):
        super().__init__()
        self.parent = parent
        self.nombre = nombre
        self.img_uns = img_uns
        self.img_sel = img_sel
        self.img_adq = img_adq
        self.image = self.img_uns
        self.rect = rect

        self._base_text = text
        self.render_text()
        EventDispatcher.register(self.recolor,'AlterColor')

        self.direcciones = dict(zip(['arriba','abajo','izquierda','derecha'],direcciones))
        self.id = id

    def render_text(self):
        text = self._base_text
        fuente = font.Font('engine/libs/Verdana.ttf', 14)
        text_rect = self.parent.parent.perk_descrip_rect.inflate(-6, -6)
        render = render_textrect(text, fuente, text_rect, Colores.TEXT_FG, Colores.CANVAS_BG)
        x, y = self.parent.parent.perk_descrip_rect.topleft
        self.text, self.text_rect = render, render.get_rect(x=x + 3, y=y + 3)

    def show(self):
        self.parent.parent.images.add(self)

    def hide(self):
        self.parent.parent.images.remove(self)

    def select(self):
        self.selected = True
        self.image = self.img_sel

    def deselect(self):
        self.selected = False
        self.image = self.img_uns

    def adquire(self):
        self.image = self.img_adq

    def select_adjacent(self, direccion):
        if self.direcciones[direccion] is not None:
            the_one = self.direcciones[direccion]
            self.parent.deselect_all()
            self.parent.select_one(the_one)

    def __repr__(self):
        return f'Perk #{str(self.id)} ({self.nombre})'

    def recolor(self, event):
        if event.data['name'] in ['CANVAS_BG', 'TEXT_FG']:
            self.render_text()
