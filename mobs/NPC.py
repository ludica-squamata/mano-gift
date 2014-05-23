from .CompoMob import Sensitivo,Autonomo
from .mob import Mob
from globs import World as W, MobGroup
from quests import QuestManager
from misc import Resources as r

class NPC (Mob,Sensitivo,Autonomo):
    quest = None
    iniciativa = 2
    hablando = False
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.data = data
        self.nombre = nombre
        MobGroup.add(self)
        self.generar_rasgos()
        self.tema_preferido = data['tema_preferido']
        self.temas_para_hablar = {}
        for tema in data['temas_para_hablar']:
            self.temas_para_hablar[tema] = r.abrir_json('data/dialogs/'+data['temas_para_hablar'][tema])
        if 'quest' in data:
            QuestManager.add(data['quest'])
    
    def responder(self):
        self.hablando = True
    
    def mover(self):
        if not self.hablando:
            return super().mover()
