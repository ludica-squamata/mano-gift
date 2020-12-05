from engine.globs.event_dispatcher import EventDispatcher
from pygame import Rect, draw, display, image, mouse, font, sprite, Surface, SCALED as PYGAME_SCALED
from engine.globs.azoe_group import AzoeGroup
from .constantes import ANCHO, ALTO, CAPA_OVERLAYS_DEBUG
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
        cls.nchs.add(spr.noche)

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
        r = cls.rect.inflate(5, 5)
        map_at = cls.bgs.get_spr_at
        adyacent_map_key = ''
        reference = []

        # shortcuts
        map_at_center = map_at(r.center)
        map_at_bottom = map_at(r.midbottom)
        map_at_right = map_at(r.midright)
        map_at_top = map_at(r.midtop)
        map_at_left = map_at(r.midleft)

        # check in ortogonal positions
        if not map_at_top:
            adyacent_map_key = 'sup'
        elif not map_at_bottom:
            adyacent_map_key = 'inf'
        if not map_at_left:
            adyacent_map_key = 'izq'
        elif not map_at_right:
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

        if adyacent_map_key != '' and len(reference):
            new_map = reference[0].checkear_adyacencia(adyacent_map_key)
        else:
            new_map = cls.focus.stage

        if new_map is not False and new_map not in map_at_center:
            cls.set_background(new_map)
            for obj in new_map.properties.sprites():
                if obj not in cls.real:
                    cls.add_real(obj)

            if adyacent_map_key == 'izq' or adyacent_map_key == 'der':
                cls.bgs_rect.w += new_map.rect.w
                if adyacent_map_key == 'izq':
                    cls.bgs_rect.x = new_map.rect.x
            elif adyacent_map_key == 'sup' or adyacent_map_key == 'inf':
                cls.bgs_rect.h += new_map.rect.h
                if adyacent_map_key == 'sup':
                    cls.bgs_rect.y = new_map.rect.y

        a_map = map_at_center[0] if len(map_at_center) else new_map
        if cls.focus.mapa_actual != a_map:
            cls.focus.translocate(a_map, *cls.rect.center)

    @classmethod
    def update_sprites_layer(cls):
        for spr in cls.visible.sprs():
            cls.visible.change_layer(spr, spr.z)

    @classmethod
    def panear(cls):
        dx = cls.focus.rect.x - cls.focus.mapRect.x - cls.focus.stage.rect.x
        dy = cls.focus.rect.y - cls.focus.mapRect.y - cls.focus.stage.rect.y

        abs_x, abs_y = abs(dx), abs(dy)
        sign_x, sign_y = 0, 0
        # Extraer el signo + o -
        if dx:
            sign_x = int(dx / abs_x)  # +1 ó -1
        if dy:
            sign_y = int(dy / abs_y)  # +1 ó -1

        while abs_x:
            # acá restauramos el valor para hacer la comparación
            dx = abs_x * sign_x
            if cls.focus.rect.centerx + dx != cls.rect.centerx:
                # y acá achicamos el valor por si es muy alto
                # no importa que sea negativo o positivo, porque eso
                # lo preserva el sign.
                abs_x -= 1
            else:
                break

        while abs_y:
            dy = abs_y * sign_y
            if cls.focus.rect.centery + dy != cls.rect.centery:
                abs_y -= 1
            else:
                break

        cls.pan(dx, dy)

    @classmethod
    def pan(cls, dx, dy):
        cls.bgs_rect.move_ip(dx, dy)
        for spr in cls.bgs.sprs():
            spr.rect.move_ip(dx, dy)

        for spr in cls.real.sprs():
            x = spr.stage.rect.x + spr.mapRect.x
            y = spr.stage.rect.y + spr.mapRect.y
            spr.ubicar(x, y)

    @classmethod
    def cut(cls, x, y):
        cls.bgs_rect.topleft = x, y
        for spr in cls.bgs:
            spr.rect.topleft = x, y

        for spr in cls.real.sprs():
            x = spr.stage.rect.x + spr.mapRect.x
            y = spr.stage.rect.y + spr.mapRect.y
            spr.ubicar(x, y)

    @classmethod
    def update(cls, use_focus):
        cls.bgs.update()
        cls.real.update()
        cls.nchs.update()
        if use_focus:
            cls.detectar_mapas_adyacentes()
            cls.panear()

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
        display.set_mode((ANCHO, ALTO), PYGAME_SCALED)
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
        ret += cls.overlays.draw(fondo)

        display.update(ret)
