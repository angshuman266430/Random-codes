import os

# Set the target directory
search_path = r"S:\For_Angshuman\LWI_2024\EnDMC_Test\EnDMC_Test_Oct_2024\Original_consultant_model\EC_ELouisianaCoastal_HEC-RAS_Model"

# Output file to write all found file names and their relative paths
output_file = "file_list.txt"

# Open the output file for writing
with open(output_file, "w") as file:
    # Walk through all directories and files within the search path
    for root, dirs, files in os.walk(search_path):
        for filename in files:
            # Get the relative path of the file
            relative_path = os.path.relpath(os.path.join(root, filename), search_path)
            # Write the relative path to the output file
            file.write(f"{relative_path}\n")

print(f"File names and relative paths saved to {output_file}")
