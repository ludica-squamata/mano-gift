from .pausa import MenuPausa
from .equipo import MenuEquipo
from .opciones import MenuOpciones
from .cargar import MenuCargar
from .principal import MenuPrincipal
from .menu import Menu
from .model import MenuModel
from .name import MenuName
from .ability import MenuAbility
from .status import MenuStatus
from .map_selector import MenuDebug

default_menus = {'MenuPausa': MenuPausa,
                 'MenuEquipo': MenuEquipo,
                 'MenuCargar': MenuCargar,
                 'MenuDebug': MenuDebug,
                 'MenuPrincipal': MenuPrincipal,
                 'MenuOpciones': MenuOpciones,
                 'MenuNuevo': MenuModel,  # en realidad sería MenuModel,
                 'MenuName': MenuName,  # pero está así para que diga "nuevo" en Principal.
                 'MenuAbility': MenuAbility,  # No es el verdadero (y viejo) "MenuNuevo".
                 'MenuStatus': MenuStatus
                 }

# estructuras para los menues raiz Principal y Pausa.
# No son lo más "automático" que se puede hacer,
# pero son lo más aproximado y menos explicito que se me ocurre.

# Botones del Menú Pausa
pause_menus = [
    'MenuEquipo',
    'MenuStatus',
    'MenuOpciones',
    'MenuCargar'
]

# Botones del Menú Principal
inital_menus = [
    'MenuNuevo',
    'MenuCargar',
    'MenuOpciones',
    'MenuDebug'
]

__all__ = [
    'Menu',
    "default_menus",
    'pause_menus',
    'inital_menus',
]
