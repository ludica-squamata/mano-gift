from engine.globs import ModData as MD
from engine.quests import QuestManager
from engine.misc import Resources as r
from .CompoMob import Sensitivo,Autonomo
from .mob import Mob

class NPC (Mob,Sensitivo,Autonomo):
    quest = None
    iniciativa = 2
    hablando = False
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        self.nombre = nombre
        super().__init__(ruta_img,stage,x,y,data)
        self.establecer_AI(data,x,y)
        self.establecer_sentidos()
        self.data = data
        
        self.generar_rasgos()
        self.tema_preferido = data['tema_preferido']
        self.temas_para_hablar = {}
        for tema in data['temas_para_hablar']:
            self.temas_para_hablar[tema] = r.abrir_json(MD.dialogos+data['temas_para_hablar'][tema])
        if 'quest' in data:
            QuestManager.add(data['quest'])
    
    def responder(self):
        self.hablando = True
    
    def mover(self):
        if not self.hablando:
            return super().mover()