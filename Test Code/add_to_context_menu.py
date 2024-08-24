import os
import re
import sys
import winreg as reg
import ctypes

def rename_files_in_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        
        # Sort files based on the numeric part after 'lof'
        sorted_files = sorted(files, key=lambda f: int(re.search(r'(\d+)', f).group(1)))
        
        # Rename files
        for old_name in sorted_files:
            match = re.search(r'(\d+)', old_name)
            if match:
                print(f"Files going to renamed '{old_name}'")
                number = match.group(1)
                new_name = f"{number} {old_name}"
                os.rename(os.path.join(folder_path, old_name), os.path.join(folder_path, new_name))
        
        print(f"Files in '{folder_path}' have been renamed.")
    except Exception as e:
        print(f"Error during renaming: {e}")

def add_to_context_menu():
    script_path = os.path.abspath(__file__)
    python_executable = os.path.abspath(sys.executable)  # Get the Python executable path

    # Registry paths for context menu
    key_path = r"Directory\shell\BatchRename"
    command_key_path = r"Directory\shell\BatchRename\command"
    
    try:
        # Create a new key for our context menu item
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path) as reg_key:
            reg.SetValue(reg_key, "", reg.REG_SZ, "Batch Rename Files")
        
        # Set the command to run our script with the selected folder as an argument
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_key_path) as reg_key:
            command = f'"{python_executable}" "{script_path}" "%1"'
            reg.SetValue(reg_key, "", reg.REG_SZ, command)
        
        print("Successfully added to the context menu.")
        
    except Exception as e:
        print(f"Failed to add to context menu: {e}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin rights: {e}")
        return False

def run_as_admin():
    try:
        script = sys.argv[0]
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
    except Exception as e:
        print(f"Error running as admin: {e}")

def main():
    try:
        # Debugging statement
        print(f"Arguments received: {sys.argv}")
        print(f"Number of arguments: {len(sys.argv)}")
        
        if not is_admin():
            run_as_admin()
            return
        
        if len(sys.argv) > 1:
            folder = sys.argv[1]  # Get the folder path from the command line
            print(f"Renaming files in folder: {folder}")
            
            # Check if folder exists and is valid
            if os.path.isdir(folder):
                rename_files_in_folder(folder)
            else:
                print(f"The path '{folder}' is not a valid directory.")
        else:
            add_to_context_menu()
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Keep the console window open
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
