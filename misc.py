from pygame import image

class Util:
    # utilidades
    pass

class Resources:
    # aqui iria la carga de imagenes, sonidos, etc.
    def cargar_imagen(ruta):
        ar = image.load(ruta).convert_alpha()
        return ar
        

class Config:
    #configuraciones
    pass

