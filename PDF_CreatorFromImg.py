from PIL import Image
import os

# Directory path
dir_path = "Z:\\Greenbelt\\Observation\\MRMS vs MRMS Cal vs AORC vs Old vs Observed Comparison\\Plots"

# Get all .png files from the directory
png_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.png')]

# Ensure there are images to process
if not png_files:
    print("No .png files found in the specified directory!")
    exit()

# Sort the files in order you want them in the PDF (modify if needed)
png_files.sort()

# Create a list to store the images
images = []

# Open and append each image to the images list
for png_file in png_files:
    img_path = os.path.join(dir_path, png_file)
    with Image.open(img_path) as img:
        # Convert to RGB as PNG can have an alpha channel which is not supported in PDF
        img_rgb = img.convert('RGB')
        images.append(img_rgb)

# Save images to a PDF
pdf_path = os.path.join(dir_path, "combined.pdf")
images[0].save(pdf_path, save_all=True, append_images=images[1:])

print(f"PDF saved to {pdf_path}")
