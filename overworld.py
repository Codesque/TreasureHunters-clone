import pygame

from settings import SCREEN_WIDTH   
pygame.init()
from game_data import levels   
from decorations import Sky , Clouds


class Node(pygame.sprite.Sprite): 

    def __init__(self,pos ,status : str , icon_speed : int , level = 0 , width = 100 , height = 80) -> None:
        super().__init__()  
        self.animations = levels[level]["overworld"]["node_graphics"]  
        self.animation_speed = 0.2 
        self.frame_counter = 0 
        self.image = self.animations[self.frame_counter]  
        self.status = status 

        self.rect = self.image.get_rect(center = pos)  
        # detection of the location of moving object 
        self.detection_size = (1) * icon_speed # size should be depend on the speed of the selection bar because overjumps could happen
        self.detection_zone = pygame.Rect(self.rect.centerx - (self.detection_size/2 ) , self.rect.centery  - (self.detection_size/2) ,self.detection_size , self.detection_size)  
        

    def animate(self): 
        self.frame_counter += self.animation_speed 
        if self.frame_counter >= len(self.animations): 
            self.frame_counter = 0 

        self.image = self.animations[int(self.frame_counter)]    

    def update(self): 
        if self.status == "available":
            self.animate()   
        elif self.status == "locked": 
            tint_img = self.image.copy() 
            tint_img.fill('black' ,None , pygame.BLEND_RGBA_MULT) 
            self.image.blit(tint_img , (0,0))


    

class Icon(pygame.sprite.Sprite): 
    def __init__(self , pos , icon_speed = 8) -> None:
        super().__init__()  
        self.pos = pos
        self.image = pygame.image.load("../Tiled/graphics/treasure_hunters/overworld/hat.png").convert_alpha() 
        self.rect = self.image.get_rect(center = pos)  
        
    def update(self) -> None:
        self.rect.center = self.pos 


class Overworld : 

    def __init__(self , start_level : int , max_level : int , display_surface : pygame.Surface , create_level : object) -> None:
        

        self.create_level = create_level

        self.current_level = start_level 
        self.max_level = max_level 
        self.display_surface = display_surface    
        self.speed = 8 
        self.setup_nodes()  
        self.setup_icon()
        # movement logic 
        self.moving = False 
        self.moving_direction = pygame.math.Vector2(0,0)  

        # background 
        self.sky = Sky(8 , "overworld") 
        self.clouds = Clouds(400 ,SCREEN_WIDTH ,20 , "overworld")
        





    def setup_nodes(self):  
        self.nodes = pygame.sprite.Group()
        for index , node_data in enumerate(levels.values()):  
            if self.max_level >= index+1:
                new_node = Node(node_data["overworld"]["node_pos"] , "available" , self.speed ,index+1) 
                self.nodes.add(new_node) 
            else : 
                new_node = Node(node_data["overworld"]["node_pos"] , "locked" , self.speed , index+1)  
                self.nodes.add(new_node)  

    def draw_paths(self):  
        points = [point["overworld"]["node_pos"] for index , point in enumerate(levels.values()) if self.max_level >= index+1  ] 
        if self.max_level > 1 :
            pygame.draw.lines(self.display_surface , '#a04f45' , False , points ,6)  


    def setup_icon(self): 
        self.icon = pygame.sprite.GroupSingle() 
        self.icon.add(Icon(self.nodes.sprites()[self.current_level-1].rect.center))  

    def get_moving_direction(self , type : str): 
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)  
        if type == "right": 
             end = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        elif type == "left": 
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level-2].rect.center) 
            
        return (end - start).normalize()

    def input(self): 
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_d] and self.current_level < self.max_level:
                self.moving_direction = self.get_moving_direction("right")
                self.current_level += 1   
                self.moving = True 

                
            elif keys[pygame.K_a] and self.current_level > 1 :    
                self.moving_direction = self.get_moving_direction("left")
                self.current_level -= 1 
                self.moving = True   

            elif keys[pygame.K_SPACE]:  
                self.create_level( self.current_level) 
                


                
    def update_icon_pos(self):  

        if self.moving and self.moving_direction:
            self.icon.sprite.pos += self.moving_direction * self.speed  
            target_node = self.nodes.sprites()[self.current_level - 1]  
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos): 
                self.moving = False 
                self.moving_direction = pygame.math.Vector2(0,0) 
                 

        





        
    def run(self):  
        
        self.input() 
        self.icon.update()  
        self.update_icon_pos()
        self.nodes.update()
         
        self.sky.draw(self.display_surface) 
        self.clouds.draw(self.display_surface , pygame.math.Vector2(0,0))
        self.draw_paths()
        self.nodes.draw(self.display_surface)  
        self.icon.draw(self.display_surface)
         
