from pygame import image,Rect
import json

class Resources:
    # aqui iria la carga de imagenes, sonidos, etc.
    def cargar_imagen(ruta):
        ar = image.load('data/grafs/'+ruta).convert_alpha()
        return ar
    
    def split_spritesheet(ruta,w=32,h=32):
        spritesheet = Resources.cargar_imagen(ruta)
        ancho = spritesheet.get_width()
        alto = spritesheet.get_height()
        tamanio = w,h
        sprites = []
        for y in range(int(alto/h)):
            for x in range(int(ancho/w)):
                sprites.append(spritesheet.subsurface(Rect(((int(ancho/(ancho/w))*x,
                                                            int(alto/(alto/h))*y),
                                                            tamanio))))
        return sprites
                
    def abrir_json (archivo):
        ex = open(archivo,'r')
        data = json.load(ex)
        ex.close()
        return data
    
    def guardar_json (archivo,datos):
        ex = open(archivo,'w')
        json.dump(datos,ex, sort_keys=True,indent=4, separators=(',', ': '))
        ex.close()