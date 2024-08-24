import sys
import os
import ctypes
import re

def log_message(message):
    print(message)  # Print to console
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")  # Write to log file

def show_folder_path(path):
    # Use ctypes to show a message box with the folder path
    # ctypes.windll.user32.MessageBoxW(0, f"Folder Path: {path}", "Folder Path", 0)
    rename_files_in_folder(path)


def rename_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    
    # Sort files based on the numeric part after 'lof'
    sorted_files = sorted(files, key=lambda f: int(re.search(r'(\d+)', f).group(1)))
    
    # Rename files
    for old_name in sorted_files:
        match = re.search(r'(\d+)', old_name)
        if match:
            print(f"Renaming File '{old_name}'")
            number = match.group(1)
            new_name = f"{number} {old_name}"
            os.rename(os.path.join(folder_path, old_name), os.path.join(folder_path, new_name))
    
    log_message(f"Files in '{folder_path}' have been renamed.")
    ctypes.windll.user32.MessageBoxW(0, f"Files in '{folder_path}' have been renamed.", "Batch Rename Sucessful", 0)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        log_message(f"Error checking admin rights: {e}")
        return False

def run_as_admin():
    try:
        script = sys.argv[0]
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
    except Exception as e:
        log_message(f"Error running as admin: {e}")


def main():
    try:
        # Check if the script is running as an admin
        # if not is_admin():
        #     run_as_admin()
        #     return
        log_message(f"Start checking the path")

        if len(sys.argv) > 1:
            folder_path = sys.argv[1]
            log_message(f"Folder path: {folder_path}")

            if os.path.isdir(folder_path):
                show_folder_path(folder_path)
            else:
                log_message(f"Invalid folder path.")
        else:
            log_message(f"No folder path provided.")
    
    except Exception as e:
        log_message(f"Unexpected error: {e}")
    
    # Keep the console window open
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
