import sys, pygame

tamaño_cuadro=32

def cargarImagen(imagen):
    return pygame.image.load(sys.path[0]+'/grafs/'+imagen).convert_alpha()

class Globales():
    VELOCIDAD=1

class Mob (pygame.sprite.DirtySprite):
    variacion_velocidad = 0
    def __init__ (self, *mobgroups):
        super().__init__(mobgroups)
        self.dirty = 2
        self.rect = self.image.get_rect()
    def mover(self):
        pass

class MobGroup(pygame.sprite.LayeredDirty):
    def __init__(self, *mobs, **kwargs):
        super().__init__(*mobs,**kwargs)

        
class Hero(Mob):
    ARRIBA =1
    DERECHA = 2
    ABAJO =3
    IZQUIERDA=4
    variacion_velocidad=16
    def __init__(self):
        self.images=(cargarImagen('heroeE.png'),cargarImagen('heroeF.png'),cargarImagen('heroeI.png'),cargarImagen('heroeD.png'))
        self.image=self.images[1]
        super().__init__()
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

class Enemy (Mob):
    variacion_velocidad=10
    direccion = 1
    def __init__(self):
        self.image=cargarImagen('Enemy.png')
        super().__init__()
        self.rect.y=70
        self.rect.x=50
    def mover(self):
        delta=Globales.VELOCIDAD*self.variacion_velocidad
        if self.direccion==1:
            self.rect.x += delta
        else:
            self.rect.x -= delta

        if self.rect.x >= 200:
            self.direccion = -1
        elif self.rect.x <=50:
            self.direccion = 1

class Vendor (Mob):
    def __init__(self):
        self.image=cargarImagen('Vendor.png')
        super().__init__()
        self.rect.y=30
        self.rect.x=150

pygame.init()
tamaño = ancho, alto = 512, 512
blanco = 255, 255, 255
pantalla = pygame.display.set_mode(tamaño)
backImages=(cargarImagen('c1.png'),cargarImagen('c2.png'),cargarImagen('c3.png'),cargarImagen('c4.png'),cargarImagen('c5.png'),cargarImagen('c6.png'))
bg=(1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,4,5,6)
pantalla.fill(blanco)
for i in range(len(bg)):
    if bg[i]!=0:
        back.blit(backImages[bg[i]-1],(i%16*32,i//16*32))
back=pantalla.convert()

heroe=Hero()
enemigo=Enemy()
vendedor=Vendor()

mapa=pygame.sprite.Sprite()
mapa.image=back
mapa.rect=back.get_rect()

gMapa=pygame.sprite.RenderUpdates(mapa)
#gMapa.clear(pantalla,back)
pygame.display.update(gMapa.draw(pantalla))

gHeroe=MobGroup(heroe)
gHeroe.clear(pantalla,back)
pygame.display.update(gHeroe.draw(pantalla))

gEnemigo=MobGroup(enemigo)
gEnemigo.clear(pantalla,back)
pygame.display.update(gEnemigo.draw(pantalla))

gVendedor=MobGroup(vendedor)
gVendedor.clear(pantalla,back)
pygame.display.update(gVendedor.draw(pantalla))

FPSc=pygame.time.Clock()

running=1
while running==1:
    FPSc.tick(30)
    enemigo.mover()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running=0
        if event.type==pygame.KEYDOWN:
            mapa.rect.x=25
            if event.key==pygame.K_UP:heroe.mover(Hero.ARRIBA)
            if event.key==pygame.K_DOWN:heroe.mover(Hero.ABAJO)
            if event.key==pygame.K_LEFT:heroe.mover(Hero.IZQUIERDA)
            if event.key==pygame.K_RIGHT:heroe.mover(Hero.DERECHA)
    
    updateList = gMapa.draw(pantalla)
    updateList.extend(gHeroe.draw(pantalla))
    updateList.extend(gEnemigo.draw(pantalla))
    updateList.extend(gVendedor.draw(pantalla))

    pygame.display.update(updateList)

pygame.quit()
