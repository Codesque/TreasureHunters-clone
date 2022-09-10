import pygame
from player import Player 
from tile import Tile 
from settings import *  
from particles import ParticleEffect 
import pytmx 
from pytmx import load_pygame



class Level :  

    def __init__(self , level_data , surface) -> None: 
        self.display_surface = surface 
        self.level_data = level_data  
        #self.setup_level(level_data)  
        self.setup_tiles()
        self.world_shift_vector = pygame.math.Vector2(0,0) 
        self.current_x = 0 

        self.dusts = pygame.sprite.GroupSingle() 
        self.player_on_the_ground = False  

        self.once = True 


    def create_jump_dust_particle(self , pos):  

        k = 10
        if self.gamers.sprite.face_right : 
            offset_x = -k 
        else : 
            offset_x = k 

        pos += pygame.math.Vector2(offset_x , 5)
        jumping_dust_sprite = ParticleEffect( pos ,"jump") 
        self.dusts.add(jumping_dust_sprite)

    def setup_level(self , layout): 
        self.tiles = pygame.sprite.Group() 
        self.gamers = pygame.sprite.GroupSingle() 
        for row_index , row in enumerate(layout): 
            for col_index , col in enumerate(row): 
                x , y  = col_index , row_index 
                pos = (x * TILE_SIZE , y * TILE_SIZE) 

                if col == "X": 
                    one_tile = Tile(pos , TILE_SIZE)  
                    self.tiles.add(one_tile) 

                if col == "P": 
                    self.player = Player(pos , self.display_surface , self.create_jump_dust_particle)  
                    self.gamers.add(self.player)  

    def setup_tiles(self , path = "../Tiled/levels/treasure_hunters1.tmx"): 
        self.tiles = pygame.sprite.Group() 
        #self.gamers = pygame.sprite.GroupSingle()  
        self.tmx_data = load_pygame(path)   
        
        """
        if self.once : 
            for layer in self.tmx_data.visible_layers : 
                print(layer.name) 
            self.once = False  
        """ 
        self.gamers = pygame.sprite.GroupSingle() 

        for layer in self.tmx_data.visible_layers : 

            if layer.name == "terrain" : 
                for x , y , surface in layer.tiles(): 
                    pos = (x * TILE_SIZE , y * TILE_SIZE)
                    new_terrain = Tile(pos ,surface) 
                    self.tiles.add(new_terrain)  

        
        object_layer = self.tmx_data.get_layer_by_name('spawn_point')  
        for obj in object_layer : 
            pos = (obj.x , obj.y) 
            new_player = Player(pos , self.display_surface , self.create_jump_dust_particle)  
            self.gamers.add(new_player)



            


            

        

                    
    def scroll_x(self): 
        player = self.gamers.sprite 
        player_x = player.rect.centerx 
        direction_x = player.direction.x 
        
        if player_x < CAMERA_BORDERS["left"] and direction_x < 0: 
            self.world_shift_vector.x = player.v0 
            player.speed.x = 0  

        elif player_x > SCREEN_WIDTH- CAMERA_BORDERS["right"] and direction_x > 0: 
            self.world_shift_vector.x = -player.v0
            player.speed.x = 0  

        else : 
            self.world_shift_vector.x = 0 
            player.speed.x = player.v0 




    def horizontal_movement_collusion(self): 
        player = self.gamers.sprite 

        player.rect.centerx += player.direction.x * player.speed.x  

        for sprite in self.tiles.sprites(): 

            if sprite.rect.colliderect(player.rect): 
                if player.direction.x < 0 : # player is moving to left 
                    player.rect.left = sprite.rect.right 
                    player.on_left = True 
                    self.current_x = player.rect.left # player could jump through , this statement will control this

                elif player.direction.x > 0 : # player is moving to right 
                    player.rect.right = sprite.rect.left 
                    player.on_right = True 
                    self.current_x = player.rect.right # player could jump through , this statement will control this 

        if player.on_left and (player.direction.x >= 0 or self.current_x > player.rect.left) : 
            player.on_left = False 

        if player.on_right and  (player.direction.x <= 0 or self.current_x < player.rect.right) : 
            player.on_right = False 
                    

    def get_player_on_ground(self): # before verticle collusions , if the player is not on the ground , check the second statement
        player = self.gamers.sprite 
        if player.on_ground : 
            self.player_on_the_ground = True 
        else : 
            self.player_on_the_ground = False  


    def create_landing_particles(self): 
        player = self.gamers.sprite  

        if player.face_right : 
            offset = pygame.math.Vector2(-10 , 0) 
        else : 
            offset = pygame.math.Vector2(10 , 0)

        if not self.player_on_the_ground and self.gamers.sprite.on_ground and not self.dusts.sprites(): 
            landing_particle = ParticleEffect( player.rect.midbottom + offset , "land") 
            self.dusts.add(landing_particle)

    def verticle_movement_collusion(self): 
        player = self.gamers.sprite  

        player.apply_gravity()
        for sprite in self.tiles.sprites(): 
            if sprite.rect.colliderect(player.rect): 
                if player.direction.y > 0 : # player is moving to bottom 
                    player.rect.bottom = sprite.rect.top    
                    player.direction.y = 0 # to overcome increment of gravity
                    player.on_ground = True # to configure animations 
                    
                
                
                
                elif player.direction.y < 0 : # player is moving to top 
                        player.rect.top = sprite.rect.bottom  
                        player.direction.y = 0 # to overcome the problem of hanging on the air 
                        player.on_ceiling = True  # to configure animations  



        if player.on_ground and player.direction.y < 0  or player.direction.y > 1 : 
            player.on_ground = False  
            

        if player.on_ceiling and player.direction.y > 0.1 : 
            player.on_ceiling = False 

        
        




        






    def run(self): 

        #self.setup_tiles()

        # tiles 
        self.tiles.update(self.world_shift_vector) # map shifts 
        self.tiles.draw(self.display_surface) 
        self.scroll_x()   

        # dusts 
        self.dusts.update(self.world_shift_vector) 
        self.dusts.draw(self.display_surface) 

        # player  
        self.gamers.update() 
        self.horizontal_movement_collusion()  
        self.get_player_on_ground() # is the player not on the ground before verticle collusions 
        self.verticle_movement_collusion() # because of verticle collusions , direction.y = 0 and on_ground = True 
        self.create_landing_particles() # if the old on_ground and new on_ground values are different and there is no jumping dust execute
        self.gamers.draw(self.display_surface) 
          

        





        
