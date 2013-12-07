import json
from pygame import image,Rect,mask as MASK,PixelArray,Surface


class Util:
    ##
    #crea una sombra para la imagen pasada. de momento tiene inclinacion fija
    #@param surface Surface
    #@return Surface
    def crear_sombra(surface, mask = None):
        if mask == None:
            mask = MASK.from_surface(surface)
        h = int(surface.get_height() *.9)
        w = surface.get_width()
        pxarray = PixelArray(Surface((int(w+h/2), h), 0, surface))
        for x in range(w):
            for y in range(h):
                if mask.get_at((x,y)):
                    pxarray[int(x+(h-y)/2),y] = (0,0,0,150)
        return pxarray.make_surface().convert_alpha()

class Resources:
    # aqui iria la carga de imagenes, sonidos, etc.
    def cargar_imagen(ruta):
        ar = image.load('grafs/'+ruta).convert_alpha()
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
        ex = open(archivo)
        data = json.load(ex)
        ex.close()
        return data

class Config:
    #configuraciones
    pass

