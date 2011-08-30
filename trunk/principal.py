import sys, pygame

tamaño_cuadro=32
velocidad = 16

def cargarImagen(imagen):
    return pygame.image.load('./grafs/'+imagen).convert_alpha()

class Globales():
    VELOCIDAD=1

class Hero(pygame.sprite.DirtySprite):
    ARRIBA =1
    DERECHA = 2
    ABAJO =3
    IZQUIERDA=4
    variacion_velocidad=16
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.images=(cargarImagen('heroeE.png'),cargarImagen('heroeF.png'),cargarImagen('heroeI.png'),cargarImagen('heroeD.png'))
        self.dirty=1
        self.image=self.images[1]
        self.rect=self.image.get_rect()
        self.rect.y=8*tamaño_cuadro
        self.rect.x=8*tamaño_cuadro
    def mover(self,direccion):
        delta=Globales.VELOCIDAD*self.variacion_velocidad
        if direccion==self.ARRIBA:
            self.rect.y -= delta
            self.image=self.images[0]
        if direccion==self.ABAJO:
            self.rect.y += delta
            self.image=self.images[1]
        if direccion==self.IZQUIERDA:
            self.rect.x -= delta
            self.image=self.images[2]
        if direccion==self.DERECHA:
            self.rect.x += delta
            self.image=self.images[3]
        self.dirty=1

class Enemy (pygame.sprite.DirtySprite):
    ARRIBA =1
    DERECHA = 2
    ABAJO =3
    IZQUIERDA=4
    variacion_velocidad=16
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image=cargarImagen('Enemy.png')
        self.rect=self.image.get_rect()
        self.dirty=1
        self.rect.y=16*tamaño_cuadro
        self.rect.x=16*tamaño_cuadro
    def mover(self,direccion):
        delta=Globales.VELOCIDAD*self.variacion_velocidad
        if direccion==self.ARRIBA:
            self.rect.y -= delta
        if direccion==self.ABAJO:
            self.rect.y += delta
        if direccion==self.IZQUIERDA:
            self.rect.x -= delta
        if direccion==self.DERECHA:
            self.rect.x += delta
        self.dirty=1

pygame.init()
tamaño = ancho, alto = 512, 512
blanco = 255, 255, 255
pantalla = pygame.display.set_mode(tamaño)
backImages=(cargarImagen('c1.gif'),cargarImagen('c2.gif'),cargarImagen('c3.gif'),cargarImagen('c4.gif'),cargarImagen('c5.gif'),cargarImagen('c6.gif'))
bg=(1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,4,5,6)
pantalla.fill(blanco)
for i in range(len(bg)):
    if bg[i]!=0:
        pantalla.blit(backImages[bg[i]-1],(i%16*32,i//16*32))
back=pantalla.convert()

heroe=Hero()
enemigo=Enemy()

gSprites=pygame.sprite.RenderUpdates(heroe,enemigo)
gSprites.draw(pantalla)

running=1
while running==1:    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running=0
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:heroe.mover(Hero.ARRIBA)
            if event.key==pygame.K_DOWN:heroe.mover(Hero.ABAJO)
            if event.key==pygame.K_LEFT:heroe.mover(Hero.IZQUIERDA)
            if event.key==pygame.K_RIGHT:heroe.mover(Hero.DERECHA)
    
    pygame.display.update()

pygame.quit()
