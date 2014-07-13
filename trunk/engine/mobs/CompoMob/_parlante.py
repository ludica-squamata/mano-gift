from engine.misc import Resources as r
from engine.globs import ModData as MD

class Parlante:
    interlocutor = None # para que el mob sepa con quién está hablando, si lo está
    conversaciones = [] # registro de los temas conversados
    temas_para_hablar = {}
    tema_preferido = ''
    hablante = True
    hablando = False
    
    def establecer_dialogos(self,data):
        self.tema_preferido = data['tema_preferido']
        self.temas_para_hablar = {}
        self.hablante = True
        for tema in data['temas_para_hablar']:
            self.temas_para_hablar[tema] = r.abrir_json(MD.dialogos+data['temas_para_hablar'][tema])
            
    def responder(self):
        self.hablando = True