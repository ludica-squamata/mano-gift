from misc import Resources as r
from globs import Constants as C

class Quest:
    tipo = ''
    objetivos = {}
    agente = ''
    terminada = False
    
    def __init__(self, stage, datafile):
        data = r.abrir_json('scripts/'+datafile)
        self.stage = stage
        self.tipo = data['tipo']
        objetivos = data['objetivos']
        for cat in objetivos:
            if objetivos[cat] != []:
                self.objetivos[cat] = objetivos[cat]
        agente = data['agente']
        for mob in self.stage.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
            if mob.nombre == agente:
                self.agente = mob
                break
        self.on_Dialog = data['dialogos']['on']
        self.off_Dialog = data['dialogos']['off']
        
        self.agente.dialogos = self.on_Dialog

    def actualizar(self,obj):
        if self.tipo == 'kill':
            for cat in self.objetivos:
                if obj in self.objetivos[cat]:
                    self.objetivos[cat].remove(obj)
                if len(self.objetivos[cat]) != 0:
                    self.stage.setDialog(
                        'objetivos actuales: '+', '.join(self.objetivos[cat]))
                else:
                    self.resolver()
                    self.terminada = True
    
    def resolver(self):
        if not self.terminada:
            self.stage.setDialog('Quest completada!')
        
        self.agente.dialogos = self.off_Dialog
    