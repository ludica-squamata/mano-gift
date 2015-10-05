from engine.base.giftSprite import GiftSprite


class Atribuido(GiftSprite):
    fuerza = 0  # capacidad del mob para empujar cosas.
    velocidad = 1  # en pixeles por frame
    salud_max = 0  # salud máxima
    salud_act = 0  # salud actual
    direcciones = {'abajo': [0, 1], 'izquierda': [-1, 0], 'arriba': [0, -1], 'derecha': [+1, 0], 'ninguna': [0, 0]}
    direccion = 'abajo'

    def __init__(self, *args, **kwargs):
        self.velocidad = self.data['velocidad']
        self.fuerza = self.data['fuerza']
        self.salud_max = self.data['salud']
        self.carisma = self.data['carisma']
        self.salud_act = self.salud_max
        super().__init__(*args, **kwargs)
