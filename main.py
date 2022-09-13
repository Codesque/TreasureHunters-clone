
import pygame 
import time   
from settings import *  
 



pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))    

from level import Level 
from overworld import Overworld

class Game : 

    def __init__(self) -> None: 
        self.max_level = 1
        self.overworld = Overworld(1 , self.max_level , screen , self.create_level)  
        self.status = "overworld"   
        self.display_surface = pygame.display.get_surface()

    def create_level(self , current_level): 
        self.level = Level(screen , current_level , self.create_overworld)  
        self.status = "level" 

    def create_overworld(self , current_level , new_max_level ): 
        self.status = "overworld"  
        if new_max_level > self.max_level : 
            self.max_level = new_max_level
        self.overworld = Overworld(current_level , self.max_level , screen , self.create_level )

    def run(self):  
        if self.status == "overworld":
            self.overworld.run() 
        else : 
            self.level.run() 


previous_time = time.time()
running = True  

level1 = Level(screen , 1 , Game.create_overworld)
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


     
