from ._caracterizado import Caracterizado
from random import randint


class Suertudo(Caracterizado):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def luck():
        return randint(1, 100)
