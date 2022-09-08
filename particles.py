import pygame  
from support import import_files

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
        

        


