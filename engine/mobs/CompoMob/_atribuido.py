from engine.base.azoeSprite import AzoeSprite


class Atribuido(AzoeSprite):
    ataque = 0
    defensa = 0
    ataque_especial = 1
    defensa_especial = 0
    social = 0
    velocidad = 0  # en pixeles por frame
    salud = 0  # salud máxima

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        data = self.data['caracteristicas']
        self.ataque = data['ataque']
        self.defensa = data['defensa']
        self.ataque_especial = data['ataque_especial']
        self.defensa_especial = data['defensa_especial']
        self.social = data['social']
        self.velocidad = data['velocidad']
        self.salud = data['salud']
        self.salud_act = self.salud

    def mover(self, dx, dy):
        dx *= self.velocidad
        dy *= self.velocidad
        return dx, dy
