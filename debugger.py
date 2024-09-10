import pygame as pg 
import os

def save_to_file(obj,filename):
    with open(filename,'w') as f:
        f.writelines(str(obj))