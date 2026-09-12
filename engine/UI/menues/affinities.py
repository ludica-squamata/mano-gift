from pygame import Color, Surface, SRCALPHA, draw, font
from engine.globs import ModData, Colores, Mob_Group
from engine.misc.resources import cargar_imagen
from engine.globs.azoe_group import AzoeGroup
import xml.etree.ElementTree as eT
from pygame.sprite import Sprite
from .menu import Menu

class AffinitiesMenu(Menu):

    # noinspection unresolved-references
    def __init__(self, parent):
        super().__init__(parent, 'Afinidades de Mana', 'Affinties')
        self.bg_img = cargar_imagen(ModData.game_fd + '/magic_affinitiesv4_blank.png')
        self.bg_rect = self.bg_img.get_rect(centerx=self.rect.centerx-12, centery=self.rect.centery)

        self.character = Mob_Group.get_controlled_mob() # issue #122 Alternar el control entre diferentes mobs

        self.fuente1 = font.Font('engine/libs/Verdanab.ttf', 20)
        self.fuente2 = font.Font('engine/libs/Verdana.ttf', 14)
        self.affinity_layers = {}
        self.circles = AzoeGroup('Imagenes')
        self.current = 9
        viewBox = float("86.3302"),float("59.3033")
        scale_x = 358 / viewBox[0]
        scale_y = 239 / viewBox[1]
        idx = -1
        with open(ModData.game_fd+'/affinities3.svg','r') as file:
            for line in file:
                if "circle" in line:
                    idx += 1
                    element = eT.fromstring(line)
                    circle_dict = element.attrib
                    x = float(circle_dict['cx'])*scale_x+127
                    y = float(circle_dict['cy'])*scale_y+118
                    fg = Color(circle_dict['fill'])
                    st = Color(circle_dict['stroke'])
                    radius = 5
                    if 50 <= idx <= 59:
                        self.affinity_layers['rojo'] = layer = 0
                    elif 40 <= idx <= 49:
                        self.affinity_layers['verde'] = layer = 1
                    elif 30 <= idx <= 39:
                        self.affinity_layers['azul'] = layer = 2
                    elif 20 <= idx <= 29:
                        self.affinity_layers['cian'] = layer = 3
                    elif 10 <= idx <= 19:
                        self.affinity_layers['magenta'] = layer = 4
                    elif 0 <= idx <= 9:
                        self.affinity_layers['amarillo'] = layer = 5

                    circle = AffinityCircle(self,x, y, fg, st, radius)
                    self.circles.add(circle, layer=layer)

        for affinity in self.character.afinidades:
            layer = self.affinity_layers[affinity]
            aff = self.character.afinidades[affinity]
            for _ in range(aff.value):
                self.turn_on(layer)


    def turn_on(self,layer):
        circles = self.circles.get_sprites_from_layer(layer)
        if 0 <= self.current < len(circles):
            circle = circles[self.current]
            circle.visible = True
            self.current -= 1
        else:
            self.current = 0

    # noinspection unresolved-references
    def render_character_name(self):
        fg, bg = Colores.TEXT_FG, Colores.CANVAS_BG
        rect = self.image.blit(self.fuente1.render('Character', True, fg, bg), [3, 32])
        character = self.fuente2.render(self.character['nombre'], True, fg, bg)
        char_rect = character.get_rect(top=rect.bottom,centerx=rect.centerx)
        self.image.blit(character, char_rect)

    # noinspection unresolved-references
    def update(self, *args, **kwargs):
        self.image.fill(Colores.CANVAS_BG)
        self.image.blit(self.bg_img, self.bg_rect)
        for circle in self.circles.sprs():
            if circle.visible:
                self.image.blit(circle.image,circle.rect)
        self.crear_titulo(self.nombre)
        self.render_character_name()


class AffinityCircle(Sprite):
    def __init__(self, parent, x, y, color, stroke, radius):
        super().__init__()
        self.parent = parent
        self.image = Surface([(radius*2)-1,(radius*2)-1])
        draw.circle(self.image,color,[radius, radius],radius)
        draw.circle(self.image,stroke,[radius, radius],radius+1,width=1)
        # noinspection unresolved-references
        self.rect = self.image.get_rect(center=[x, y])
        self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False
