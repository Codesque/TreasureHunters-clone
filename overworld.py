import pygame  
from game_data import levels

class Node(pygame.sprite.Sprite): 

    def __init__(self,pos ,status : str , width = 100 , height = 80) -> None:
        super().__init__() 
        self.image = pygame.Surface((width , height))  
        self.status = status 
        if self.status == "available": 
            self.image.fill('red') 

        elif self.status == "locked": 
            self.image.fill('grey')

        self.rect = self.image.get_rect(center = pos) 

class Icon(pygame.sprite.Sprite): 
    def __init__(self , pos) -> None:
        super().__init__()  
        self.pos = pos
        self.image = pygame.Surface([20,20]) 
        self.image.fill('blue') 
        self.rect = self.image.get_rect(center = pos) 

    def update(self) -> None:
        self.rect.center = self.pos 


class Overworld : 

    def __init__(self , start_level : int , max_level : int , display_surface : pygame.Surface) -> None:
        
        self.current_level = start_level 
        self.max_level = max_level 
        self.display_surface = display_surface   
        self.setup_nodes()  
        self.setup_icon()

        # movement logic 
        self.moving = False 
        self.moving_direction = pygame.math.Vector2(0,0) 
        self.speed = 0.1


    def setup_nodes(self):  
        self.nodes = pygame.sprite.Group()
        for index , node_data in enumerate(levels.values()):  
            if self.max_level >= index+1:
                new_node = Node(node_data["node_pos"] , "available") 
                self.nodes.add(new_node) 
            else : 
                new_node = Node(node_data["node_pos"] , "locked") 
                self.nodes.add(new_node)  

    def draw_paths(self):  
        points = [point["node_pos"] for index , point in enumerate(levels.values()) if self.max_level >= index+1  ] 
        pygame.draw.lines(self.display_surface , 'red' , False , points ,6) 


    def setup_icon(self): 
        self.icon = pygame.sprite.GroupSingle() 
        self.icon.add(Icon(self.nodes.sprites()[self.current_level-1].rect.center))  

    def get_moving_direction(self , type : str): 
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center) 
        end = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center) 

        if type == "right": 
            return (end - start) 
        elif type == "left": 
            return (start - end)

    def input(self): 
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_d] and self.current_level <= self.max_level:
                self.moving_direction = self.get_moving_direction("right")
                self.current_level += 1   
                self.moving = True 

                
            elif keys[pygame.K_a] and self.current_level >= 1 :    
                self.moving_direction = self.get_moving_direction("left")
                self.current_level -= 1 
                self.moving = True    

                
    def update_icon_pos(self): 
        self.icon.sprite.pos += self.moving_direction * self.speed 





        
    def run(self):  
        self.input() 
        self.update_icon_pos() 
        self.icon.update()
        self.nodes.draw(self.display_surface)  
        self.draw_paths() 
        self.icon.draw(self.display_surface)
