import pygame 
pygame.init()
pygame.font.init()
class UI : 

    def __init__(self , display_surface : pygame.Surface ) -> None: 


        self.display_surface = display_surface


        root_path = "../Tiled/graphics/treasure_hunters/ui/" 

        # health_bar 
        self.health_bar = pygame.image.load(root_path+"health_bar.png")  
        self.startingOf_hbar = (54,39) 
        self.hbar_width , self.hbar_height = 152 , 4 
        


        
        # coin 
        self.coin = pygame.image.load(root_path+"coin.png") 
        self.coin_rect = self.coin.get_rect(topleft = (50,61)) # we use rects for coin because we want it's center to have the 
                                                        # same y axis with the center of the text surface   
        self.font = pygame.font.Font(root_path + "ARCADEPI.TTF" , 20)    
        

        
 
                                                          


    def show_health(self , current : int  , full : int): 
        self.display_surface.blit(self.health_bar , (20,10))   
        current_ratio = current/full 
        current_hbar_w = self.hbar_width * current_ratio 
        hbar_rect = pygame.Rect(self.startingOf_hbar , (current_hbar_w , self.hbar_height) )  
        pygame.draw.rect(self.display_surface , "#dc4949" , hbar_rect)



    def show_coins(self , amount , off_x = 40):  

        # coin text
        text_surf = self.font.render("x" + str(amount) ,False , "#33323d") 
        text_center = self.coin_rect.center + pygame.math.Vector2(off_x , 0)
        text_rect = text_surf.get_rect(center = text_center ) 
        
        # draw surfaces 
        self.display_surface.blit(self.coin , self.coin_rect)  
        self.display_surface.blit(text_surf , text_rect) 


    
        