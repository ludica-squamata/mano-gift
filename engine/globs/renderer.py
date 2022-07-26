from engine.globs.event_dispatcher import EventDispatcher
from pygame import Rect, draw, display, image, mouse, font, sprite, Surface, SCALED
from engine.globs.azoe_group import AzoeGroup
from .constantes import ANCHO, ALTO, CAPA_OVERLAYS_DEBUG
from .tiempo import Tiempo
import sys
import os


class Camara:
    focus = None  # objeto que la camara sigue.
    bgs_rect = None  # el rect colectivo de los fondos
    bgs = AzoeGroup('bgs')  # el grupo de todos los fondos cargados    
    visible = AzoeGroup('visible')  # objetos que se ven (incluye sombras)
    real = AzoeGroup('real')  # objetos reales del mundo (no incluye sombras)
    nchs = AzoeGroup('noches')
    x, y = 0, 0
    w, h = ANCHO, ALTO
    rect = Rect(x, y, w, h)
    rect_pos = rect.copy()
    compass_CW = ['north', 'east', 'south', 'west']
    compass_CCW = ['north', 'west', 'south', 'east']
    view_name = 'north'

    current_map = None

    @classmethod
    def init(cls):
        EventDispatcher.register_many(
            (cls.save_focus, 'Save'),
            (cls.rotate_view, 'Rotate')
        )

    @classmethod
    def set_background(cls, spr):
        if cls.bgs_rect is None:
            cls.bgs_rect = spr.rect.copy()
        cls.bgs.add(spr)
        # cls.nchs.add(spr.noche)

    @classmethod
    def add_real(cls, obj):
        cls.real.add(obj)
        if obj not in cls.visible:
            cls.visible.add(obj, layer=obj.z)

    @classmethod
    def add_visible(cls, obj):
        if obj in cls.visible:
            cls.remove_obj(obj)
        cls.visible.add(obj, layer=obj.z)

    @classmethod
    def remove_obj(cls, obj):
        if obj in cls.real:
            cls.real.remove(obj)
        if obj in cls.visible:
            cls.visible.remove(obj)

    @classmethod
    def set_focus(cls, spr):
        cls.focus = spr

    @classmethod
    def save_focus(cls, event):
        EventDispatcher.trigger(event.tipo + 'Data', 'Camara', {'focus': cls.focus.nombre})

    @classmethod
    def is_focus(cls, spr):
        return cls.focus == spr

    @classmethod
    def get_current_map(cls):
        return cls.focus.stage

    @classmethod
    def clear(cls):
        cls.real.empty()
        cls.visible.empty()
        cls.bgs.empty()
        cls.bgs_rect = None
        cls.nchs.empty()

    @classmethod
    def rotate_view(cls, event):

        new_view = event.data['view']
        cw = cls.compass_CW.index(new_view)
        ccw = cls.compass_CCW.index(new_view)

        if cw < ccw:
            angle = -cw
        else:
            angle = ccw

        if cls.view_name != new_view:
            cls.view_name = new_view
            cls.compass_CW = [cls.compass_CW[cw]] + cls.compass_CW[cw + 1:] + cls.compass_CW[:cw]
            cls.compass_CCW = [cls.compass_CCW[ccw]] + cls.compass_CCW[ccw + 1:] + cls.compass_CCW[:ccw]

        EventDispatcher.trigger('RotateEverything', 'Camara', {'new_view': new_view, 'view': cw, 'angle': angle * 90})

    @classmethod
    def detectar_mapas_adyacentes(cls):
        map_at_center, map_at_bottom, map_at_right, map_at_top, map_at_left = [None] * 5
        r = cls.rect.inflate(5, 5)
        map_at = cls.bgs.get_spr_at
        adyacent_map_key = ''
        reference = None

        # shortcuts
        if len(cls.bgs):
            map_at_center = map_at(r.center)
            map_at_bottom = map_at(r.midbottom)
            map_at_right = map_at(r.midright)
            map_at_top = map_at(r.midtop)
            map_at_left = map_at(r.midleft)

        if map_at_center is not None:
            cls.current_map = map_at_center

        # check in ortogonal positions
        if map_at_top is None:
            adyacent_map_key = 'sup'
        elif map_at_bottom is None:
            adyacent_map_key = 'inf'
        elif map_at_left is None:
            adyacent_map_key = 'izq'
        elif map_at_right is None:
            adyacent_map_key = 'der'

        if adyacent_map_key == '':
            # check in diagonal positions
            if not map_at(r.topleft):
                if map_at_top:
                    reference = map_at_top
                    adyacent_map_key = 'izq'
                elif map_at_left:
                    reference = map_at_left
                    adyacent_map_key = 'sup'
            elif not map_at(r.topright):
                if map_at_top:
                    reference = map_at_top
                    adyacent_map_key = 'der'
                elif map_at_right:
                    reference = map_at_right
                    adyacent_map_key = 'sup'
            elif not map_at(r.bottomleft):
                if map_at_bottom:
                    reference = map_at_bottom
                    adyacent_map_key = 'izq'
                elif map_at_left:
                    reference = map_at_left
                    adyacent_map_key = 'inf'
            elif not map_at(r.bottomright):
                if map_at_bottom:
                    reference = map_at_bottom
                    adyacent_map_key = 'der'
                elif map_at_right:
                    reference = map_at_right
                    adyacent_map_key = 'inf'
        else:
            reference = map_at_center

        if adyacent_map_key != '' and reference is not None:
            new_map = reference.checkear_adyacencia(adyacent_map_key)
        else:
            new_map = cls.focus.parent

        if new_map is not False and new_map is not map_at_center:
            cls.set_background(new_map)
            for obj in new_map.properties.sprites() + new_map.parent.properties.sprites():
                if obj not in cls.real:
                    cls.add_real(obj)
                if hasattr(obj, 'luz') and obj.luz is not None:
                    cls.add_real(obj.luz)

        # a_map = map_at_center if map_at_center is not None else new_map
        # if cls.focus.mapa_actual != a_map:
        #     cls.focus.translocate(a_map, *cls.rect.center)

    @classmethod
    def update_sprites_layer(cls):
        for spr in cls.visible.sprs():
            cls.visible.change_layer(spr, spr.z)

    @classmethod
    def pan(cls):
        dx = cls.focus.rect.x - cls.focus.x - cls.focus.parent.rect.x
        dy = cls.focus.rect.y - cls.focus.y - cls.focus.parent.rect.y

        for spr in cls.bgs.sprs():
            spr.rect.move_ip(dx, dy)

        for spr in cls.real.sprs():
            x = spr.parent.rect.x + spr.x
            y = spr.parent.rect.y + spr.y
            spr.ubicar(x, y)

    @classmethod
    def update(cls, use_focus):
        cls.bgs.update()
        cls.real.update()
        cls.nchs.update()
        if use_focus:
            cls.detectar_mapas_adyacentes()
            cls.pan()

        cls.update_sprites_layer()

    @classmethod
    def draw(cls, fondo):
        ret = cls.bgs.draw(fondo)
        ret += cls.visible.draw(fondo)
        ret += cls.nchs.draw(fondo)
        if 'pydevd' in sys.modules:
            draw.line(fondo, (0, 100, 255), (cls.rect.centerx, 0), (cls.rect.centerx, cls.h))
            draw.line(fondo, (0, 100, 255), (0, cls.rect.centery), (cls.w, cls.rect.centery))
            for spr in cls.visible:
                draw.rect(fondo, (255, 0, 0), spr.rect, 1)
        return ret


class Renderer:
    use_focus = False
    camara = Camara()
    overlays = AzoeGroup('overlays')
    debug_text = None
    debug_pos = 0, 0

    @classmethod
    def init(cls, nombre, favicon):
        os.environ['SDL_VIDEO_CENTERED'] = "{!s},{!s}".format(0, 0)
        display.set_caption(nombre)
        display.set_icon(image.load(favicon))
        display.set_mode((ANCHO, ALTO), flags=SCALED, vsync=1)
        mouse.set_visible(False)
        cls.camara.init()

        EventDispatcher.register_many(
            (cls.get_debug_text, 'DEBUG'),
            (cls.clear, 'EndDialog', 'NewGame')
        )

    @classmethod
    def set_focus(cls, spr=None):
        if spr is not None:
            cls.camara.set_focus(spr)
            cls.use_focus = True
        else:
            cls.use_focus = False

    @classmethod
    def clear(cls, event=None, layer=None):
        if event is not None and 'layer' in event.data:
            layer = event.data['layer']
            cls.overlays.remove_sprites_of_layer(layer)
        elif layer:
            cls.overlays.remove_sprites_of_layer(layer)
        else:
            cls.camara.clear()

    @classmethod
    def add_overlay(cls, obj, _layer):
        cls.overlays.add(obj, layer=_layer)

    @classmethod
    def del_overlay(cls, obj):
        if obj in cls.overlays:
            cls.overlays.remove(obj)

    @classmethod
    def get_debug_text(cls, event):
        if 'debug' in sys.argv:
            cls.clear(layer=CAPA_OVERLAYS_DEBUG)
            spr = sprite.Sprite()
            fuente = font.SysFont('Verdana', 16)
            w = ANCHO - event.data['pos'][0]
            h = fuente.get_height()
            spr.image = Surface((w, h))
            spr.image.blit(fuente.render(event.data['text'], True, (255, 0, 0)), (0, 0))
            spr.rect = spr.image.get_rect(topleft=event.data['pos'])

            spr.active = True
            cls.add_overlay(spr, CAPA_OVERLAYS_DEBUG)

    @classmethod
    def update(cls):
        fondo = display.get_surface()
        fondo.fill((0, 0, 0))
        cls.camara.update(cls.use_focus)

        for over in cls.overlays.sprs():
            if over.active:
                over.update()
        ret = cls.camara.draw(fondo)
        clock = Tiempo.clock.render('red')
        ret += [fondo.blit(clock, [ANCHO - clock.get_width(), 0])]
        ret += cls.overlays.draw(fondo)

        display.update(ret)
