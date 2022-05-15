import random
import pygame
from pygame.locals import(
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    QUIT,
)
screen_width=800
screen_height=600

class cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(cloud, self).__init__()
        self.surf=pygame.image.load("Cloud.png").convert()
        self.surf=pygame.transform.scale(self.surf,(125,75))
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect=self.surf.get_rect(
            center=(
                random.randint(screen_width+20,screen_width+100),
                random.randint(0,screen_height)
            )
        )
    def update(self):
        self.rect.move_ip(-5,0)
        if self.rect.right<0:
            self.kill()

class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(enemy, self).__init__()
        self.surf=pygame.image.load("red missile.jpg").convert()
        self.surf=pygame.transform.rotate(self.surf,90)
        self.surf=pygame.transform.scale(self.surf,(55,35))
        self.surf=pygame.transform.rotate(self.surf,90)
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect=self.surf.get_rect(
            center=(
                random.randint(screen_width+20,screen_width+100),
                random.randint(0,screen_height)
            )
        )
        self.speed=random.randint(5,20)

    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right<0:
            self.kill()

class player(pygame.sprite.Sprite):
    def __init__(self):
        super(player,self).__init__()
        self.surf=pygame.image.load("red.png").convert()
        self.surf=pygame.transform.rotate(self.surf,-90)
        self.surf=pygame.transform.scale(self.surf,(45,85))
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        self.rect=self.surf.get_rect()

    def update(self,pressed_key):
        if pressed_key[K_UP]:
            self.rect.move_ip(0,-8)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0,8)
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-8,0)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(8,0)

        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>screen_width:
            self.rect.right=screen_width
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>screen_height:
            self.rect.bottom=screen_height    
        
pygame.init()

screen=pygame.display.set_mode((screen_width,screen_height))
addenemy=pygame.USEREVENT+1
pygame.time.set_timer(addenemy,450)
addcloud=pygame.USEREVENT+2
pygame.time.set_timer(addcloud,1000)
running=True

player=player() 
enemies=pygame.sprite.Group()
clouds=pygame.sprite.Group()
all_sprites=pygame.sprite.Group()
all_sprites.add(player)
clock=pygame.time.Clock()
#bg = pygame.image.load("BG.png")
while running:
  
    for event in pygame.event.get():
        if event.type== KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running=False
        elif event.type==QUIT:
            running=False
        elif event.type==addenemy:
            new_enemy=enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type==addcloud:
            new_cloud=cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
    pressed_key=pygame.key.get_pressed()
    player.update(pressed_key)
    enemies.update()
    clouds.update()
    screen.fill((135, 206, 250))
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
    if pygame.sprite.spritecollideany(player,enemies):
        player.kill()
        running=False  
    pygame.display.flip()   
    clock.tick(30)
pygame.quit()