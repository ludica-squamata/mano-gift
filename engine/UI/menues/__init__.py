from .pausa import MenuPausa
from .equipo import MenuEquipo, _boton_equipo
from .opciones import MenuOpciones, _boton_opciones
from .cargar import MenuCargar, _boton_cargar
from .personaje import MenuNuevo
from .principal import MenuPrincipal
from .menu import Menu

default_menus = {'MenuPausa': MenuPausa,
                 'MenuEquipo': MenuEquipo,
                 'MenuCargar': MenuCargar,
                 'MenuNuevo': MenuNuevo,
                 'MenuPrincipal': MenuPrincipal,
                 'MenuOpciones': MenuOpciones
                 }

# estructuras para los menues raiz Principal y Pausa.
# No son lo más "automático" que se puede hacer,
# pero son lo más aproximado y menos explicito que se me ocurre.

# Botones del Menú Pausa
pause_menus = [
    'MenuEquipo',
    'MenuOpciones',
    'MenuCargar'
]

# Botones del Menú Principal
inital_menus = [
    'MenuNuevo',
    'MenuCargar',
    'MenuOpciones'
]

__all__ = [
    'Menu',
    "default_menus",
    'pause_menus',
    'inital_menus'
]
