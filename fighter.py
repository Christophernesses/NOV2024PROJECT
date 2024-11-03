import pygame

class Fighter():
    def __init__(self, x, y, data, spritesheet, animation_steps):
        self.size = data[0]
        self.flip = False
        self.rect = pygame.Rect((x,y,257,96))
        self.vely_y = 0
        self.jump = False
        self.attacking = False
        self.action = 0 
        self.frame_index = 0
        self.anim_list = self.load_images(spritesheet,animation_steps)
        self.image = self.anim_list[self.action][self.frame_index]
        self.attack_type = 0
        self.health = 100
    def load_images(self,spritesheet,animation_steps):
        anim_list = []
        for j, animation in enumerate(animation_steps):
            img1list = []
            for i in range(animation):
                img1 = spritesheet.subsurface(0,0,self.size,self.size)
                img1list.append(img1)
            anim_list.append(img1list) 
        return anim_list
            
    def move(self, screen_width, screen_height,surface, target):
        SPEED=12
        GRAVITY = 2
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if self.attacking == False:
            if key[pygame.K_a]:
                dx = -SPEED
            if key[pygame.K_d]:
                dx = SPEED
            if key[pygame.K_SPACE] and self.jump == False:
                self.vely_y = -30
                self.jump = True

            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

  
        self.vely_y += GRAVITY
        dy+= self.vely_y
            
        if self.rect.left + dx <0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height -48:
            self.vely_y = 0
            dy = screen_height -48 - self.rect.bottom
            self.jump = False

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        self.rect.x += dx
        self.rect.y += dy
    def attack(self,surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2*self.rect.width * self.flip),self.rect.y,2*self.rect.width,self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        pygame.draw.rect(surface,(0,255,0),attacking_rect)

        # pygame.joystick.init()
        # if event.type == pygame.JOYDEVICEADDED:
        #     print("Controller connected: "+str(event))
        #     joy = pygame.j
    def draw(self,surface):
        pygame.draw.rect(surface,(255,0,0),self.rect)
        surface.blit(self.image, (self.rect.x, self.rect.y))