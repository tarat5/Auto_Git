import tkinter as tk
from tkinter import filedialog
import os
import json

# Function to open the file explorer and get the folder path
def select_folder():
    # Open the file dialog to select a folder
    folder_selected = filedialog.askdirectory(title="Select a Folder")
    
    if folder_selected:
        # Get the last directory name from the folder path
        last_directory = os.path.basename(folder_selected)
        
        # Define the path to the JSON file that will store the directories
        json_file_path = "directories.json"
        
        # Check if the JSON file exists and load its content
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                directories = json.load(json_file)
        else:
            directories = []

        # Check if the folder path is already in the directories list
        if folder_selected not in directories:
            # If not, append the new folder to the list
            directories.append(folder_selected)
            print(f"New directory added: {folder_selected}")
        else:
            print(f"Directory already exists in the list: {folder_selected}")

        # Save the updated list back to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(directories, json_file, indent=4)

        print(f"Directories saved to {json_file_path}")
    else:
        print("No folder selected.")

# Create a basic Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the main window since we only need the file dialog

# Call the function to select a folder
select_folder()
