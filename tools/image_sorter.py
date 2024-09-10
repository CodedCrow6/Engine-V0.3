import os
import shutil

def group_images_by_prefix(directory):
    # List to hold the file names
    file_names = []

    # Get all image files from the directory
    for file in os.listdir(directory):
        # Only consider files that are images (in this case, with .png extension)
        if file.endswith('.png'):
            file_names.append(file)

    # Dictionary to store grouped file names
    grouped_files = {}

    # Loop through the list and group files by the first number (before '-')
    for file in file_names:
        # Dynamically split at the first occurrence of '-' and take the first part as the key
        prefix = file.split('-')[0]
        # Add the file to the group corresponding to the prefix
        if prefix not in grouped_files:
            grouped_files[prefix] = []
        grouped_files[prefix].append(file)

    return grouped_files  # Return a dictionary

def move_files_to_groups(directory):
    # Get the grouped files based on prefix
    grouped_files = group_images_by_prefix(directory)

    # Iterate over each group
    for prefix, files in grouped_files.items():  # Use .items() for dictionary
        # Create a new folder for each group (if it doesn't already exist)
        group_folder = os.path.join(directory, prefix)
        os.makedirs(group_folder, exist_ok=True)

        # Move each file into the respective folder
        for file in files:
            src = os.path.join(directory, file)  # Source path
            dst = os.path.join(group_folder, file)  # Destination path
            shutil.move(src, dst)
            print(f'Moved {file} to {group_folder}')


