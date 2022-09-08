import pygame
from player import Player 
from tile import Tile 
from settings import * 



class Level :  

    def __init__(self , level_data , surface) -> None: 
        self.display_surface = surface 
        self.level_data = level_data  
        self.setup_level(level_data) 
        self.world_shift_vector = pygame.math.Vector2(0,0)

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
                    self.player = Player(pos)  
                    self.gamers.add(self.player) 

                    
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

        player.rect.centerx += player.speed.x * player.direction.x  

        for sprite in self.tiles.sprites(): 

            if sprite.rect.colliderect(player.rect): 
                if player.direction.x < 0 : # player is moving to left 
                    player.rect.left = sprite.rect.right 

                elif player.direction.x > 0 : # player is moving to right 
                    player.rect.right = sprite.rect.left 



    def verticle_movement_collusion(self): 
        player = self.gamers.sprite  

        player.apply_gravity()
        for sprite in self.tiles.sprites(): 
            if sprite.rect.colliderect(player.rect): 
                if player.direction.y > 0 : # player is moving to bottom
                    player.rect.bottom = sprite.rect.top  
                    player.direction.y = 0 # to overcome increment of gravity
                
                
                
                elif player.direction.y < 0 : # player is moving to top 
                        player.rect.top = sprite.rect.bottom 
                        player.direction.y = 0 # to overcome the problem of hanging on the air




        






    def run(self): 

        # tiles 
        self.tiles.update(self.world_shift_vector) # map shifts 
        self.tiles.draw(self.display_surface) 
        self.scroll_x()  

        # player  
        self.gamers.update() 
        self.horizontal_movement_collusion() 
        self.verticle_movement_collusion() 
        self.gamers.draw(self.display_surface) 
          
        





        
