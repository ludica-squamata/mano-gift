from engine.misc import Resources


class AzoeEntity:
    """Entidad que carga data de un archivo"""
    data = None  # {}

    def __init__(self, ruta):
        self.data = Resources.abrir_json(ruta)
