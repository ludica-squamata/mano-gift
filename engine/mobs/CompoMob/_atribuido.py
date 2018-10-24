from engine.base.azoe_sprite import AzoeSprite


class Atribuido(AzoeSprite):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        self.accion_fisica = self.data['atributos']['accion_fisica']
        self.defensa_fisica = self.data['atributos']['defensa_fisica']
        self.accion_especial = self.data['atributos']['accion_especial']
        self.defensa_especial = self.data['atributos']['defensa_especial']
        self.accion_social = self.data['atributos']['accion_social']
        self.defensa_social = self.data['atributos']['defensa_social']

        self.velocidad = self.data['atributos']['velocidad']

        self.salud_act = self.data['atributos']['salud']
        self.mana_act = self.data['atributos']['mana']

        self.salud = self.salud_act
        self.mana = self.mana_act

    def mover(self, dx, dy):
        dx *= self.velocidad
        dy *= self.velocidad
        return dx, dy
