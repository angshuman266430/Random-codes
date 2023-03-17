import os

def find_file(target_file, search_path):
    for root, dirs, files in os.walk(search_path):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

target_file = "RAS_HDF_WaterSurface_Extract.py"
search_path = "Z:\\"  # Change this path to the directory you want to start the search from

file_path = find_file(target_file, search_path)

if file_path:
    print(f"File found at: {file_path}")
else:
    print("File not found")
