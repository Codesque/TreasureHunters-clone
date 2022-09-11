
import pygame 
import time   
from settings import *  
from level import Level


pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))  

previous_time = time.time()
running = True  

level1 = Level(level_map , screen)
clock = pygame.time.Clock()
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
    level1.run()
    pygame.display.update()  
    clock.tick(60)


     
