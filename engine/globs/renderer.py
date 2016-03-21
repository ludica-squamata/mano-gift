from pygame.sprite import LayeredUpdates
from pygame import Rect
from .constantes import Constants as Cs


class Camara:
    focus = None  # objeto que la camara sigue.
    bg = None  # el fondo
    bgs_rect = None  # el rect colectivo de los fondos
    bgs = LayeredUpdates()  # el grupo de todos los fondos cargados    
    visible = LayeredUpdates()  # objetos que se ven (incluye sombras)
    real = LayeredUpdates()  # objetos reales del mundo (no incluye sombras)
    x, y = 0, 0
    w, h = Cs.ANCHO, Cs.ALTO
    rect = Rect(x, y, w, h)

    @classmethod
    def set_background(cls, spr):
        if cls.bg is None:
            cls.bg = spr
            cls.bgs_rect = spr.rect.copy()
        cls.bgs.add(spr)

    @classmethod
    def add_real(cls, obj):
        cls.real.add(obj)
        if obj not in cls.visible:
            cls.visible.add(obj, layer=obj.z)

    @classmethod
    def add_visible(cls, obj):
        if obj not in cls.visible:
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
    def is_focus(cls, spr):
        if cls.focus is not None and hasattr(spr, 'nombre'):
            if cls.focus.nombre == spr.nombre:
                return True
        return False

    @classmethod
    def clear(cls):
        cls.real.empty()
        cls.visible.empty()
        cls.bgs.empty()
        cls.bg = None

    @classmethod
    def detectar_mapas_adyacentes(cls):
        r = cls.rect.inflate(2, 2)
        map_at = cls.bgs.get_sprites_at
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
            mapa = reference[0]
            new_map = mapa.checkear_adyacencia(adyacent_map_key)
            if new_map:
                cls.set_background(new_map)
                if adyacent_map_key == 'izq' or adyacent_map_key == 'der':
                    cls.bgs_rect.w += new_map.rect.w
                    if adyacent_map_key == 'izq':
                        cls.bgs_rect.x = new_map.rect.x
                elif adyacent_map_key == 'sup' or adyacent_map_key == 'inf':
                    cls.bgs_rect.h += new_map.rect.h
                    if adyacent_map_key == 'sup':
                        cls.bgs_rect.y = new_map.rect.y

    @classmethod
    def update_sprites_layer(cls):
        for spr in cls.visible:
            cls.visible.change_layer(spr, spr.z)

    @classmethod
    def panear(cls):
        new_x = cls.focus.rect.x - cls.focus.mapX
        new_y = cls.focus.rect.y - cls.focus.mapY

        dx = new_x - cls.bg.rect.x
        dy = new_y - cls.bg.rect.y

        f = cls.focus.rect
        b = cls.bgs_rect
        s = cls.rect

        if any([b.x + dx > 1, b.right + dx < s.w - 2, f.x != s.centerx]):
            dx = 0
        if any([b.y + dy > 2, b.bottom + dy < s.h - 2, f.y != s.centery]):
            dy = 0

        cls.bgs_rect.move_ip(dx, dy)
        for spr in cls.bgs:
            spr.rect.move_ip(dx, dy)

        for spr in cls.real:
            x = cls.bg.rect.x + spr.mapX
            y = cls.bg.rect.y + spr.mapY
            spr.ubicar(x, y, dy)

    @classmethod
    def update(cls, use_focus):
        cls.bgs.update()
        cls.visible.update()
        if use_focus:
            cls.detectar_mapas_adyacentes()
            cls.panear()

        cls.update_sprites_layer()

    @classmethod
    def draw(cls, fondo):
        ret = cls.bgs.draw(fondo)
        ret += cls.visible.draw(fondo)
        # draw.line(fondo,(0,100,255),(cls.rect.centerx,0),(cls.rect.centerx,cls.h))
        # draw.line(fondo,(0,100,255),(0,cls.rect.centery),(cls.w,cls.rect.centery))
        return ret


class Renderer:
    use_focus = False
    camara = Camara()
    overlays = LayeredUpdates()

    @classmethod
    def clear(cls):
        cls.camara.clear()
        cls.overlays.empty()

    @classmethod
    def add_overlay(cls, obj, _layer):
        cls.overlays.add(obj, layer=_layer)

    @classmethod
    def del_overlay(cls, obj):
        if obj in cls.overlays:
            cls.overlays.remove(obj)

    @classmethod
    def clear_overlays_from_layer(cls, layer):
        cls.overlays.remove_sprites_of_layer(layer)

    @classmethod
    def update(cls, fondo):
        fondo.fill((125, 125, 125))
        cls.camara.update(cls.use_focus)

        for over in cls.overlays:
            if over.active:
                over.update()
        ret = cls.camara.draw(fondo)
        ret += cls.overlays.draw(fondo)
        return ret
