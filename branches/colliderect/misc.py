import json
from pygame import image


class Util:
    # utilidades
    pass

class Resources:
    # aqui iria la carga de imagenes, sonidos, etc.
    def cargar_imagen(ruta):
        ar = image.load(ruta).convert_alpha()
        return ar
    
    def abrir_json (archivo):
        ex = open(archivo)
        data = json.load(ex)
        ex.close()
        return data

class Config:
    #configuraciones
    pass

