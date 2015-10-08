from pygame.sprite import LayeredUpdates
from pygame import Rect
from .constantes import Constants as Cs


class Renderer:
    camara = None
    overlays = None
    use_focus = False

    def __init__(self):
        self.camara = Camara(self)
        self.overlays = LayeredUpdates()

    def clear(self):
        self.camara.clear()
        self.overlays.empty()

    def add_overlay(self, obj, _layer):
        self.overlays.add(obj, layer = _layer)

    def del_overlay(self, obj):
        if obj in self.overlays:
            self.overlays.remove(obj)

    def update(self, fondo):
        fondo.fill((125, 125, 125))
        self.camara.update(self.use_focus)

        for over in self.overlays:
            if over.active:
                over.update()
        ret = self.camara.draw(fondo)
        ret += self.overlays.draw(fondo)
        return ret


class Camara:
    bg = None  # el fondo
    focus = None  # objeto que la camara sigue.
    visible = None  # objetos que se ven (incluye sombras)
    real = None  # objetos reales del mundo (no incluye sombras)
    x, y, w, h = 0, 0, 0, 0

    def __init__(self, parent):
        self.parent = parent
        self.visible = LayeredUpdates()
        self.real = LayeredUpdates()
        self.bgs = LayeredUpdates()
        self.w = Cs.ANCHO
        self.h = Cs.ALTO
        self.rect = Rect(self.x, self.y, self.w, self.h)

    def set_background(self, spr):
        if self.bg is None:
            self.bg = spr
        self.bgs.add(spr)

    def add_real(self, obj):
        self.real.add(obj)
        if obj not in self.visible:
            self.visible.add(obj, layer = obj.z)

    def add_visible(self, obj):
        if obj not in self.visible:
            self.visible.add(obj, layer = obj.z)

    def remove_obj(self, obj):
        if obj in self.real:
            self.real.remove(obj)
        if obj in self.visible:
            self.visible.remove(obj)

    def set_focus(self, spr):
        self.focus = spr

    def is_focus(self, spr):
        if self.focus is not None and hasattr(spr, 'nombre'):
            if self.focus.nombre == spr.nombre:
                return True
        return False

    def clear(self):
        self.real.empty()
        self.visible.empty()
        self.bgs.empty()
        self.bg = None

    def detectar_limites(self):

        # offx = self.bg.rect.w-self.rect.w
        # offy = self.bg.rect.h-self.rect.h
        # if any([self.bg.rect.x==0,self.bg.rect.x==offx]):
        #    print(self.bg.rect.x==0,self.bg.rect.x==offx)

        top, bottom, left, right = True, True, True, True
        _tl, _tr, _bl, _br = True, True, True, True
        map_at_top = True
        map_at_bottom = True
        map_at_left = True
        map_at_right = True
        map_at_topleft = True
        map_at_topright = True
        map_at_bottomleft = True
        map_at_bottomright = True

        if not len(self.bgs.get_sprites_at((1, 1))):
            _tl, map_at_topleft = False, False
        if not len(self.bgs.get_sprites_at((640, 1))):
            _tr, map_at_topright = False, False
        if not len(self.bgs.get_sprites_at((1, 480))):
            _bl, map_at_bottomleft = False, False
        if not len(self.bgs.get_sprites_at((640, 480))):
            _br, map_at_bottomright = False, False

        if not _tl and not _tr:
            map_at_top = False
        if not _bl and not _br:
            map_at_bottom = False
        if not _tl and not _bl:
            map_at_left = False
        if not _tr and not _br:
            map_at_right = False

        adyacent_map_keys = []
        if not map_at_top:
            adyacent_map_keys.append('sup')
        if not map_at_bottom:
            adyacent_map_keys.append('inf')
        if not map_at_left:
            adyacent_map_keys.append('izq')
        if not map_at_right:
            adyacent_map_keys.append('der')
        if not map_at_topleft:
            adyacent_map_keys.append('supizq')
        if not map_at_topright:
            adyacent_map_keys.append('supder')
        if not map_at_bottomleft:
            adyacent_map_keys.append('infizq')
        if not map_at_bottomright:
            adyacent_map_keys.append('infder')

        self.bg.checkear_adyacencias(adyacent_map_keys)  # bool
        if 'sup' in adyacent_map_keys:
            top = True
        if 'inf' in adyacent_map_keys:
            bottom = True
        if 'izq' in adyacent_map_keys:
            left = True
        if 'der' in adyacent_map_keys:
            right = True

        new_x = self.focus.rect.x - self.focus.mapX
        new_y = self.focus.rect.y - self.focus.mapY

        dx = new_x - self.bg.rect.x
        dy = new_y - self.bg.rect.y

        if not left or not right:
            dx = 0  # descomentar para restringir
        if not top or not bottom:
            dy = 0  # el movimiento fuera de borde

        return dx, dy

    def update_sprites_layer(self):
        for spr in self.visible:
            self.visible.change_layer(spr, spr.z)

    def panear(self, dx, dy):
        self.bg.rect.x += dx
        self.bg.rect.y += dy

        for spr in self.bgs:
            if spr != self.bg:
                x = self.bg.rect.x + spr.offsetX
                y = self.bg.rect.y + spr.offsetY
                spr.ubicar(x, y)

        for spr in self.real:
            x = self.bg.rect.x + spr.mapX
            y = self.bg.rect.y + spr.mapY
            spr.ubicar(x, y, dy)

    def update(self, use_focus):
        self.bgs.update()
        self.visible.update()
        if use_focus:
            dx, dy = self.detectar_limites()

            if dx or dy:
                self.panear(dx, dy)
            else:
                x = self.bg.rect.x + self.focus.mapX
                y = self.bg.rect.y + self.focus.mapY
                self.focus.ubicar(x, y, dy)

        self.update_sprites_layer()

    def draw(self, fondo):
        ret = self.bgs.draw(fondo)
        ret += self.visible.draw(fondo)
        # draw.line(fondo,(0,100,255),(self.rect.centerx,0),(self.rect.centerx,self.h))
        # draw.line(fondo,(0,100,255),(0,self.rect.centery),(self.w,self.rect.centery))
        return ret
