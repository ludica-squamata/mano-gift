#coding: utf-8
import pygame

from gift_util import cargar_imagen, Grupos, Mapa,Globales
from mobs_base import MobGroup
from hero import Hero
from enemigos import Enemy
from npcs import Vendor
from objetos import Tesoro

pygame.init()
blanco = 255, 255, 255
pantalla = pygame.display.set_mode((512,512))
backImages=(cargar_imagen('c1.png'),cargar_imagen('c2.png'),cargar_imagen('c3.png'),cargar_imagen('c4.png'),cargar_imagen('c5.png'),cargar_imagen('c6.png'))
bg=(1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,4,5,6)
pantalla.fill(blanco)
back=pantalla.convert()

reback = pygame.Surface((512,512)) # pantalla es un rect, este Surface hace que el fondo no se marque.
reback.fill(blanco) # no es lo que habias dicho, pero asi queda, por lo menos.

for i in range(len(bg)):
    if bg[i]!=0:
        back.blit(backImages[bg[i]-1],(i%16*32,i//16*32))

heroe=Hero()
enemigo=Enemy()
vendedor=Vendor()

mapa=pygame.sprite.DirtySprite()
mapa.image=back
mapa.rect=back.get_rect()

cofre = Tesoro()
cofre.rect.x = 300
cofre.rect.y = 30
cofre.contenido = ['Monedas']

Grupos.gItems = MobGroup(cofre)
#Grupos.gItems.clear(pantalla,reback)
pygame.display.update(Grupos.gItems.draw(pantalla))

Grupos.gMapa=pygame.sprite.LayeredDirty(mapa)
Grupos.gMapa.clear(pantalla,reback)
pygame.display.update(Grupos.gMapa.draw(pantalla))

Grupos.gHeroe=MobGroup(heroe)
#gHeroe.clear(pantalla,reback)
pygame.display.update(Grupos.gHeroe.draw(pantalla))

Grupos.gEnemigo=MobGroup(enemigo)
Grupos.gEnemigo.clear(pantalla,reback)
pygame.display.update(Grupos.gEnemigo.draw(pantalla))

Grupos.gNPC=MobGroup(vendedor) # grupo administrativo
#Grupos.gNPC.clear(pantalla,reback)
pygame.display.update(Grupos.gNPC.draw(pantalla))

FPSc=pygame.time.Clock()
pygame.key.set_repeat(300,1) #150

Grupos.gSolidos=MobGroup(enemigo,vendedor,cofre)
Grupos.gMovibles=MobGroup(enemigo,vendedor,mapa,cofre)
Grupos.gInteractivos = MobGroup (vendedor,cofre)

running=1
while running==1:
    FPSc.tick(30)
    enemigo.mover()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running=0
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:heroe.mover(Hero.ARRIBA)
            if event.key==pygame.K_DOWN:heroe.mover(Hero.ABAJO)
            if event.key==pygame.K_LEFT:heroe.mover(Hero.IZQUIERDA)
            if event.key==pygame.K_RIGHT:heroe.mover(Hero.DERECHA)
            if event.key==pygame.K_x:heroe.accion()
            if event.key==pygame.K_i:Globales.inventario.abrir()

    pygame.display.update()

    updateList = Grupos.gMapa.draw(pantalla)
    updateList.extend(Grupos.gItems.draw(pantalla))
    updateList.extend(Grupos.gEnemigo.draw(pantalla))
    updateList.extend(Grupos.gNPC.draw(pantalla))
    updateList.extend(Grupos.gHeroe.draw(pantalla))

    pygame.display.update(updateList)

pygame.quit()
