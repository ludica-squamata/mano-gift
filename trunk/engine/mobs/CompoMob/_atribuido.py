from engine.misc import Resources as r
from engine.globs import ModData as MD

class Atribuido:
    fuerza = 0 # capacidad del mob para empujar cosas.
    velocidad = 1 # en pixeles por frame
    show,hide = {},{}
    
    def generar_rasgos(self):
        rasgos = r.abrir_json(MD.scripts+'rasgos.json')
        
        for car in rasgos['cars']:
            if rasgos['cars'][car]:
                if car == "Fuerza":
                    self.show[car] = {"tipo": "atributo", "nombre":car, "value": self.fuerza}
                else:
                    self.show[car] = {"tipo": "atributo", "nombre":car, "value": 0}
            else:
                self.hide[car] = {"tipo": "atributo", "nombre":car, "value": 0}
        
        for hab in rasgos['habs']:
            if rasgos['habs'][hab]:
                self.show[hab] = {"tipo": "habilidad", "nombre":hab, "value": 0}
            else:
                self.hide[hab] = {"tipo": "habilidad", "nombre":hab, "value": 0}