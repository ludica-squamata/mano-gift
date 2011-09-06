import sys, pygame

tamaño_cuadro=32

def cargarImagen(imagen):
    return pygame.image.load(sys.path[0]+'/grafs/'+imagen).convert_alpha()

class Globales():
    VELOCIDAD=1

class Pos:
    x = 0
    y = 0
    layer = 0

class Mob (pygame.sprite.DirtySprite):
    variacion_velocidad = 0
    pos=Pos()
    def __init__ (self, *mobgroups):
        super().__init__(mobgroups)
        self.dirty = 1
        self.rect = self.image.get_rect()
    def mover(self):
        pass

class Objeto:
    pass

class Tesoro (pygame.sprite.DirtySprite):
    contenido = list

class MobGroup(pygame.sprite.LayeredDirty):
    def __init__(self, *mobs, **kwargs):
        super().__init__(*mobs,**kwargs)
    def reubicar (self,x,y):
        for sprite in self:
            sprite.rect.y += y
            sprite.rect.x += x
            sprite.dirty = 1

class Hero (Mob):
    ARRIBA,ABAJO,IZQUIERDA,DERECHA = 0,1,2,3
    variacion_velocidad=2
    def __init__(self):
        self.images=(cargarImagen('heroeE.png'),cargarImagen('heroeF.png'),cargarImagen('heroeI.png'),cargarImagen('heroeD.png'))
        self.image=self.images[1]
        super().__init__()
        self.rect.y=8*tamaño_cuadro
        self.rect.x=8*tamaño_cuadro
        self.dirty = 1
        self.delta = Globales.VELOCIDAD*self.variacion_velocidad
        self.direccion = 0
    def mover(self,direccion):
        dx = dy = 0
        if direccion==self.ARRIBA:
            self.image=self.images[self.ARRIBA]
            dy = self.delta
        if direccion==self.ABAJO:
            self.image=self.images[self.ABAJO]
            dy = -self.delta
        if direccion==self.IZQUIERDA:
            self.image=self.images[self.IZQUIERDA]
            dx = self.delta
        if direccion==self.DERECHA:
            self.image=self.images[self.DERECHA]
            dx = -self.delta

        colisiona = True
        self.rect.x -= dx
        self.rect.y -= dy
        if pygame.sprite.spritecollideany(self,gSolidos)==None:
            colisiona=False
        self.rect.x += dx
        self.rect.y += dy

        if not colisiona:
            gMovibles.reubicar (dx,dy)

        self.direccion = direccion
        self.dirty=1
    
    def accion (self):
        if self.direccion == 0:
        # Mirando hacia arriba
            self.rect.y -= 10
            enRadio = pygame.sprite.spritecollideany(self,gNPC)
            self.rect.y += 10
        
        elif self.direccion == 1:
        # Mirando hacia abajo
            self.rect.y += 10
            enRadio = pygame.sprite.spritecollideany(self,gNPC)
            self.rect.y -= 10
        
        # Mirando hacia la izquierda
        elif self.direccion == 2:
            self.rect.x -= 10
            enRadio = pygame.sprite.spritecollideany(self,gNPC)
            self.rect.x += 10
        
        # Mirando hacia la derecha
        elif self.direccion == 3:
            self.rect.x += 10
            enRadio = pygame.sprite.spritecollideany(self,gNPC)
            self.rect.x -= 10
        
        if enRadio != None:
            enRadio.hablar()

                
class Enemy (Mob):
    variacion_velocidad=10
    def __init__(self):
        self.image=cargarImagen('Enemy.png')
        super().__init__()
        self.rect.y=70
        self.rect.x=0
        self.pos.x=0
        self.pos.y=70
        self.direccion=1
    def mover(self):
        delta=Globales.VELOCIDAD*self.variacion_velocidad*self.direccion
        self.rect.x += delta
        self.pos.x += delta
        if pygame.sprite.spritecollideany(self,gHeroe) == None:
            if (0 >= self.pos.x):
                self.direccion = 1 # Derecha
            elif (self.pos.x >= 200):
                self.direccion = -1 # Izquierda
        else:
            self.direccion *= -1 # Cambiá
            self.rect.x -= delta
            self.pos.x -= delta
        self.dirty=1

class Vendor (Mob):
    def __init__(self):
        self.image=cargarImagen('Vendor.png')
        super().__init__()
        self.rect.y=30
        self.rect.x=150
    def hablar(self):
        print ('Bienvenido')

class mapa (pygame.sprite.DirtySprite):
    pass

pygame.init()
tamaño = ancho, alto = 512, 512
blanco = 255, 255, 255
pantalla = pygame.display.set_mode(tamaño)
backImages=(cargarImagen('c1.png'),cargarImagen('c2.png'),cargarImagen('c3.png'),cargarImagen('c4.png'),cargarImagen('c5.png'),cargarImagen('c6.png'))
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

gMapa=pygame.sprite.LayeredDirty(mapa)
gMapa.clear(pantalla,reback)
pygame.display.update(gMapa.draw(pantalla))

gHeroe=MobGroup(heroe)
#gHeroe.clear(pantalla,reback)
pygame.display.update(gHeroe.draw(pantalla))

gEnemigo=MobGroup(enemigo)
gEnemigo.clear(pantalla,reback)
pygame.display.update(gEnemigo.draw(pantalla))

gNPC=MobGroup(vendedor) # grupo administrativo
#gVendedor.clear(pantalla,reback)
pygame.display.update(gNPC.draw(pantalla))

FPSc=pygame.time.Clock()
pygame.key.set_repeat(300,1) #150

gSolidos=MobGroup(enemigo,vendedor)
gMovibles=MobGroup(enemigo,vendedor,mapa)

running=1
while running==1:
    FPSc.tick(30)
    enemigo.mover()
    pantalla.blit(cuadro_dialogo.cuadro,(0,362))
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running=0
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                heroe.mover(Hero.ARRIBA)
            if event.key==pygame.K_DOWN:
                heroe.mover(Hero.ABAJO)
            if event.key==pygame.K_LEFT:
                heroe.mover(Hero.IZQUIERDA)
            if event.key==pygame.K_RIGHT:
                heroe.mover(Hero.DERECHA)
            if event.key==pygame.K_x:
                heroe.accion()
    
    pygame.display.update()
    
    updateList = gMapa.draw(pantalla)
    updateList.extend(gEnemigo.draw(pantalla))
    updateList.extend(gNPC.draw(pantalla))
    updateList.extend(gHeroe.draw(pantalla))
    
    pygame.display.update(updateList)

pygame.quit()
