import pygame 

class Tile(pygame.sprite.Sprite): 

    def __init__(self, pos , size) -> None:
        super().__init__() 
        self.image = pygame.Surface((size,size)) 
        self.image.fill((204,102,90)) 
        self.rect = self.image.get_rect(topleft = pos)  
        self.tile_shift_vector = pygame.math.Vector2(0,0) 


    def shift_vector(self): 
        self.rect.center += self.tile_shift_vector 

    def shift_x(self , x_shift): 
        self.rect.centerx += x_shift  

    def update(self , shift_vector : pygame.math.Vector2) -> None:  
        self.tile_shift_vector = shift_vector
        self.shift_vector()
        

        