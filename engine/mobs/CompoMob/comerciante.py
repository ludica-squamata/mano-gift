class Comerciante:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wallet = []

    def recibir_dinero(self, value):
        self.wallet.append(value)