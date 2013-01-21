import pygame
from misc import Resources as r

class Tile (pygame.sprite.DirtySprite):
    '''Clase para los objetos de ground_items'''
    
    #basicamente, sprites que no se mueven
    #para las cosas en pantalla (tronco de arbol, puerta, piedras, loot)
    #como los árboles de pokemon que se pueden golpear
    def __init__(self,imagen,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = r.cargar_imagen(imagen)
        self.rect = self.image.get_rect()

class Stage:
    capa_background = ''
    capa_background_colisiones = ''
    
    capa_ground_items = []
    capa_ground_mobs = []
    
    capa_top_items = []
    capa_top_mobs = []
    
    #def __init__(self, id_mapa):
    #    '''Busca los datos en la db, y carga los recursos que correspondan'''
    #    
    #    #self.capa_background = back
    #    #self.capa_background_colisiones = back_c
    #    #self.capa_ground_items = grnd_i
    #    #self.capa_ground_mobs = grnd_m
    #    #self.capa_top_items = top_i
    #    #self.capa_top_mobs = top_m
    #    pass
    #    
    #def render(self):
    #    pass
    
    def __init__(self,MAPA,CUADRO):
        self.MAPA = MAPA
        self.capa_background(MAPA,CUADRO)
        self.mapa_props(MAPA,CUADRO)
            
    def capa_background (self,MAPA,CUADRO):
        back = MAPA['capa_background']
        self.capa_background = r.cargar_imagen(back['fondo'])
        self.capa_background_colisiones = self.mapa_colisiones(back['colisiones'],CUADRO)
        
    def mapa_colisiones(self,colisiones,CUADRO):
        imagen = r.cargar_imagen(colisiones)
        color_colision = pygame.Color('magenta')
        test_rect = pygame.Rect(0,0,CUADRO,CUADRO)
        rects_colisiones = []
        for col in range(16):
            for fila in range(16):
                test_rect.top = col*CUADRO
                test_rect.left = fila*CUADRO
                if imagen.get_at((fila*(CUADRO+1), col*(CUADRO+1))) == color_colision:
                    rects_colisiones.append(test_rect.copy())
        return rects_colisiones
    
    def mapa_props (self,MAPA,CUADRO):
        TILES = MAPA['capa_ground']['tiles']
        REF = MAPA['capa_ground']['ref']
        for item in TILES: 
            x = item[1][0]*CUADRO
            y = item[1][1]*CUADRO
            self.capa_ground_items.append(Tile(REF[item[0]],x,y))
            
    def render(self,fondo):
        fondo.blit(self.capa_background,[0,0])
        for tile in self.capa_ground_items:
            fondo.blit(tile.image,[tile.x,tile.y])
        
        return fondo.get_rect()
            
