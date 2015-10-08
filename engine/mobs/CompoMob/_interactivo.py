from engine.globs import EngineData as ED, MobGroup
from engine.base import _giftSprite
from pygame import mask, Rect, Surface
from pygame.sprite import Sprite

class Interactivo (_giftSprite):
    #el nombre no es del todo correcto, pero no existe palabra en castellano
    #para lo que sería un interactuante. Al menos, el dRAE dice que no existe.
    def __init__(self,*args,**kwargs):
        self._rect_h = Rect((0,0),(8*5,32))
        self._rect_v = Rect((0,0),(32,8*5))
        
        self._interaction_rect = None
        super().__init__(*args,**kwargs)
        
    def _orient_interaction_rect(self, x, y):
        """Orienta el rect de interacción. Función simplificada."""
        
        if x != 0:
            self._interaction_rect = self._rect_h.copy()
        if y != 0:
            self._interaction_rect = self._rect_v.copy()
        
        _rect = self.rect.copy()
        if x < 0:
            self._interaction_rect.right = _rect.centerx
        elif x > 0:
            self._interaction_rect.left = _rect.centerx
        else:
            self._interaction_rect.x = _rect.x
            
        if y < 0:
            self._interaction_rect.bottom = _rect.centery
        elif y > 0:
            self._interaction_rect.top = _rect.centery
        else:
            self._interaction_rect.y = _rect.y
    
    def _interact_with_props(self, x, y):
        """Selecciona a un prop utilizando el rect de interacción"""
        self._orient_interaction_rect(x, y)
        for prop in self.stage.interactives:
            if prop.image is not None:
                if self._interaction_rect.colliderect(prop.rect):
                    return prop
    
    def _interact_with_mobs(self, x, y):
        """Selecciona a un mob utilizando el rect de interacción"""
        self._orient_interaction_rect(x, y)
        for key in MobGroup:
            mob = MobGroup[key]
            if mob != self:
                if self._interaction_rect.colliderect(mob.rect):
                    return mob
