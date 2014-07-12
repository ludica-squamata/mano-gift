from engine.globs import EngineData as ED, Constants as C, MobGroup, ModData as MD
from engine.misc import Resources as r
from engine.mobs import NPC, PC
from engine.quests import QuestManager
from engine.scenery import newProp
from .salida import Salida

class _loader:
    STAGE = None
    
    @staticmethod
    def setStage(stage):
        _loader.STAGE = stage
    
    @staticmethod
    def loadEverything(entrada):
        _loader.cargar_hero(entrada)
        _loader.cargar_props()
        #_loader.cargar_props('top')
        _loader.cargar_mobs(NPC)
        _loader.cargar_quests()
        _loader.cargar_salidas()
        
    @staticmethod
    def cargar_props ():
        imgs = _loader.STAGE.data['refs']
        POS = _loader.STAGE.data['capa_ground']['props']
        props = r.abrir_json(MD.scripts+'props.json')
        
        for ref in POS:
            for x,y in POS[ref]:
                if ref in props:
                    prop = newProp(ref,props[ref]['image'],x,y,props[ref])
                else:
                    prop = newProp(ref,imgs[ref],x,y)

                _loader.STAGE.addProperty(prop,C.CAPA_GROUND_ITEMS)
    
    @staticmethod
    def cargar_mobs(clase):
        #if clase == Enemy:
        #    pos = _loader.STAGE.data['capa_ground']['mobs']['enemies']
        #    act = 'agressive'
        if clase == NPC:
            pos = _loader.STAGE.data['capa_ground']['mobs']['npcs']
            act = 'passive'

        for ref in pos:
            base = r.abrir_json(MD.mobs+act+'.mob')
            try:
                data = r.abrir_json(MD.mobs+ref+'.mob')
            except IOError:
                data = {}
            base.update(data)
            for x,y in pos[ref]:
                mob = clase(ref,data['imagen'],_loader.STAGE,x,y,base)
                _loader.STAGE.addProperty(mob,C.CAPA_GROUND_MOBS)
    
    @staticmethod
    def cargar_hero(entrada):
        #if entrada != None and entrada in _loader.STAGE.data['entradas']:
        #no hace falta si no va a haber un mensaje de error en caso contrario.
        x,y = _loader.STAGE.data['entradas'][entrada]
        ED.HERO = PC(r.abrir_json(MD.mobs+'hero.mob'),_loader.STAGE,x,y)
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