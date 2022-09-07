import pygame

level_map = [ 
"..............................",
"........XX....................", 
"XX..................XX........",
"XX.........P....X.........XX..",
"XXXX......XXX.................",
"XXXX............XX.....XXX....",
"XX............XX......X.XX....",
".........X..XXXX.....X..XX....",
"........XX..XXXX....XX..XX....",
"......XXXX..XXXX..XXXX..XX....",
"XXXXXXXXXX..XXXX..XXXX..XX...."
] 

TILE_SIZE = 64 
SCREEN_WIDTH = 1200 
SCREEN_HEIGHT = len(level_map) * TILE_SIZE # 704  

CAMERA_BORDERS = {
    "left" : SCREEN_WIDTH//4 , 
    "right" : SCREEN_WIDTH//4 , 
    "top" : SCREEN_HEIGHT//4 , 
    "bottom": SCREEN_HEIGHT//4
}


pygame.font.init()
font = pygame.font.Font(None , 30)

def debug(info , y = 10 , x = 10):  
    display_surface = pygame.display.get_surface() 
    debug_surf = font.render(str(info) , True , 'White') 
    debug_rect = debug_surf.get_rect(topleft = (x,y) ) 
    pygame.draw.rect(display_surface , 'Black' , debug_rect)  
    display_surface.blit(debug_surf , debug_rect)
