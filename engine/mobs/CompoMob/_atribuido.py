from engine.base.azoeSprite import AzoeSprite


class Atribuido(AzoeSprite):
    _atributos = None

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._atributos = self.data['atributos']
        self.salud_act = self._atributos['salud']
        self.mana_act = self._atributos['mana']

    # ataque ##############################

    @property
    def ataque(self):
        return self._atributos['ataque']

    @ataque.setter
    def ataque(self, value):
        self._atributos['ataque'] = value

    @ataque.deleter
    def ataque(self):
        self._atributos['ataque'] = 0

    # defensa ###############################

    @property
    def defensa(self):
        return self._atributos['defensa']

    @defensa.setter
    def defensa(self, value):
        self._atributos['defensa'] = value

    @defensa.deleter
    def defensa(self):
        self._atributos['defensa'] = 0

    # ataque_especial #######################

    @property
    def ataque_especial(self):
        return self._atributos['ataque_especial']

    @ataque_especial.setter
    def ataque_especial(self, value):
        self._atributos['ataque_especial'] = value

    @ataque_especial.deleter
    def ataque_especial(self):
        self._atributos['ataque_especial'] = 0

    # defensa_especial ######################

    @property
    def defensa_especial(self):
        return self._atributos['defensa_especial']

    @defensa_especial.setter
    def defensa_especial(self, value):
        self._atributos['defensa_especial'] = value

    @defensa_especial.deleter
    def defensa_especial(self):
        self._atributos['defensa_especial'] = 0

    # velocidad #############################

    @property
    def velocidad(self):
        return self._atributos['velocidad']

    @velocidad.setter
    def velocidad(self, value):
        self._atributos['velocidad'] = value

    @velocidad.deleter
    def velocidad(self):
        self._atributos['velocidad'] = 0

    # social ################################

    @property
    def social(self):
        return self._atributos['social']

    @social.setter
    def social(self, value):
        self._atributos['social'] = value

    @social.deleter
    def social(self):
        self._atributos['social'] = 0

    # salud ################################

    @property
    def salud(self):
        return self._atributos['salud']

    @salud.setter
    def salud(self, value):
        self._atributos['salud'] = value

    @salud.deleter
    def salud(self):
        self._atributos['salud'] = 0

    # ataque ##############################

    @property
    def mana(self):
        return self._atributos['mana']

    @mana.setter
    def mana(self, value):
        self._atributos['mana'] = value

    @mana.deleter
    def mana(self):
        self._atributos['mana'] = 0

    def mover(self, dx, dy):
        dx *= self.velocidad
        dy *= self.velocidad
        return dx, dy
