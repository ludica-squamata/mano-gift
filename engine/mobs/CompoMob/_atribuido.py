from engine.base.azoeSprite import AzoeSprite


class Atribuido(AzoeSprite):
    atributos = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.atributos = self.data['atributos']
        self.salud_act = self.atributos['salud']
        self.mana_act = self.atributos['mana']

    def __getattr__(self, item):
        if item in self.atributos:
            return self.atributos[item]
        else:
            return 0

    def __setattr__(self, key, value):
        if key in self.atributos:
            self.atributos[key] = value

    def mover(self, dx, dy):
        dx *= self.velocidad
        dy *= self.velocidad
        return dx, dy
