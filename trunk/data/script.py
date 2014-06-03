from globs.tiempo import Tiempo as T
from globs.world import World as W
from globs.giftgroups import MobGroup
i = 0

def run():
    W.RENDERER.camara.setFocus(None)
    if T._segs < 1:
        W.RENDERER.camara.paneolibre(1,0)
    elif T._segs < 2:
        W.RENDERER.camara.paneolibre(-1,0)
    elif T._segs < 3:
        W.RENDERER.camara.paneolibre(0,1)
    elif T._segs < 4:
        W.RENDERER.camara.paneolibre(0,-1)
    elif T._segs < 5:
        W.RENDERER.camara.paneolibre(1,1)
    elif T._segs < 6:
        W.RENDERER.camara.paneolibre(-1,-1)
    else:
        mob = MobGroup.get('commoner')
        W.RENDERER.camara.setFocus(mob)
    
