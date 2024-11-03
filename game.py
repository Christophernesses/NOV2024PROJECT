import pygame
from pygame import mixer
from fighter import Fighter


mixer.init()
pygame.font.init() 
pygame.joystick.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
COMS_BLUE = (105,185,225)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TURDUKKEN 3: The Final Quackdown")

clock = pygame.time.Clock()
FPS = 60
controller_count = 1
count_in = 1
count_ud = pygame.time.get_ticks()
player_score = [0,0]#p1,#p2
round_done = False
ROUND_COOLDOWN = 5000

FRAME_SIZE = 256
FRAME_SCALE = 4
FRAME_OFFSET = [420,400]
FRAME_DATA = [FRAME_SIZE,FRAME_SCALE, FRAME_OFFSET]

#background
background_image = pygame.image.load("Graphics/Background/city.jpg").convert_alpha()


duck_anims = pygame.image.load("Graphics/Animations/Anims.png").convert_alpha()
duck_anims2 = pygame.image.load("Graphics/Animations/Anims2.png").convert_alpha()

win_text  = pygame.image.load("Graphics/VICTORY.png").convert_alpha()
DUCK_STEPS = [20,21,31,20,11,18,30] #Idle,Walk,Jump,Whack,Peck,Hit,Die

pygame.mixer.Channel(0).play(pygame.mixer.Sound('Audio/KEVINMACLEODVOLATILEREACTION.MP3'))

score_font = pygame.font.Font("Graphics/Fonts/CafeFelixPersonalUseOnly-ARJ16.ttf", 30)
counter_font = pygame.font.Font("Graphics/Fonts/CityBrawlersBoldCaps.otf", 80)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))

def draw_background():
    scaled_background = pygame.transform.scale(background_image,(SCREEN_WIDTH*1.2,SCREEN_HEIGHT)) #scale background to screen
    screen.blit(scaled_background,(0,0))

def draw_health(health,x,y):
    pygame.draw.rect(screen,(255,255,255),(x-2,y-2,404,34))
    pygame.draw.rect(screen,(255,0,0),(x,y,400,30))
    pygame.draw.rect(screen,(255,165,0),(x,y,400*(health/100),30))

fighter1 = Fighter(1,200,400, False, FRAME_DATA, duck_anims, DUCK_STEPS)
fighter2 = Fighter(2,700,400, True, FRAME_DATA, duck_anims2, DUCK_STEPS)
    


while True:
    clock.tick(FPS)
    
    draw_background()


    draw_health(fighter1.health, 20, 20)
    draw_health(fighter2.health, 580, 20)
    draw_text("P1: " + str(player_score[0]), counter_font, COMS_BLUE, 20, 50)
    draw_text("P2: " + str(player_score[1]), counter_font, COMS_BLUE, 580, 50)
    if count_in <=0:
        fighter1.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter2, round_done)
        fighter2.move(SCREEN_WIDTH,SCREEN_HEIGHT,screen,fighter1, round_done)
    else:
        draw_text(str(count_in), counter_font,COMS_BLUE,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        if (pygame.time.get_ticks() - count_ud) >= 1000:
            count_in -=1
            count_ud = pygame.time.get_ticks()
    fighter1.update()
    fighter2.update()

    

    fighter1.draw(screen)
    fighter2.draw(screen) 

    if round_done == False:
        if fighter1.alive == False:
            player_score[1] += 1
            round_done = True
            round_out_time = pygame.time.get_ticks()
        elif fighter2.alive == False:
            player_score[0] += 1
            round_done = True
            round_out_time = pygame.time.get_ticks()
    else:
        screen.blit(win_text, (0,200))
        if pygame.time.get_ticks() -round_out_time > ROUND_COOLDOWN:
            round_done = False
            count_in = 4
            fighter1 = Fighter(1,200,400, False, FRAME_DATA, duck_anims, DUCK_STEPS)
            fighter2 = Fighter(2,700,400, True, FRAME_DATA, duck_anims2, DUCK_STEPS)
            
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    pygame.display.update()

    
pygame.quit()
