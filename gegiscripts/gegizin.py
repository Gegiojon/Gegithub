import cv2
import numpy as np
import os

# Function to calculate mean dimensions of images
def calculate_mean_dimensions(images):
    total_width = 0
    total_height = 0
    total_images = len(images)

    for img in images:
        height, width, _ = img.shape
        total_width += width
        total_height += height

    mean_width = int(total_width / total_images)
    mean_height = int(total_height / total_images)

    return mean_width, mean_height

# Function to resize images
def resize_images(images, mean_width, mean_height):
    resized_images = []

    for img in images:
        resized_img = cv2.resize(img, (mean_width, mean_height))
        resized_images.append(resized_img)

    return resized_images

# Directory containing your images
input_dir = r"C:\Users\Usuario\Desktop\PROJECTS\KIOSKOLO\ALMACEN"

# Load all images from the directory
images = []
for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)
    print("Loading image:", filepath)  # Print the filename being loaded
    img = cv2.imread(filepath)
    if img is not None:
        print("Image loaded successfully:", filepath)  # Print if the image is loaded successfully
        images.append((filename, img))  # Store both filename and image
    else:
        print("Failed to load image:", filepath)  # Print if the image loading failed

# Calculate mean dimensions
mean_width, mean_height = calculate_mean_dimensions([img for _, img in images])

# Resize images
resized_images = resize_images([img for _, img in images], mean_width, mean_height)

# Save resized images with original filenames
output_dir = r"C:\Users\Usuario\Desktop\PROJECTS\KIOSKOLO\KIOSKO"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for (filename, resized_img) in zip([name for name, _ in images], resized_images):
    output_path = os.path.join(output_dir, filename)
    cv2.imwrite(output_path, resized_img)

print("Resized images saved to:", output_dir)