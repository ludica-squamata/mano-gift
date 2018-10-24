from .pausa import MenuPausa
from .equipo import MenuEquipo, _boton_equipo
from .opciones import MenuOpciones, _boton_opciones
from .cargar import MenuCargar, _boton_cargar
from .personaje import MenuNuevo
from .principal import MenuPrincipal
from .menu import Menu

MenuPausa.nombres = [_boton_equipo, _boton_opciones, _boton_cargar]

default_menus = {'MenuPausa': MenuPausa,
                 'MenuEquipo': MenuEquipo,
                 'MenuCargar': MenuCargar,
                 'MenuNuevo': MenuNuevo,
                 'MenuPrincipal': MenuPrincipal,
                 'MenuOpciones': MenuOpciones
                 }

__all__ = [
    'Menu',
    "default_menus"
]
