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
    bgs = None  # el grupo de todos los fondos cargados
    bgs_rect = None  # el rect colectivo de los fondos
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
            self.bgs_rect = spr.rect.copy()
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

    def detectar_mapas_adyacentes(self):
        r = self.rect.inflate(2,2)
        map_at = self.bgs.get_sprites_at
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
                self.set_background(new_map)
                if adyacent_map_key == 'izq' or adyacent_map_key == 'der':
                    self.bgs_rect.w += new_map.rect.w
                    if adyacent_map_key == 'izq':
                        self.bgs_rect.x = new_map.rect.x
                elif adyacent_map_key == 'sup' or adyacent_map_key == 'inf':
                    self.bgs_rect.h += new_map.rect.h
                    if adyacent_map_key == 'sup':
                        self.bgs_rect.y = new_map.rect.y
    
    def update_sprites_layer(self):
        for spr in self.visible:
            self.visible.change_layer(spr, spr.z)

    def panear(self):
        new_x = self.focus.rect.x - self.focus.mapX
        new_y = self.focus.rect.y - self.focus.mapY

        dx = new_x - self.bg.rect.x
        dy = new_y - self.bg.rect.y
        
        f = self.focus.rect
        b = self.bgs_rect
        s = self.rect
        
        if any([b.x+dx > 1, b.right+dx < s.w-2, f.x != s.centerx]):
            dx = 0
        if any([b.y+dy > 2, b.bottom+dy < s.h-2, f.y != s.centery]):
            dy = 0
        
        self.bgs_rect.move_ip(dx, dy)
        for spr in self.bgs:
            spr.rect.move_ip(dx, dy)

        for spr in self.real:
            x = self.bg.rect.x + spr.mapX
            y = self.bg.rect.y + spr.mapY
            spr.ubicar(x, y, dy)

    def update(self, use_focus):
        self.bgs.update()
        self.visible.update()
        if use_focus:
            self.detectar_mapas_adyacentes()
            self.panear()

        self.update_sprites_layer()

    def draw(self, fondo):
        ret = self.bgs.draw(fondo)
        ret += self.visible.draw(fondo)
        # draw.line(fondo,(0,100,255),(self.rect.centerx,0),(self.rect.centerx,self.h))
        # draw.line(fondo,(0,100,255),(0,self.rect.centery),(self.w,self.rect.centery))
        return ret
