import pygame

class Fighter():
    def __init__(self, player,  x, y, flip, data, spritesheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.offset = data[2]
        self.image_scale = data[1]
        self.flip = flip
        self.rect = pygame.Rect((x,y,180,96))
        self.vely_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.update_time = pygame.time.get_ticks()
        self.action = 0 
        self.frame_index = 0
        self.anim_list = self.load_images(spritesheet,animation_steps)
        self.image = self.anim_list[self.action][self.frame_index]
        self.attack_type = 0
        self.hit = False
        self.health = 100
        self.alive = True
        self.attack_cooldown = 10
        self.health = 100
        
    def load_images(self,spritesheet,animation_steps):
        anim_list = []
        for j, animation in enumerate(animation_steps):
            img1list = []
            for i in range(animation):
                img1 = spritesheet.subsurface(i*self.size,j*self.size,self.size,self.size)
                img1list.append(pygame.transform.scale(img1,(self.size*self.image_scale,self.size*self.image_scale)))
            anim_list.append(img1list) 
        return anim_list
            
    def move(self, screen_width, screen_height,surface, target, round_done):
        SPEED=8
        GRAVITY = 1.5
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()
        if self.attacking == False and self.alive == True and round_done == False:
            
            if self.player == 1:             
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]: 
                    dx = SPEED
                    self.running = True
                if key[pygame.K_SPACE] and self.jump == False:
                    self.vely_y = -30
                    self.jump = True

                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2
            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]: 
                    dx = SPEED
                    self.running = True
                if key[pygame.K_UP] and self.jump == False:
                    self.vely_y = -30
                    self.jump = True

                if key[pygame.K_9] or key[pygame.K_0]:
                    self.attack(target)
                    if key[pygame.K_9]:
                        self.attack_type = 1
                    if key[pygame.K_0]:
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

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1


        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('Audio/PUNCHSVC.mp3'))


        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 11
        self.image = self.anim_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.anim_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.anim_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 5
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 5
    def attack(self, target):
        if self.attack_cooldown == 0: 
            if self.jump == False:
                self.attacking = True
                attacking_rect = pygame.Rect(self.rect.centerx - (self.rect.width/1.3 * self.flip),self.rect.y*1.1,self.rect.width/1.3,self.rect.height/1.3)
                if attacking_rect.colliderect(target.rect):
                    target.health -= 7
                    target.hit = True
                
    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index =  0
            self.update_time = pygame.time.get_ticks()

    def draw(self,surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x-self.offset[0], self.rect.y-self.offset[1]))