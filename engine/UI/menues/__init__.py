from .menu_Pausa import MenuPausa
from .menu_Equipo import MenuEquipo
from .menu_Opciones import MenuOpciones
from .menu_Cargar import MenuCargar
from .menu_Personaje import MenuNuevo
from .menu_Principal import MenuPrincipal
from .menu import Menu

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
