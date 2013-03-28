import json
from pygame import image,Rect


class Util:
    # utilidades
    pass

class Resources:
    # aqui iria la carga de imagenes, sonidos, etc.
    def cargar_imagen(ruta):
        ar = image.load(ruta).convert_alpha()
        return ar
    
    def split_spritesheet(ruta):
        spritesheet = Resources.cargar_imagen(ruta)
        ancho = spritesheet.get_width()
        alto = spritesheet.get_height()
        tamanio = 32,32
        sprites = []
        for x in range(int(ancho/32)):
            for y in range(int(alto/32)):
                sprites.append(spritesheet.subsurface(Rect(((int(ancho/(ancho/32))*x,
                                                            int(alto/(alto/32))*y),
                                                            tamanio))))
        return sprites
                
    def abrir_json (archivo):
        ex = open(archivo)
        data = json.load(ex)
        ex.close()
        return data

class Config:
    #configuraciones
    pass

