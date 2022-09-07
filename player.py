import pygame

from physics import gravitation


class Player(pygame.sprite.Sprite): 

    def __init__(self , pos) -> None:
        super().__init__() 
           
        self.v0 = 1
        self.speed = pygame.math.Vector2(self.v0 , self.v0) 
        self.direction = pygame.math.Vector2(0,0)     
        self.dir_changed = False  

        self.mass = 1 
        self.neg_mass = self.mass * -1



        self.sprites = {}
        # Animation Speeds
        self.animation_speed = {} 
        self.animation_speed["run"] = 0.02 
        self.animation_speed["idle"] = 0.02 
        self.animation_speed["jump"] = 0.001



        # loading animations
        self.sprites["idle"] = [] 
        [self.sprites["idle"].append(
            "assets/Treasure Hunters/Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/01-Idle/Idle 0"+str(i+1)+".png") 
            for i in range(5)] 
         

        self.sprites["run"] = []  
        [self.sprites["run"].append(
            "assets/Treasure Hunters/Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/02-Run/Run 0"+str(i+1)+".png") 
            for i in range(6)]  

        self.sprites["jump"] = [] 
        [self.sprites["jump"].append("assets/Treasure Hunters/Captain Clown Nose/Sprites/Captain Clown Nose/Captain Clown Nose without Sword/03-Jump/Jump 0"+str(i+1)+".png")
        for i in range(3) ] 
        

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
            



    def jump(self): 
        if self.status == "jump": 
            self.direction.y = -1 
            try:
                F_net = 0.5 * self.mass * (self.speed.y ** 2)   
            finally: 
                print(self.speed)

            self.speed -= pygame.math.Vector2(0 , F_net) 
            
            if self.speed.y < 0 :  
                self.direction.y = -1 
            
            if self.speed.y <= (-self.v0 -1): 
                self.status = "idle" 
                self.speed.y = self.v0   
                self.direction.y = 1





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

            if keys[pygame.K_w]:
                
                if self.status != "jump":
                    self.status = "jump"  
                self.animate() 



    def update(self): 
        


        if self.status != "jump": 
            gravitation(self) 
        
        
        
        self.get_input()   
        self.direction.x *= self.speed.x
        self.direction.y *= self.speed.y 
        self.rect.center += self.direction 



    



        
        