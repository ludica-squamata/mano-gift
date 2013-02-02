import pygame,sys
from mapa import Stage
from mobs import PC
from misc import Resources as r

pygame.init()

tamanio = alto, ancho = 512,512
negro = pygame.Color('black')
pantalla = pygame.display # screen
fondo = pantalla.set_mode(tamanio) # surface
fondo.fill(negro)
mapa = Stage(r.abrir_json('maps/map1.json'),32)
FPS = pygame.time.Clock()
pygame.key.set_repeat(30,15)

hero = PC('grafs/hero_ph.png')
rect_fondo = mapa.render(fondo,0,0)
fondo.blit(hero.sprite,hero.pos)

while True:
        FPS.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mapa.render(fondo,+1,0)
    
                elif event.key  == pygame.K_RIGHT:
                    mapa.render(fondo,-1,0)
    
                elif event.key  == pygame.K_UP:
                    mapa.render(fondo,0,+1)
    
                elif event.key  == pygame.K_DOWN:
                    mapa.render(fondo,0,-1)
                
                elif event.key  == pygame.K_RETURN: # debug
                    print (hero.pos)
                
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
        fondo.blit(hero.sprite,hero.pos)
        pantalla.update([hero.rect,rect_fondo])
