
import pygame 
import time   
from settings import *  
 



pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))    

from level import Level 
from overworld import Overworld 
from gui import UI

class Game : 

    def __init__(self) -> None: 
        
        # UI 
        self.max_health = 100 
        self.current_health = 100  
        self.coins = 0
        self.ui = UI(screen)
        # Overworld Creation 
        self.max_level = 3
        self.overworld = Overworld(1 , self.max_level , screen , self.create_level)  
        self.status = "overworld"   
        self.display_surface = pygame.display.get_surface()

    def create_level(self , current_level): 
        self.level = Level(screen , current_level , self.create_overworld , self.change_coin_amount , self.change_health)  
        self.status = "level" 

    def create_overworld(self , current_level , new_max_level ): 
        self.status = "overworld"  
        if new_max_level > self.max_level : 
            self.max_level = new_max_level
        self.overworld = Overworld(current_level , self.max_level , screen , self.create_level ) 

    def change_coin_amount(self , amount):  
        self.coins += amount 

    def change_health(self , amount):  
        self.current_health += amount
        
    def game_over(self):  

        if self.current_health <= 0 : 
            self.create_overworld(1 , 0) 
            self.current_health = 100  
            self.max_health = 100
            self.coins = 0 


    def run(self):  
        if self.status == "overworld":
            self.overworld.run() 
        else : 
            self.level.run()  
            self.ui.show_health(self.current_health , self.max_health) 
            self.ui.show_coins(self.coins)  
            self.game_over()
            
            


previous_time = time.time()
running = True  

level1 = Level(screen , 1 , Game.create_overworld , Game.change_coin_amount , Game.change_health)
clock = pygame.time.Clock() 
game = Game()
while running: 

    delta_time = time.time() - previous_time 
    previous_time = time.time()  
    

    for e in pygame.event.get(): 
        if e.type == pygame.QUIT:
            running = False 
            pygame.quit() 
            raise SystemExit 

        if e.type == pygame.KEYDOWN: 
            if e.key == pygame.K_ESCAPE: 
                pygame.event.post(pygame.event.Event(pygame.QUIT))  

    screen.fill((51,102,204))  #(51,102,204) 
    game.run()
    #level1.run()
    pygame.display.update()  
    clock.tick(60)


     
