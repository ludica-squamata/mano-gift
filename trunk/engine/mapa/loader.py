from engine.globs import EngineData as ED, Constants as C, MobGroup
from engine.misc import Resources as r
from engine.mobs import NPC, PC
from engine.quests import QuestManager
from . import Prop, Salida

class _loader:
    STAGE = None
    
    @staticmethod
    def setStage(stage):
        _loader.STAGE = stage
    
    @staticmethod
    def loadEverything(entrada):
        _loader.cargar_hero(entrada)
        _loader.cargar_props('ground')
        _loader.cargar_props('top')
        _loader.cargar_mobs(NPC)
        _loader.cargar_quests()
        _loader.cargar_salidas()
        
    @staticmethod
    def cargar_props (capa):
        imgs = _loader.STAGE.data['refs']
        POS = _loader.STAGE.data['capa_'+capa]['props']
        data = r.abrir_json('data/scripts/props.json')
        if capa == 'ground':
            layer = C.CAPA_GROUND_ITEMS
        elif capa == 'top':
            layer = C.CAPA_TOP_ITEMS
        
        for ref in POS:
            for x,y in POS[ref]:
                if ref in data:
                    if 'image' in data[ref]:
                        imagen = data[ref]['image']
                    else:
                        imagen = imgs[ref]
                    
                    prop = Prop(ref,imagen,_loader.STAGE,x,y,data[ref])
                else:
                    prop = Prop(ref,imgs[ref],stage=_loader.STAGE,x=x,y=y)
                _loader.STAGE.addProperty(prop,layer)
                if prop.sombra != None:
                    _loader.STAGE.mapa.image.blit(prop.sombra,[x*C.CUADRO,y*C.CUADRO])
    
    @staticmethod
    def cargar_mobs(clase):
        #if clase == Enemy:
        #    pos = _loader.STAGE.data['capa_ground']['mobs']['enemies']
        #    act = 'agressive'
        if clase == NPC:
            pos = _loader.STAGE.data['capa_ground']['mobs']['npcs']
            act = 'passive'
        imgs = _loader.STAGE.data['refs']

        for ref in pos:
            base = r.abrir_json('data/mobs/'+act+'.mob')
            try:
                data = r.abrir_json('data/mobs/'+ref+'.mob')
            except IOError:
                data = {}
            base.update(data)
            for x,y in pos[ref]:
                mob = clase(ref,imgs[ref],_loader.STAGE,x,y,base)
                _loader.STAGE.addProperty(mob,C.CAPA_GROUND_MOBS)
                MobGroup.add(mob)
    
    @staticmethod
    def cargar_hero(entrada = None):
        ED.HERO = PC('heroe',r.abrir_json('data/mobs/hero.mob'),_loader.STAGE)
        if entrada != None:
            if entrada in _loader.STAGE.data['entradas']:
                x,y = _loader.STAGE.data['entradas'][entrada]
                ED.HERO.ubicar(x*C.CUADRO, y*C.CUADRO)
                _loader.STAGE.addProperty(ED.HERO,C.CAPA_HERO)
    
    @staticmethod
    def cargar_quests():
        if 'quests' in _loader.STAGE.data:
            for quest in _loader.STAGE.data['quests']:
                QuestManager.add(quest)
    
    @staticmethod  
    def cargar_salidas():
        salidas = _loader.STAGE.data['salidas']
        for salida in salidas:
            sld = Salida(salidas[salida])
            _loader.STAGE.properties.add(sld,layer=C.CAPA_GROUND_SALIDAS)