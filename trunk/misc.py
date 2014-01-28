import json
from pygame import image,Rect,mask as MASK,PixelArray,Surface
from globs.teclas import Teclas

class Util:
    ##
    #crea una sombra para la imagen pasada. de momento tiene inclinacion fija
    #@param surface Surface
    #@return Surface
    def crear_sombra(surface, mask = None):
        if mask == None:
            mask = MASK.from_surface(surface)
        h = surface.get_height()
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
        json.dump(datos,ex)
        ex.close()

class Config:
    # configuraciones
    recordar = False
    intro = True
    
    def cargar():
        data = Resources.abrir_json('config.json')
        Config.asignar(data)
        
    def guardar():
        from globs.constantes import Constants as C
        from globs.teclas import Teclas as T
        
        data = {
            "mostrar_intro":True,"recordar_menus":True, #próximamente cofigurables
            "resolucion":{"CUADRO":C.CUADRO,"ANCHO":C.ANCHO,"ALTO":C.ALTO},
            "teclas":{"arriba":T.ARRIBA,"abajo":T.ABAJO,
                      "derecha":T.DERECHA,"izquierda":T.IZQUIERDA,
                      "accion":T.ACCION,"hablar":T.HABLAR,
                      "cancelar":T.CANCELAR_DIALOGO,"inventario":T.INVENTARIO,
                      "posicion":T.CAMBIAR_POSICION,
                      "menu":T.MENU,"debug":T.DEBUG,"salir":T.SALIR}}
        
        Resources.guardar_json('config.json',data)
    
    def asignar(self,data):
        from globs.constantes import Constants as C
        from globs.teclas import Teclas as T
        
        Config.recordar = data['recordar_menus']
        Config.intro = data['mostrar_intro']
        C.CUADRO = data['resolucion']['CUADRO']
        C.ANCHO = data['resolucion']['ANCHO']
        C.ALTO = data['resolucion']['ALTO']
        T.asignar(data['teclas'])
    
