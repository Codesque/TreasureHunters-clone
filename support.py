import os 
from os import walk  
import pygame 

pygame.init()
def import_files(fpath : str ):  
    if fpath[-1] != "/": fpath += "/"

    for fpath , _ , fnames in walk(fpath):  
        return [ pygame.image.load(os.path.join(fpath , sprite )).convert_alpha() for sprite in fnames ]
        
#print(import_files("graphics/character/run/")) # -------->> ('fpath','foldernames','filenames')
#('graphics/character/run', [], ['Run Sword 01.png', 'Run Sword 02.png', 'Run Sword 03.png', 'Run Sword 04.png', 'Run Sword 05.png', 'Run Sword 06.png'])