import os
import re
import sys

def rename_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    
    # Sort files based on the numeric part after 'lof'
    sorted_files = sorted(files, key=lambda f: int(re.search(r'(\d+)', f).group(1)))

    # Rename files
    for old_name in sorted_files:
        match = re.search(r'(\d+)', old_name)
        if match:
            number = match.group(1)
            new_name = f"{number} {old_name}"
            os.rename(os.path.join(folder_path, old_name), os.path.join(folder_path, new_name))

    print(f"Files in '{folder_path}' have been renamed.")

if __name__ == "__main__":
    folder = sys.argv[1]  # Get the folder path from the command line
    rename_files_in_folder(folder)
