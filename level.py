import pygame 
import pytmx  
from game_data import levels

from player import Player

from tile import Coins, GrassTile, Tile, TreeObject 
from settings import *  
from particles import ParticleEffect , ExplosionEffect 

from pytmx import load_pygame
from enemy import Zombies , Constraints
from decorations import Sky , Water , Clouds



class Level :  

    def __init__(self  , surface : pygame.Surface ,current_level : int , create_overworld : object  , change_coin_amount : object , change_health : object) -> None: 
        
        self.create_overworld = create_overworld  
        self.change_coin_amount = change_coin_amount 
        self.change_health = change_health

        self.level_path = levels[current_level]["path"]  
        self.current_level = current_level  
        self.unlock_level = levels[current_level]["overworld"]["unlock"]
        
        self.display_surface = surface  
        self.w ,self.h = self.display_surface.get_width() , self.display_surface.get_height()  
        #self.setup_level(level_data)  
        self.setup_tiles(self.level_path) 
        
        self.world_shift_vector = pygame.math.Vector2(0,0) 
        self.current_x = 0 

        self.dusts = pygame.sprite.GroupSingle() 
        self.player_on_the_ground = False  

        # decorations 
        self.sky = Sky(6)  
        self.water = Water(SCREEN_HEIGHT-40 , 2 *LEVEL_WIDTH)  
        self.clouds = Clouds(400 , LEVEL_WIDTH ,30)




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
        self.background_tiles = pygame.sprite.Group()  
        self.coins = pygame.sprite.Group()
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
        self.background_tiles = pygame.sprite.Group()  
        self.crates = pygame.sprite.Group()   
        self.coins = pygame.sprite.Group() 
        self.enemies = pygame.sprite.Group() 
        self.explosions = pygame.sprite.Group()  
        self.constraints = pygame.sprite.Group()
        self.tmx_data = load_pygame("../Tiled/levels/treasure_hunters1.tmx")   
        
        """
        if self.once : 
            for layer in self.tmx_data.visible_layers : 
                print(layer.name) 
            self.once = False  
        """ 
        self.gamers = pygame.sprite.GroupSingle()  

        



        for layer in self.tmx_data.visible_layers : 

            #print(layer.name)
            if layer.name == "terrain" : 
                for x , y , surface in layer.tiles(): 
                    pos = (x * TILE_SIZE , y * TILE_SIZE)
                    new_terrain = Tile(pos ,surface) 
                    self.tiles.add(new_terrain)    

            if layer.name == "crates": 

                for x , y , surface in layer.tiles():  
                    pos = (x * TILE_SIZE , y * TILE_SIZE) 
                    new_crate = Tile(pos , surface , 0 , 25) 
                    self.tiles.add(new_crate)
                    


            if layer.name == "grass": 
                for x , y , surface in layer.tiles(): 
                    pos = (x * TILE_SIZE , y * TILE_SIZE) 
                    new_grass = GrassTile(pos , surface) 
                    self.background_tiles.add(new_grass)  

        print(self.tmx_data.layernames)


        # Spawn Points 
        spawn_layer = self.tmx_data.get_layer_by_name('spawn_point')   
        for obj in spawn_layer : 
            
            pos = (obj.x , obj.y) 
            new_player = Player(pos , self.display_surface , self.create_jump_dust_particle , self.change_health)  
            self.gamers.add(new_player)   

        checkpoint_layer = self.tmx_data.get_layer_by_name('ending_point') 
        for obj in checkpoint_layer: 
            pos = (obj.x , obj.y)  
            hat_img = pygame.image.load("../Tiled/graphics/treasure_hunters/level_1/character/hat.png") 
            self.goal = Tile(pos , hat_img) 
            self.background_tiles.add(self.goal)  

        # BackGround Palms
        bg_palms_layer = self.tmx_data.get_layer_by_name('bg_palms') 
        for obj in bg_palms_layer:  
            pos = (obj.x , obj.y) 
            new_bg_palm = TreeObject(pos , "palm_bg") 
            self.background_tiles.add(new_bg_palm)  


        # ForeGround Palms 
        fg_palms_layer = self.tmx_data.get_layer_by_name('fg_palms')
        for obj in fg_palms_layer: 
            type1 = "large_palm" 
            type2 = "small_palm"
            if obj.name == type1:  
                pos = (obj.x , obj.y) 
                new_large_palm = TreeObject(pos , "palm_large") 
                self.tiles.add(new_large_palm)  

            elif obj.name == type2:  
                pos = (obj.x , obj.y) 
                new_small_palm = TreeObject(pos , "palm_small") 
                self.tiles.add(new_small_palm)   


        gold_coins_layer = self.tmx_data.get_layer_by_name("gold_coins") 
        for x , y , surface in gold_coins_layer.tiles(): 
            pos = (x * TILE_SIZE , y * TILE_SIZE) 
            new_gold_coin = Coins(pos , "gold") 
            self.coins.add(new_gold_coin)  

        silver_coins_layer = self.tmx_data.get_layer_by_name("silver_coins")  
        for x , y , surface in silver_coins_layer.tiles(): 
            pos = (x * TILE_SIZE , y * TILE_SIZE) 
            new_silver_coin = Coins(pos , "silver") 
            self.coins.add(new_silver_coin)  


        enemy_layer = self.tmx_data.get_layer_by_name("enemies") 
        for x , y , surface in enemy_layer.tiles(): 
            pos = (x * TILE_SIZE , y * TILE_SIZE)  
            new_enemy = Zombies(pos) 
            self.enemies.add(new_enemy) 

        constraints_layer = self.tmx_data.get_layer_by_name("constraints") 
        for x , y , surface in constraints_layer.tiles():  
            pos = (x * TILE_SIZE , y * TILE_SIZE)  
            new_constraint =   Constraints(surface , pos)  
            self.constraints.add(new_constraint)
            
    def coinCollusion(self): 
        player = self.gamers.sprite 
        collided_coins = pygame.sprite.spritecollide(player , self.coins , True)  
        if collided_coins: 
            for coin in collided_coins : 
                if coin.type == "gold" : self.change_coin_amount(5) 
                elif coin.type == "silver" : self.change_coin_amount(1)

    def zombieCollusion(self): 

       for zombie in self.enemies.sprites(): 

            if pygame.sprite.spritecollide(zombie , self.constraints , False): 
                zombie.turn_from_corner() 
                  
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

    def create_explosion(self):  

        player = self.gamers.sprite  

        for zombie in self.enemies.sprites(): 
            if player.rect.colliderect(zombie.rect):
                if abs(player.rect.bottom - zombie.rect.top) <= COLLUSION_TOLERANCE and (player.status == "fall"):  
                    zombie_pos = zombie.rect.center
                    zombie.kill()  
                    explosion = ExplosionEffect(zombie_pos)  
                    player.direction.y = -15
                    self.explosions.add(explosion)  

                else : 
                    player.get_damage()

                
                        
                    
        
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

    def input(self): 

        keys = pygame.key.get_pressed() 

        if keys[pygame.K_o]: 
            self.create_overworld(self.current_level ,self.unlock_level) #unlocks the next level 
            # if you change the self.unlock part to 0 , no level will be unlocked 

    def check_death(self): 
        if self.gamers.sprite.rect.top > SCREEN_HEIGHT : 
            #self.create_overworld(self.current_level , 0)   
            self.change_health(-999)


    def check_win(self): 
        if self.gamers.sprite.rect.colliderect(self.goal.rect): 
            self.create_overworld(self.current_level , self.unlock_level)

        
    def run(self): 

        #self.setup_tiles() 

        self.input() 
        self.check_win()
        self.check_death() 
        #decorations
        self.sky.draw(self.display_surface)  
        self.clouds.draw(self.display_surface , self.world_shift_vector)


        #background_tiles which has no collusions 
        self.background_tiles.update(self.world_shift_vector) 
        self.background_tiles.draw(self.display_surface)

        # tiles - ones which has collusions  
        self.tiles.update(self.world_shift_vector) # map shifts 
        self.tiles.draw(self.display_surface) 
        self.scroll_x()   
 


        #coins
        self.coinCollusion()
        self.coins.update(self.world_shift_vector) 
        self.coins.draw(self.display_surface)

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

        # zombies 
        self.zombieCollusion()
        self.create_explosion() 
        self.enemies.update(self.world_shift_vector) 
        self.enemies.draw(self.display_surface)
        self.explosions.draw(self.display_surface) 
        self.explosions.update(self.world_shift_vector) 
        self.constraints.update(self.world_shift_vector)  

        # decoration:water 
        self.water.draw(self.display_surface , self.world_shift_vector)

          

        





        
