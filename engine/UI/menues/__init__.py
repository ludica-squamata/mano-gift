from .menu_Pausa import MenuPausa
from .menu_Equipo import MenuEquipo, _boton_equipo
from .menu_Opciones import MenuOpciones, _boton_opciones
from .menu_Cargar import MenuCargar, _boton_cargar
from .menu_Personaje import MenuNuevo
from .menu_Principal import MenuPrincipal
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
