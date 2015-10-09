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
        self.bgs_rect = Rect(0,0,0,0)
        self.w = Cs.ANCHO
        self.h = Cs.ALTO
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.cam_rect = Rect(0,0,self.w,self.h)

    def set_background(self, spr):
        if self.bg is None:
            self.bg = spr
            self.cam_rect.topleft = spr.rect.topleft
        self.bgs.add(spr)
        self.bgs_rect.union_ip(spr.rect)


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

        offx = self.rect.w-self.bgs_rect.w
        offy = self.bgs_rect.h-self.rect.h
        #print(self.cam_rect)




        # map_at_topleft = True
        # map_at_topright = True
        # map_at_bottomleft = True
        # map_at_bottomright = True
        #
        # if not len(self.bgs.get_sprites_at((0, 0))):
        #     map_at_topleft = False
        # if not len(self.bgs.get_sprites_at((640, 0))):
        #     map_at_topright = False
        # if not len(self.bgs.get_sprites_at((0, 480))):
        #     map_at_bottomleft = False
        # if not len(self.bgs.get_sprites_at((640, 480))):
        #     map_at_bottomright = False

        map_at_bottom = bool(len(self.bgs.get_sprites_at((320, 480))))
        map_at_right = bool(len(self.bgs.get_sprites_at((640, 240))))
        map_at_top = bool(len(self.bgs.get_sprites_at((320, 0))))
        map_at_left = bool(len(self.bgs.get_sprites_at((0, 240))))

        adyacent_map_keys = []
        if not map_at_top:
            adyacent_map_keys.append('sup')
        if not map_at_bottom:
            adyacent_map_keys.append('inf')
        if not map_at_left:
            adyacent_map_keys.append('izq')
        if not map_at_right:
            adyacent_map_keys.append('der')
        # if not map_at_topleft:
        #     adyacent_map_keys.append('supizq')
        # if not map_at_topright:
        #     adyacent_map_keys.append('supder')
        # if not map_at_bottomleft:
        #     adyacent_map_keys.append('infizq')
        # if not map_at_bottomright:
        #     adyacent_map_keys.append('infder')
        mapas = self.bgs.get_sprites_at((320, 240))
        if len(mapas):
            mapa = mapas[0]
            mapa.checkear_adyacencias(adyacent_map_keys)

        new_x = self.focus.rect.x - self.focus.mapX
        new_y = self.focus.rect.y - self.focus.mapY

        dx = new_x - self.bg.rect.x
        dy = new_y - self.bg.rect.y

        return dx, dy

    def update_sprites_layer(self):
        for spr in self.visible:
            self.visible.change_layer(spr, spr.z)

    def panear(self, dx, dy):
        self.cam_rect.move_ip(dx,dy)
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
