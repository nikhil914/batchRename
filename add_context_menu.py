import winreg as reg
import os
import sys

def add_context_menu_entry():
 # Path to the Python executable and script
    script_path = os.path.abspath("print_folder_path.py")  # Get the absolute path to the Python script
    python_exe = sys.executable  # This will get the current Python executable path

        # Define registry key paths and values

    key_path = r"Directory\shell\BatchRename"
    command_key_path = r"Directory\shell\BatchRename\command"

    # Path to the icon (you can use any .ico file or a file with an embedded icon like .exe or .dll)
    icon_path = os.path.abspath("icon.ico")  # Replace with the path to your icon file

   
    # Debugging output to ensure paths are correct
    print(f"Python Executable: {python_exe}")
    print(f"Script Path: {script_path}")
    print(f"Icon Path: {icon_path}")

    # Create the registry key and set values
    try:
        # Open or create the registry key for the context menu
        # with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path) as key:
        #     winreg.SetValue(key, '', winreg.REG_SZ, 'Print Folder Pathxxx')
        
        # # Open or create the registry key for the command
        # with winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_key_path) as command_key:
        #     command = f'"{python_exe}" "{script_path}" "%V"'
        #     winreg.SetValue(command_key, '', winreg.REG_SZ, command)


        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, key_path) as reg_key:
            reg.SetValue(reg_key, "", reg.REG_SZ, "Batch Rename by Nik")
            # Set the icon for the context menu entry
            reg.SetValueEx(reg_key, "Icon", 0, reg.REG_SZ, icon_path)
        
        # Set the command to run our script with the selected folder as an argument
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, command_key_path) as reg_key:
            command = f'"{python_exe}" "{script_path}" "%1"'
            reg.SetValue(reg_key, "", reg.REG_SZ, command)
        
        print("Context menu entry added successfully!")
    
    except Exception as e:
        print(f"Error adding context menu entry: {e}")

if __name__ == '__main__':
    add_context_menu_entry()
