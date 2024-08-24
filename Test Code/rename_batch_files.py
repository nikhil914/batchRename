import os
import re
import win32com.shell.shell as shell
import ctypes
import sys

def rename_batch_files(folder_path):
    """Renames batch files in the specified folder, ensuring ascending numerical order.

    Args:
        folder_path (str): The path to the folder containing the batch files.
    """

     if not is_admin():
            run_as_admin()
            return

    file_list = os.listdir(folder_path)
    batch_files = [f for f in file_list if f.endswith('.bat')]

    # Extract the numerical part from each file name
    numerical_parts = [re.search(r'\d+', f).group() for f in batch_files]

    # Sort the file list based on the numerical parts
    sorted_files = [f for _, f in sorted(zip(numerical_parts, batch_files))]

    # Rename the files using the sorted order
    for i, file_name in enumerate(sorted_files, start=1):
        new_name = f"{i:03d}_{file_name}"
        try:
            os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_name))
        except Exception as e:
            print(f"Error renaming file {file_name}: {e}")

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

def add_to_context_menu():
    """Adds the batch file renaming function to the Windows context menu."""

    if not is_admin():
        run_as_admin()
        return

    desktop = shell.SHGetDesktopFolder()
    menu_key = desktop.GetUIObjectOfFile(r"C:\")  # Replace with the desired path

    menu_key.QueryInterface(shell.IContextMenu).InvokeCommand(0, 0, None, None)

    input("Press Enter to exit...")

if __name__ == "__main__":
    add_to_context_menu()