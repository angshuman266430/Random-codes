import os
import fnmatch

root_dir = r"Z:\Y2022"
folder_to_search = "Calculated Layers"

for dirpath, dirnames, filenames in os.walk(root_dir):
    if os.path.basename(dirpath) == folder_to_search:
        for filename in filenames:
            print(os.path.join(dirpath, filename))
