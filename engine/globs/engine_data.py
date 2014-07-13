from .renderer import Renderer

class EngineData:
    MAPA_ACTUAL = ''
    HERO = ''
    menu_actual = ''
    menu_previo = ''
    MENUS = {}
    DIALOG = None
    MODO = ''
    onPause = False
    RENDERER = Renderer()
    HUD = None
    
    def setear_mapa(mapa, entrada):
        ED = EngineData
        ED.MODO = 'Aventura'
        from engine.mapa import Stage
        ED.MAPA_ACTUAL = Stage(mapa,entrada)
        ED.RENDERER.setBackground(ED.MAPA_ACTUAL.mapa)
        for obj in ED.MAPA_ACTUAL.properties:
            ED.RENDERER.addObj(obj,obj.rect.bottom)
        ED.RENDERER.camara.centrar()