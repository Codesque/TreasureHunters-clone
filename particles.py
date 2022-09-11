import pygame  
from support import import_files 
import random 

pygame.init() 

class ParticleEffect(pygame.sprite.Sprite): 

    def __init__(self , pos , type) -> None:
        super().__init__()  

        self.static_frame_counter = 0 
        self.static_animation_speed = 0.15

        if type == "jump": 
            self.particles = import_files("graphics/character/dust_particles/jump") 

        elif type == "land": 
            self.particles = import_files("graphics/character/dust_particles/land")    

        self.image = self.particles[self.static_frame_counter] 
        self.rect = self.image.get_rect(center = pos)  



    
    def animate(self): 

        self.static_frame_counter += self.static_animation_speed 

        if self.static_frame_counter >= len(self.particles): 
            self.kill()   

        else : 
            self.image = self.particles[int(self.static_frame_counter)] 

    def update(self , xshift : pygame.math.Vector2): 
        self.animate()
        self.rect.x += xshift.x 
        

class ExplosionEffect(pygame.sprite.Sprite): 
    def __init__(self , pos) -> None:
        super().__init__()  
        self.import_animation()  
        self.image = self.animations[0] 
        self.rect = self.image.get_rect(center = pos) 


        self.frame_counter = 0 
        self.animation_speed = random.randint(3,5) / 20 


        
    def import_animation(self , path = "../Tiled/graphics/treasure_hunters/level_1/enemy/explosion"): 
        self.animations = import_files(path)  

    def animate(self) : 
        self.frame_counter += self.animation_speed 
        if self.frame_counter >= len(self.animations): 
            self.kill() 
        else : 
            self.image = self.animations[int(self.frame_counter)] 


    def update(self , xshift : pygame.math.Vector2) -> None:
        self.animate() 
        self.rect.x += xshift.x 


        


