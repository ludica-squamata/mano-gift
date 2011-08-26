import sys, pygame

tamaño_cuadro=32

def cargarImagen(imagen):
    return pygame.image.load('./grafs/'+imagen).convert_alpha()

class Hero(pygame.sprite.DirtySprite):
    ARRIBA =1
    DERECHA = 2
    ABAJO =3
    IZQUIERDA=4
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image=cargarImagen('heroe.gif')
        self.rect=self.image.get_rect()
        self.dirty=1
        self.rect.y=8*tamaño_cuadro
        self.rect.x=8*tamaño_cuadro
    def mover(self,direccion):
        if direccion==self.ARRIBA:
            self.rect.y -= tamaño_cuadro
        if direccion==self.DERECHA:
            self.rect.x += tamaño_cuadro
        if direccion==self.ABAJO:
            self.rect.y += tamaño_cuadro
        if direccion==self.IZQUIERDA:
            self.rect.x -= tamaño_cuadro
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
gHeroe=pygame.sprite.LayeredDirty(heroe)
gHeroe.clear(pantalla,back)
pygame.display.update(gHeroe.draw(pantalla))


#pygame.key.set_repeat(100000,100000)
FPSc=pygame.time.Clock()
FPS=pygame.font.Font(pygame.font.match_font('Courier New,Arial'),12)
#print(pygame.K_UP)
running=1
while running==1:
    FPSc.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running=0
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:heroe.mover(Hero.ARRIBA)
            if event.key==pygame.K_DOWN:heroe.mover(Hero.ABAJO)
            if event.key==pygame.K_LEFT:heroe.mover(Hero.IZQUIERDA)
            if event.key==pygame.K_RIGHT:heroe.mover(Hero.DERECHA)
##    pygame.event.pump()
##    tecla=pygame.key.get_pressed()
##    if tecla[pygame.K_UP]:heroe.mover(Hero.ARRIBA)
##    if tecla[pygame.K_DOWN]:heroe.mover(Hero.ABAJO)
##    if tecla[pygame.K_LEFT]:heroe.mover(Hero.IZQUIERDA)
##    if tecla[pygame.K_RIGHT]:heroe.mover(Hero.DERECHA)
    
    updateList = gHeroe.draw(pantalla)

    updateList.append(pantalla.blit(FPS.render(str(int(FPSc.get_fps())),False,(0,0,0),(255,255,255)),(150,0)))
    pygame.display.update(updateList)
#    print( FPSc.get_fps())
pygame.quit()
