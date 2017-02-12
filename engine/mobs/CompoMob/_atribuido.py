from engine.base.azoeSprite import AzoeSprite


class Atribuido(AzoeSprite):
    fuerza = 0  # capacidad del mob para empujar cosas.
    velocidad = 0  # en pixeles por frame
    salud_max = 0  # salud máxima
    salud_act = 0  # salud actual
    iniciativa = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocidad = self.data['velocidad']
        self.fuerza = self.data['fuerza']
        self.salud_max = self.data['salud']
        self.carisma = self.data['carisma']
        self.iniciativa = self.data['iniciativa']
        self.salud_act = self.salud_max

    def mover(self, dx, dy):
        dx *= self.velocidad
        dy *= self.velocidad
        return dx, dy
