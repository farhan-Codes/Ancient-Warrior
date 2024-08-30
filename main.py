import pygame,sys,time

#Game Configuuration, I should Have done this in a separate File :(
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 337
FRAME_RATE = 60

#Assets,Player And Opponent Main Logics
class Bullets(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/Player/SpongeBullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,4)
        self.rect = self.image.get_rect(midbottom =(230,278))
    
    def animate(self):
        self.rect.x +=7
        if self.rect.right >= SCREEN_WIDTH:self.kill()
    
    def update(self):
        self.animate()

class Player(pygame.sprite.Sprite):
    def __init__(self,bullets):
        super().__init__()
        self.Actions = {
                "idle":[(f"graphics/Player/idle/idle{x}.png") for x in range(1,6)],
                "death":[(f"graphics/Player/Death/death{x}.png") for x in range(1,8)],     
                "shoot":["graphics/Player/shoot.png","graphics/Player/idle/idle1.png"]
        }
        self.player_index = 0
        self.image = pygame.transform.scale2x(pygame.image.load(self.Actions.get('idle')[self.player_index])).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (170,330))
        
    def animate(self):
        #Player Idle animation
        keys = pygame.key.get_pressed()
        self.player_index+=0.09
        if self.player_index >= len(self.Actions.get('idle')):self.player_index = 0
        self.image = pygame.transform.scale2x(pygame.image.load(self.Actions.get('idle')[int(self.player_index)])).convert_alpha()
        
        #Player shooting animation
        if keys[pygame.K_SPACE]:
            self.player_index+=0.09              
            if self.player_index >= len(self.Actions.get('shoot')):self.player_index = 0
            self.image = pygame.transform.scale2x(pygame.image.load(self.Actions.get('shoot')[int(self.player_index)])).convert_alpha()
            if(self.player_index ==0):bullets.add(Bullets())
            
        #Player Death
    
    def healthBar(self):
        pass
        
    def update(self):
        self.animate()       

#GAME WINDOW:
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Ultimate Shooting")
clock = pygame.time.Clock()
game_running = True

#GAME VARIBLES:
BG = pygame.image.load("graphics/Background/Bg.png")
bullets = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
player.add(Player(bullets))


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
    bullets.draw(screen)
    bullets.update()
    pygame.display.update()
    clock.tick(60)