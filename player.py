
import os
import pygame

from settings import TILE_SIZE, debug  
from support import import_files


class Player(pygame.sprite.Sprite): 

    def __init__(self , pos , surface : pygame.Surface , create_particle) -> None:
        super().__init__()  

        # For animations 
        self.import_animations()  
        self.frame_counter = 0  
        self.animation_speed = 0.15  
        self.create_dust_particles = create_particle 
        

        #Creating Surface
        self.image = self.animations["idle"][0] 
        l , t = pos 
        w , h = 40 , 30
        self.rect = self.image.get_rect(topleft = pos)
        #self.sprites = {}    


        self.import_dust_animations() 
        self.dust_frame_counter = 0  
        self.dust_animation_speed = 0.15 
        self.display_surface = surface 

        self.v0 = 5
        self.speed = pygame.math.Vector2(self.v0 , self.v0) 
        self.direction = pygame.math.Vector2(0,0)       

        self.mass = 1 
        self.gravity = self.mass * 0.8
        self.jump_speed = -20

        #self.dir_changed = False 
        #self.old_import_animations(pos) 

        #player status : 
        self.status = "idle"  
        self.hasJump = 3
        self.face_right = True  
            # to configure animations based on the effect of collusions to our animations 
        self.on_ground = False 
        self.on_ceiling = False 
        self.on_left = False 
        self.on_right = False  

        

    def old_import_animations(self, pos):
        # Animation Speeds
        self.animation_speed = {} 
        self.animation_speed["run"] = 0.3 
        self.animation_speed["idle"] = 0.02


        # loading animations
        self.sprites["idle"] = [] 
        [self.sprites["idle"].append(
            "assets/Treasure Hunters/Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/01-Idle/Idle 0"+str(i+1)+".png") 
            for i in range(5)] 
         

        self.sprites["run"] = []  
        [self.sprites["run"].append(
            "assets/Treasure Hunters/Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/02-Run/Run 0"+str(i+1)+".png") 
            for i in range(6)] 
        

        self.status = "idle"   
        self.frame_counter = 0  
        self.image = pygame.image.load(self.sprites[self.status][round(self.frame_counter)]).convert_alpha()  
        self.rect = self.image.get_rect(topleft = pos)
    def old_animate(self):  

        
        self.frame_counter += self.animation_speed[self.status] 
        if self.frame_counter > len(self.sprites[self.status]) - 1: 
            self.frame_counter = 0 

        

        self.image = pygame.image.load(self.sprites[self.status][round(self.frame_counter)]).convert_alpha()  
        if self.dir_changed: 
            self.image = pygame.transform.flip(self.image , True , False)
            

    def import_animations(self ):  
        character_path = "graphics/character/"
        self.animations = {"idle":[] , "run":[] , "jump":[] , "fall":[]}  
        for animation in self.animations.keys():  
            fpath = character_path + animation
            self.animations[animation] = import_files(fpath) 


    def import_dust_animations(self): 
        path = "graphics/character/dust_particles/run"
        self.dust_run_particles = import_files(path)  

    def run_dust_animation(self): 
        if self.status == "run" and self.on_ground: 
            self.dust_frame_counter += self.dust_animation_speed 
            if self.dust_frame_counter >= len(self.dust_run_particles): 
                self.dust_frame_counter = 0 

            
            dust_animation = self.dust_run_particles[int(self.dust_frame_counter)]   

            if self.face_right :  
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10) 
                self.display_surface.blit(dust_animation , pos) 

            else :  
                pos = self.rect.bottomright - pygame.math.Vector2(-6,10)  
                dust_animation = pygame.transform.flip(dust_animation , True , False) 
                self.display_surface.blit(dust_animation , pos) 




            



    def animate(self): 
        animation = self.animations[self.status] 
        
        self.frame_counter += self.animation_speed
        if self.frame_counter >= len(animation): 
            self.frame_counter = 0 

        image = animation[int(self.frame_counter)]   
        if self.face_right : 
            self.image = image 
        else : 
            self.image = pygame.transform.flip(image , True , False) 



        # Configure the origin of the image for properly working animations.
		
        if self.on_ground and self.on_right:
			
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		
        elif self.on_ground and self.on_left:
			
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		
        elif self.on_ground:
			
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		
        elif self.on_ceiling and self.on_right:
			
            self.rect = self.image.get_rect(topright = self.rect.topright)
		
        elif self.on_ceiling and self.on_left:
			
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
		
        elif self.on_ceiling:
			
            self.rect = self.image.get_rect(midtop = self.rect.midtop)



    def get_status(self): 

        if self.direction.y < 0 : 
            self.status = "jump" 

        elif self.direction.y > self.gravity + 1 : # to pretend the problem of mixing jump and fall animations there is a tolerance ...
                                                # which if the falling speed isnt greater than gravity , then it is standing.
            self.status = "fall" 

        else :  
            if self.direction.x != 0 : 
                self.status = "run" 

            else : 
                self.status = "idle"  
                






    def apply_gravity(self): 
        self.direction.y += self.gravity 
        self.rect.y += self.direction.y 



    def get_input(self): 

            keys = pygame.key.get_pressed()  
             

            # the commented ones used for old_animate() method 
            
            if keys[pygame.K_w] and self.on_ground : 
                #self.status = "jump" 
                self.create_dust_particles(self.rect.midbottom)
                self.jump() 
                 
                  
             
                     

            if keys[pygame.K_d]: 
                self.direction.x = 1    
                self.face_right = True
                #self.dir_changed = False 
                #self.status = "run" 
                #self.old_animate()

            elif keys[pygame.K_a]: 
                self.direction.x = -1  
                self.face_right = False   
                #self.dir_changed = True 
                #self.status = "run" 
                #self.old_animate() 
                

            else : 
                self.direction.x = 0   
                #self.status = "idle" 
                #self.old_animate() 





    def jump(self): 
 
        self.direction.y += self.jump_speed 


    def update(self): 

        self.get_input()   
        debug(f"status : {self.status}  //  ground:{self.on_ground} ,ceiling: {self.on_ceiling} , on_Left: {self.on_left} ,on_right {self.on_right} ")
        self.get_status()
        self.animate()  
        self.run_dust_animation() 
        #pygame.draw.rect(self.display_surface , 'red' ,self.rect , 5)  
         
        



    



        
        