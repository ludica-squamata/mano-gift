class Teclas:
    ARRIBA, ABAJO, IZQUIERDA, DERECHA = 0, 0, 0, 0
    ACCION, CONTEXTUAL, MENU = 0, 0, 0

    _keydict = None

    def __init__(self, data):
        """No es que vaya a haber más de uno,
        pero mirá lo que hacemos en constantes..."""

        self.asignar(data)

        # podría ser __init__ en lugar de asignar,
        # pero lo dejo así por las dudas.

    def asignar(self, data):
        """Usamos este metodo para cargar desde config.json
        :param data: dict
        """

        self.ARRIBA = data['arriba']
        self.ABAJO = data['abajo']
        self.IZQUIERDA = data['izquierda']
        self.DERECHA = data['derecha']

        self.ACCION = data['accion']
        self.CONTEXTUAL = data['contextual']
        self.MENU = data['menu']

        self._keydict = self._crear_keydict()

    def _crear_keydict(self):
        observar = {}
        _teclas = {
            'arriba': self.ARRIBA,
            'abajo': self.ABAJO,
            'derecha': self.DERECHA,
            'izquierda': self.IZQUIERDA,
            'accion': self.ACCION,
            'contextual': self.CONTEXTUAL,
            'menu': self.MENU,
        }

        for key in _teclas:
            observar[_teclas[key]] = {'key': _teclas[key], 'nom': key,
                                      'pressed': False, 'tap': False,
                                      'holding': 0, 'hold': False,
                                      'release': False, 'held': 0}

        return observar

    def devolver(self):
        return self._keydict
