import pygame 


class Player(pygame.sprite.Sprite): 

    def __init__(self , pos) -> None:
        super().__init__() 
        self.sprites = {}   
        self.v0 = 1
        self.speed = pygame.math.Vector2(self.v0 , self.v0) 

        self.direction = pygame.math.Vector2(0,0)     

        self.dir_changed = False 

        # Animation Speeds
        self.animation_speed = {} 
        self.animation_speed["run"] = 0.02 
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


    def animate(self):  

        
        self.frame_counter += self.animation_speed[self.status] 
        if self.frame_counter > len(self.sprites[self.status]) - 1: 
            self.frame_counter = 0 

        

        self.image = pygame.image.load(self.sprites[self.status][round(self.frame_counter)]).convert_alpha()  
        if self.dir_changed: 
            self.image = pygame.transform.flip(self.image , True , False)
            



    def get_input(self): 

            keys = pygame.key.get_pressed() 

            if keys[pygame.K_d]: 
                self.direction.x = 1   
                self.dir_changed = False 
                self.status = "run" 
                self.animate()

            elif keys[pygame.K_a]: 
                self.direction.x = -1   
                self.dir_changed = True 
                self.status = "run" 
                self.animate() 
                

            else : 
                self.direction.x = 0   
                self.status = "idle" 
                self.animate()


    def update(self): 
        self.get_input()   
        self.direction.x *= self.speed.x
        self.direction.y *= self.speed.y 
        self.rect.center += self.direction 



    



        
        