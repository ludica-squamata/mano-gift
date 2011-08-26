import sys, pygame

def iLoad(image):
    return pygame.image.load('./grafs/'+image).convert_alpha()

pygame.init()
size = width, height = 512, 512
speed = [2, 2]
white = 255, 255, 255
screen = pygame.display.set_mode(size)
backImages=(iLoad('c1.gif'),iLoad('c2.gif'),iLoad('c3.gif'),iLoad('c4.gif'),iLoad('c5.gif'),iLoad('c6.gif'))
bg=(1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,4,5,6)
hero = iLoad('heroe.gif')
#print(hero)
herorect = hero.get_rect()
screen.fill(white)
for i in range(len(bg)):
    if bg[i]!=0:
        screen.blit(backImages[bg[i]-1],(i%16*32,i//16*32))
back=screen.convert()
heroX=8
heroY=8
herorect=herorect.move(heroX*32,heroY*32)
screen.blit(hero, herorect)
pygame.display.update()
heroX=0
heroY=0
running=1

pygame.key.set_repeat(25,5)
FPSc=pygame.time.Clock()
FPS=pygame.font.Font(pygame.font.match_font('Courier New,Arial'),12)

while running==1:
    FPSc.tick(70)
    for event in pygame.event.get():
#        print(event)
        if event.type == pygame.QUIT: running=0#pygame.quit()#sys.exit()
##        if event.type==pygame.KEYDOWN:
##            #print(event)
##            #heroX=0
##            #heroY=0
##            if event.key==273:
##                heroY-=1
##            elif event.key==274:
##                heroY+=1
##            elif event.key==275:
##                heroX+=1
##            elif event.key==276:
##                heroX-=1
##        if event.type==pygame.KEYUP:
##            #print(event)
##            #heroX=0
##            #heroY=0
##            if event.key==273:
##                heroY+=1
##            elif event.key==274:
##                heroY-=1
##            elif event.key==275:
##                heroX-=1
##            elif event.key==276:
##                heroX+=1
    pygame.event.pump()
    tecla=pygame.key.get_pressed()
    heroX=0
    heroY=0
    if tecla[pygame.K_UP]:heroY=-1
    if tecla[pygame.K_DOWN]:heroY=1
    if tecla[pygame.K_LEFT]:heroX=-1
    if tecla[pygame.K_RIGHT]:heroX=1
    
    
    if heroX!=0 or heroY!=0:
#        print(heroX,heroY)
        screen.blit(back, herorect,herorect)
        herorect=herorect.move(heroX*2,heroY*2)
        screen.blit(hero, herorect)
    screen.blit(FPS.render(str(int(FPSc.get_fps())),False,(0,0,0),(255,255,255)),(150,0))
    pygame.display.update()
#    print( FPSc.get_fps())
pygame.quit()
