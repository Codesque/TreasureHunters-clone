import pygame

from support import import_files 

class Tile(pygame.sprite.Sprite): 

    def __init__(self, pos ,surface : pygame.Surface , offset_x = 0 , offset_y = 0) -> None:
        super().__init__() 
        self.image = surface.convert_alpha() 
        #self.image.fill((204,102,90)) 
        self.rect = self.image.get_rect(topleft = pos + pygame.math.Vector2(offset_x ,offset_y))  
        self.tile_shift_vector = pygame.math.Vector2(0,0)  
        


    def shift_vector(self): 
        self.rect.center += self.tile_shift_vector 

    def shift_x(self , x_shift): 
        self.rect.centerx += x_shift  

    def update(self , shift_vector : pygame.math.Vector2) -> None:  
        self.tile_shift_vector = shift_vector
        self.shift_vector() 

class StaticTile(pygame.sprite.Sprite): 
    def __init__(self, size , x , y , surface : pygame.Surface) -> None:
        super().__init__()   
        self.image = pygame.Surface((size , size)) 
        self.image = surface 
        self.rect = self.image.get_rect(topleft = (x,y)) 

        

class GrassTile(pygame.sprite.Sprite): 

    def __init__(self , pos , surface : pygame.Surface) -> None:
        super().__init__()  
        self.image = surface.convert_alpha() 
        self.rect = self.image.get_rect(topleft = pos) 

    def shift_vector(self): 
        self.rect.center += self.tile_shift_vector  

    def update(self , shift_vector : pygame.math.Vector2) -> None:  
        self.tile_shift_vector = shift_vector
        self.shift_vector()  


class TreeObject(pygame.sprite.Sprite): 

    def __init__(self,pos, type="palm_bg") -> None: 
        # types are palm_bg , palm_large , palm_small
        super().__init__() 
        self.type = type  
        try:
            self.animations = import_files("../Tiled/graphics/treasure_hunters/level_1/terrain/"+self.type)  
        except: 
            print("UnCorrect Type Selection! Current types are : palm_bg , palm_large , palm_small") 
        
        self.image = self.animations[0] 
        self.rect = self.image.get_rect(topleft = pos)   

        # for animation to work properly : 
        self.frame_counter = 0 
        self.animation_speed = 0.1

    def shift_vector(self): 
        self.rect.center += self.tile_shift_vector   

    def animate(self):  

        self.frame_counter += self.animation_speed 
        if self.frame_counter >= len(self.animations): 
            self.frame_counter = 0 

        self.image = self.animations[int(self.frame_counter)]  

    def update(self , vector: pygame.math.Vector2): 
        self.tile_shift_vector = vector 
        self.animate() 
        self.shift_vector() 


class Coins(pygame.sprite.Sprite):  

    def __init__(self,pos, type="gold") -> None: 
        
        super().__init__() 
        self.type = type  
        try:
            self.animations = import_files("../Tiled/graphics/treasure_hunters/level_1/coins/"+self.type)  
        except: 
            print("UnCorrect Type Selection! Current types are : silver , gold") 
        
        self.image = self.animations[0] 
        self.rect = self.image.get_rect(topleft = pos)   

        # for animation to work properly : 
        self.frame_counter = 0 
        self.animation_speed = 0.2 
        self.isTouched = False 

    def shift_vector(self): 
        self.rect.center += self.tile_shift_vector   

    def animate(self):  

        self.frame_counter += self.animation_speed 
        if self.frame_counter >= len(self.animations): 
            self.frame_counter = 0 

        self.image = self.animations[int(self.frame_counter)]   

    def kill(self) -> None:
        return super().kill()
        

        

    def update(self , vector: pygame.math.Vector2): 
        self.tile_shift_vector = vector 
        self.animate() 
        self.shift_vector()  



class WaterAnimation(pygame.sprite.Sprite): 

    def __init__(self , size , x , y , path = "../Tiled/graphics/treasure_hunters/level_1/decoration/water") -> None:
        super().__init__()   
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y)) 
        self.animations = import_files(path) 
        self.frame_counter = 0 
        self.animation_speed = 0.1 
		


    def animate(self): 
        self.frame_counter += self.animation_speed 
        if self.frame_counter >= len(self.animations): 
            self.frame_counter = 0
        self.image = self.animations[int(self.frame_counter)] 

    def shift_vector(self): 
        self.rect.center += self.tile_shift_vector  

    def update(self , shift_vector : pygame.math.Vector2) -> None:  
        self.animate()
        self.tile_shift_vector = shift_vector
        self.shift_vector()  




        