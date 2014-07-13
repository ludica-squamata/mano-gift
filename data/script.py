from engine.globs import Tiempo as T, EngineData as ED, MobGroup

def run():
    ED.RENDERER.camara.setFocus(None)
    if T._segs < 1:
        ED.RENDERER.camara.paneolibre(1,0)
    elif T._segs < 2:
        ED.RENDERER.camara.paneolibre(-1,0)
    elif T._segs < 3:
        ED.RENDERER.camara.paneolibre(0,1)
    elif T._segs < 4:
        ED.RENDERER.camara.paneolibre(0,-1)
    elif T._segs < 5:
        ED.RENDERER.camara.paneolibre(1,1)
    elif T._segs < 6:
        ED.RENDERER.camara.paneolibre(-1,-1)
    else:
        mob = MobGroup.get('commoner')
        ED.RENDERER.camara.setFocus(mob)
    
