import pygame,sys,time

#Game Configuuration, I should Have done this in a separate File :(
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 337
FRAME_RATE = 60

#Assets,Player And Opponent Main Logics
class Bullets(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        self.type = type
        if(self.type == "Player"):
            self.image = pygame.image.load("graphics/Player/SpongeBullet.png").convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,4)
            self.rect = self.image.get_rect(midbottom =(230,278))
        else:
            self.image = pygame.image.load("graphics/Opponent/SpongeBullet.png").convert_alpha()
            self.image = pygame.transform.rotozoom(self.image,0,4)
            self.rect = self.image.get_rect(midbottom =(370,278))
    
    def animate(self):
        if self.type == "Player":
            self.rect.x +=2
        else:
            self.rect.x -= 2
    
    def update(self):
        self.animate()
        
class healthBar(pygame.sprite.Sprite):
    def __init__(self,color=None,player_pos=(0,0),index=1,time=0):
        super().__init__()
        self.frames = [f"graphics/Player/Health/Health{x}.png" for x in range(1,10)]
        self.image =  pygame.transform.scale2x(pygame.image.load(self.frames[index])).convert_alpha() 
        self.rect = self.image.get_rect(center=player_pos)
        self.start_time = time # This Will Be Intially Zero
        
    def show_time(self):
        current_time = pygame.time.get_ticks() - self.start_time  #Subtracted Start time to reset the value of current time, A bit Complex But It Works Tough :/
        if(int(current_time/1000)==1): # After 1 second current time Remove The Sprite
           self.kill()
    
    def update(self):
        self.show_time()

class Player(pygame.sprite.Sprite):
    def __init__(self,bullets,health):
        super().__init__()
        self.Actions = {
                "idle":[(f"graphics/Player/idle/idle{x}.png") for x in range(1,6)],
                "death":[(f"graphics/Player/Death/death{x}.png") for x in range(1,8)],     
                "shoot":["graphics/Player/shoot.png","graphics/Player/idle/idle1.png"]
        }
        self.bullets = bullets
        self.health = health
        self.health_index = 1
        self.player_index = 0
        self.player_dead = False
        self.image = pygame.transform.scale2x(pygame.image.load(self.Actions.get('idle')[self.player_index])).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (170,330))
        
    def animate(self):
        #Player Idle animation
        keys = pygame.key.get_pressed()
        self.player_index+=0.09
        if not self.player_dead:
            if self.player_index >= len(self.Actions.get('idle')):self.player_index = 0
            self.image = pygame.transform.scale2x(pygame.image.load(self.Actions.get('idle')[int(self.player_index)])).convert_alpha()
        
        #Player shooting animation
        if type(self)==Player:
            if keys[pygame.K_SPACE] and not self.player_dead:
                self.player_index+=0.09              
                if self.player_index >= len(self.Actions.get('shoot')):self.player_index = 0
                self.image = pygame.transform.scale2x(pygame.image.load(self.Actions.get('shoot')[int(self.player_index)])).convert_alpha()
                #Conditon To add Bullets Only When The Shoot Frame is Selected
                if(self.player_index ==0):
                    bullets.add(Bullets("Player"))
        else:
            if keys[pygame.K_TAB] and not self.player_dead:
                self.player_index+=0.09              
                if self.player_index >= len(self.Actions.get('shoot')):self.player_index = 0
                self.image = pygame.transform.scale2x(pygame.image.load(self.Actions.get('shoot')[int(self.player_index)])).convert_alpha()
                #Conditon To add Bullets Only When The Shoot Frame is Selected
                if(self.player_index ==0):
                    bullets.add(Bullets("Opponent"))
        #Player Death
        if self.player_dead == True:
            global game_running
            if self.player_index >= len(self.Actions.get('death')):
                self.player_index = 0 
                #Separation Based On the Type
                if type(self)==Player:
                    game_running = False
                else:
                    self.health.empty()
                    self.kill()
            self.image = pygame.transform.scale2x(pygame.image.load(self.Actions.get('death')[int(self.player_index)])).convert_alpha()
            
                
        
    #Check Collsion (Unfinieshed Method)
    def Check_collision(self):
        if (pygame.sprite.spritecollide(self,bullets,True)):  
            if self.health_index >=8:
                self.health_index = 7     
                self.player_dead = True
            self.health_index +=1
            self.HP()
       
        
    
    # Method of Displaying Hp Bar
    def HP(self):
        health_x = self.rect.centerx
        health_y = self.rect.centery - 38
        reset_time = pygame.time.get_ticks()
        self.health.add(healthBar(0,(health_x,health_y),int(self.health_index),reset_time))
        
    def update(self):
        self.animate()       
        self.Check_collision()


class Opponent(Player):
    def __init__(self,bullets,health,color):
        super().__init__(bullets,health)
        self.Actions = {
                "idle":[(f"graphics/Opponent/idle/idle{x}.png") for x in range(1,6)],
                "death":[(f"graphics/Opponent/Death/death{x}.png") for x in range(1,8)],     
                "shoot":["graphics/Opponent/shoot.png","graphics/Opponent/idle/idle1.png"]
        }

        self.image =  pygame.transform.scale2x(pygame.image.load(self.Actions.get('idle')[self.player_index])).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (430,330))

    def animate(self):
        return super().animate()
    
    def update(self):
        return super().update()




#GAME WINDOW:
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Ultimate Shooting")
clock = pygame.time.Clock()

game_running = True

#GAME VARIBLES:
BG = pygame.image.load("graphics/Background/Bg.png")
bullets = pygame.sprite.Group()
Hp_bar = pygame.sprite.GroupSingle()
player = pygame.sprite.GroupSingle()
player.add(Player(bullets,Hp_bar))
opponent = pygame.sprite.GroupSingle()
opponent.add(Opponent(bullets,Hp_bar,"red"))



#GAME LOOP
while game_running:
    #EVENT LOOP:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.blit(BG,(0,0))
    player.draw(screen)
    player.update()
    opponent.draw(screen)
    opponent.update()
    bullets.draw(screen)
    bullets.update()
    Hp_bar.draw(screen)
    Hp_bar.update()
    pygame.display.update()
    clock.tick(60)