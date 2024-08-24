import winreg as reg

def remove_from_context_menu():
    key_path = r"Directory\shell\BatchRename"
    
    try:
        # Delete the registry key for the context menu item
        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_path + r"\command")
        reg.DeleteKey(reg.HKEY_CLASSES_ROOT, key_path)
        
        print("Successfully removed from the context menu.")
    
    except Exception as e:
        print(f"Failed to remove from context menu: {e}")

if __name__ == "__main__":
    remove_from_context_menu()
