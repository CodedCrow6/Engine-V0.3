import os


def get_anim_lists(directory_path):

    # Initialize the master list
    master_list = []

    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file is an image (assuming .png extension)
        if filename.endswith(".png"):
            # Extract the number from the filename before the first '-'
            num = filename.split('-')[0].lstrip('_')
            # Convert the number to an integer
            num = int(num)
            # Find the list in the master list that corresponds to this number
            for animation in master_list:
                if num in [int(img.split('-')[0].lstrip('_')) for img in animation]:
                    animation.append(filename)
                    break
            # If no matching list is found, create a new list
            else:
                master_list.append([filename])
    return master_list

if __name__=="__main__":
    print(get_anim_lists('C:/Users/CDE.RG/Documents/Programming projects/Python Scripts/engine_v0.3/assets/graphics/characters/Vegeta/model'))
