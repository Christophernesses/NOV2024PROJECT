import pygame
from fighter import Fighter




SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stream Flighter")

clock = pygame.time.Clock()
FPS = 60

FRAME_SIZE = 256  
FRAME_DATA = [FRAME_SIZE]
#background
background_image = pygame.image.load("Graphics/Background/Pond1.webp").convert_alpha()


duck_anims = pygame.image.load("Graphics/Animations/Anims.jpg").convert_alpha()
DUCK_STEPS = [20,21,31,20,17] #Idle,Walk,Jump,Attack1,Attack2



def draw_background():
    scaled_background = pygame.transform.scale(background_image,(SCREEN_WIDTH*1.2,SCREEN_HEIGHT)) #scale background to screen
    screen.blit(scaled_background,(0,0))

def draw_health(health,x,y):
    pygame.draw.rect(screen,(255,255,255),(x-2,y-2,404,34))
    pygame.draw.rect(screen,(255,0,0),(x,y,400,30))
    pygame.draw.rect(screen,(255,255,0),(x,y,400*(health/100),30))

fighter1 = Fighter(200,310, FRAME_DATA, duck_anims, DUCK_STEPS)
fighter2 = Fighter(700,310, FRAME_DATA, duck_anims, DUCK_STEPS)
    
  
 
while True:
    clock.tick(FPS)
    
    draw_background()


    draw_health(fighter1.health, 20, 20)
    draw_health(fighter2.health, 580, 20)
    
    fighter1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter2)
    
    

    fighter1.draw(screen)
    fighter2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()   
        
    pygame.display.update()

    
pygame.quit()
