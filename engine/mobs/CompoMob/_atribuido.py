from engine.base.azoeSprite import AzoeSprite


class Atribuido(AzoeSprite):
    ataque = 0
    defensa = 0
    ataque_especial = 0
    defensa_especial = 0
    social = 0
    velocidad = 0  # en pixeles por frame
    salud = 0  # salud máxima
    mana = 0  # maná maximo
    salud_act = 0 # puntos de salud restantes
    mana_act = 0  # cantidad de magia restante.

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        data = self.data['atributos']
        self.ataque = data['ataque']
        self.defensa = data['defensa']
        self.ataque_especial = data['ataque_especial']
        self.defensa_especial = data['defensa_especial']
        self.mana = data['mana']
        self.social = data['social']
        self.velocidad = data['velocidad']
        self.salud = data['salud']
        self.salud_act = self.salud
        self.mana_act = self.mana

    def mover(self, dx, dy):
        dx *= self.velocidad
        dy *= self.velocidad
        return dx, dy
