from pygame import mask as MASK,PixelArray,Surface

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