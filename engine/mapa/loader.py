from engine.globs import EngineData as ED, Constants as C, MobGroup, ModData as MD
from engine.misc import Resources as r
from engine.mobs import NPCSocial, PC
from engine.quests import QuestManager
from engine.scenery import newProp
from .salida import Salida

class _loader:
    STAGE = None
    
    @staticmethod
    def setStage(stage):
        _loader.STAGE = stage
    
    @staticmethod
    def loadEverything(entrada,mobs_data):
        _loader.cargar_hero(entrada)
        _loader.cargar_props()
        #_loader.cargar_props('top')
        _loader.cargar_mobs(mobs_data)
        _loader.cargar_quests()
        _loader.cargar_salidas()
        _loader.cargar_limites()
        
    @staticmethod
    def cargar_props ():
        imgs = _loader.STAGE.data['refs']
        POS = _loader.STAGE.data['capa_ground']['props']
        
        for ref in POS:
            try:
                data = r.abrir_json(MD.items+ref+'.item')
                imagen = r.cargar_imagen(data['image'])
            except IOError:
                data = False
                imagen = r.cargar_imagen(imgs[ref])
            
            
            for x,y in POS[ref]:
                if data:
                    prop = newProp(ref,imagen,x,y,data)
                    addInteractive = True
                else:
                    prop = newProp(ref,imagen,x,y)
                    addInteractive = False

                _loader.STAGE.addProperty(prop,C.CAPA_GROUND_ITEMS,addInteractive)
    
    @staticmethod
    def cargar_mobs(extra_data,capa = 'capa_ground'):
        for key in _loader.STAGE.data[capa]['mobs']:
            pos = _loader.STAGE.data[capa]['mobs'][key]
            if key == 'npcs':
                clase = NPCSocial
    
            
                for ref in pos:
                    data = r.abrir_json(MD.mobs+ref+'.mob')
                    data.update(extra_data[ref])
                    for x,y in pos[ref]:
                        mob = clase(ref,x,y,data)
                        if capa == 'capa_ground':
                            _loader.STAGE.addProperty(mob,C.CAPA_GROUND_MOBS)
                        elif capa == 'capa_top':
                            _loader.STAGE.addProperty(mob,C.CAPA_TOP_MOBS)
    
    @staticmethod
    def cargar_hero(entrada):
        x,y = _loader.STAGE.data['entradas'][entrada]
        try:
            pc = MobGroup['heroe']
            ED.HERO = pc
            _loader.STAGE.addProperty(ED.HERO,C.CAPA_HERO)
            ED.HERO.ubicar(x,y)
            ED.HERO.mapX = x
            ED.HERO.mapY = y
        except:
            ED.HERO = PC(r.abrir_json(MD.mobs+'hero.mob'),x,y)
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
            _loader.STAGE.addProperty(sld,C.CAPA_GROUND_SALIDAS)
    
    @staticmethod
    def cargar_limites():
        if 'limites' in _loader.STAGE.data:
            limites = _loader.STAGE.data['limites']
            
            for key in limites:
                _loader.STAGE.limites[key.lower()] = limites[key]