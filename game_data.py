import pygame
from support import import_files  
pygame.init()  
screen = pygame.display.get_surface()

main_path = "../Tiled/graphics/treasure_hunters/overworld/"

level_1 = {"node_graphics": import_files(main_path + "0") ,"node_pos" : (110,400) , "content":"this is level 1" , 'unlock':2} 
level_2 = {"node_graphics": import_files(main_path + "1") ,"node_pos" : (300,220) , "content":"this is level 2" , 'unlock':3}
level_3 = {"node_graphics": import_files(main_path + "2") ,"node_pos" : (480,610) , "content":"this is level 3" , 'unlock':4}
level_4 = {"node_graphics": import_files(main_path + "3") ,"node_pos" : (680,440) , "content":"this is level 4" , 'unlock':5}
level_5 = {"node_graphics": import_files(main_path + "4") ,"node_pos" : (790,200) , "content":"this is level 5" , 'unlock':6} 
level_6 = {"node_graphics": import_files(main_path + "5") ,"node_pos" : (1030,350) , "content":"this is level 6" , 'unlock':6} 


levels = {
    1: {"overworld" : level_1 , "path": "../Tiled/levels/treasure_hunters1.tmx"},
    2:{"overworld" : level_2 , "path": "../Tiled/levels/treasure_hunters2.tmx"},
    3:{"overworld" : level_3 , "path": "../Tiled/levels/treasure_hunters3.tmx"},
    4:{"overworld" : level_4 , "path": "../Tiled/levels/treasure_hunters4.tmx"}, 
    5:{"overworld" : level_5 , "path": "../Tiled/levels/treasure_hunters5.tmx"},
    6:{"overworld" : level_6 , "path": "../Tiled/levels/treasure_hunters6.tmx"}
} 

