import pygame 
from support import import_files_convert , import_files
from settings import *  
from tile import WaterAnimation , StaticTile
import random 


class Sky : 
    def __init__(self , horizon) -> None:
        self.bottom , self.middle , self.top = import_files_convert("../Tiled/graphics/treasure_hunters/level_1/decoration/sky")  
        self.horizon = horizon  

        #stretch horizontally  
        self.top = pygame.transform.scale(self.top ,(SCREEN_WIDTH , TILE_SIZE)) 
        self.middle = pygame.transform.scale(self.middle ,(SCREEN_WIDTH , TILE_SIZE))  
        self.bottom = pygame.transform.scale(self.bottom ,(SCREEN_WIDTH , TILE_SIZE)) 



    def draw(self , surface : pygame.Surface): 

        for row in range(VERTICLE_TILE_NUMBER): 
            y = row * TILE_SIZE 
            if row < self.horizon :
                surface.blit(self.top , (0,y)) 
            elif row == self.horizon : 
                surface.blit(self.middle , (0 , y)) 
            else : 
                surface.blit(self.bottom , (0,y))

class Water:

    def __init__(self ,height : int , level_width : int) -> None: 
        water_start = SCREEN_WIDTH * -1 
        water_tile_size = 192 
        tile_x_amount = (level_width+SCREEN_WIDTH)//water_tile_size  

        self.water_sprites = pygame.sprite.Group()
        for tile in range(tile_x_amount): 
            x = tile * water_tile_size + water_start
            y = height 
            sprite = WaterAnimation(192 , x , y) 
            self.water_sprites.add(sprite) 
        
    def draw(self , surface : pygame.Surface , xshift : pygame.math.Vector2): 
        self.water_sprites.update(xshift) 
        self.water_sprites.draw(surface) 

class Clouds: 

    def __init__(self , horizon : int , level_width : int , cloud_number : int) -> None:
        
        cloud_surf_list = import_files("../Tiled/graphics/treasure_hunters/level_1/decoration/clouds") 

        min_x = SCREEN_WIDTH * -1 
        max_x = level_width + SCREEN_WIDTH 
        min_y = 0 
        max_y = horizon 

        self.cloud_sprites = pygame.sprite.Group()
        for cloud in range(cloud_number):   

            x = random.randint(min_x , max_x) 
            y = random.randint(min_y , max_y) 
            surface = cloud_surf_list[random.randint(0,2)] 
            
            sprite = StaticTile(0 , x , y , surface)  
            self.cloud_sprites.add(sprite) 


    def draw(self , surface : pygame.Surface , xshift : pygame.math.Vector2): 
        self.cloud_sprites.update(xshift)
        self.cloud_sprites.draw(surface)




