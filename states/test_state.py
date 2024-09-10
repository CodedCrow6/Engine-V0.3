import pygame as pg 
 
assets_dir = 'C:/Users/CDE.RG/Documents/Programming projects/Python Scripts/engine_v0.3/assets/graphics/characters'
def load_sprites():
    cache = []
    for animation in animation_lists:
        print(animation)
        temp_list = []
        for file_name in animation:
            image = pg.image.load(f'{assets_dir}/{file_name}').convert_alpha()
            temp_list.append(image)
        cache.append(temp_list)
    print(cache)
    return cache
    
    
load_sprites()