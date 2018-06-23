from engine.misc import Config


class Teclas:
    key_dict = None

    @classmethod
    def asignar(cls, data=None):
        """Usamos este metodo para cargar desde config.json
        :param data: dict
        """
        if data is None:
            data = Config.dato('comandos')

        cls.key_dict = {
            # data["<string>"] == int
            data['arriba']: {'nom': 'arriba'},
            data['abajo']: {'nom': 'abajo'},
            data['derecha']: {'nom': 'derecha'},
            data['izquierda']: {'nom': 'izquierda'},
            data['accion']: {'nom': 'accion'},
            data['contextual']: {'nom': 'contextual'},
            data['menu']: {'nom': 'menu'}
        }

        for key in cls.key_dict:
            cls.key_dict[key].update({'pressed': False, 'tap': False, 'holding': 0,
                                      'hold': False, 'release': False, 'held': 0})


Teclas.asignar()
