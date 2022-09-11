import pygame 
import settings 
from support import import_files  
import random 

class Zombies(pygame.sprite.Sprite): 
    
    def __init__(self , pos) -> None:
        
        super().__init__()
        self.frame_counter = 0 
        self.animation_speed = 0.3  
        self.animation_run = import_files("../Tiled/graphics/treasure_hunters/level_1/enemy/run") 
        
        #self.animation_explode = import_files("../Tiled/graphics/treasure_hunters/level_1/enemy/explosion") 
        offset = pygame.math.Vector2(0,15)
        self.image = self.animation_run[0] 
        self.rect = self.image.get_rect(topleft = pos+offset)  

        # Running Attributes 
        self.speed = pygame.math.Vector2(random.randint(3,5) , 0 ) 
        self.direction = pygame.math.Vector2(1 , 0) 

    def turn_from_corner(self): 
        self.direction.x *= -1 

    def animate(self):  
        self.frame_counter += self.animation_speed 
        if self.frame_counter >= len(self.animation_run): 
            self.frame_counter = 0 

        self.image = self.animation_run[int(self.frame_counter)] 
        if self.direction.x > 0 : 
            self.image = pygame.transform.flip(self.image , True , False)   

    def update(self , xshift : pygame.math.Vector2): 
        self.animate()  
        self.rect.x += self.speed.x * self.direction.x 
        self.rect.x += xshift.x 

        
class Constraints(pygame.sprite.Sprite): 

    def __init__(self, surface : pygame.Surface , pos ) -> None:
        super().__init__() 
        self.image = surface  
        self.rect = self.image.get_rect(topleft = pos) 

    def update(self , xshift : pygame.math.Vector2): 
        self.rect.centerx += xshift.x 

         
            
        
        
        





