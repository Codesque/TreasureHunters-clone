import pygame 

GRAVITY_CONSTANT = 0.8



def gravitation(target:pygame.sprite.Sprite): 
    
    gravity_force = pygame.math.Vector2( 0 , target.mass * GRAVITY_CONSTANT) 
    # target.speed.y += GRAVITY_CONSTANT # If the object is not on the ground , uncomment this 
    target.speed += gravity_force