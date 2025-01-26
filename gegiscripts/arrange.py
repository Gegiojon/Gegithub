import cv2
import numpy as np
import os
import re

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

# Function to calculate the dimensions of the collage grid
def calculate_dimensions(n):
    """
    Calculate the dimensions of a grid that is as close to square as possible
    and can contain 'n' elements.
    """
    min_diff = n
    best_a = 1
    best_b = n
    
    # Find the pair of numbers that minimize the difference
    for a in range(1, n + 1):
        b = n // a
        if a * b == n:
            diff = abs(a - b)
            if diff < min_diff:
                min_diff = diff
                best_a = a
                best_b = b
    
    return best_a, best_b

# Function to create a collage from images
def create_collage(images, collage_size):
    # Create a blank canvas for the collage
    collage_height = images[0].shape[0] * collage_size[0]
    collage_width = images[0].shape[1] * collage_size[1]
    collage = np.zeros((collage_height, collage_width, 3), dtype=np.uint8)

    # Fill the collage with images
    index = 0
    for row in range(collage_size[0]):
        for col in range(collage_size[1]):
            if index < len(images):
                collage[row * images[0].shape[0]:(row + 1) * images[0].shape[0],
                        col * images[0].shape[1]:(col + 1) * images[0].shape[1]] = images[index]
                index += 1
            else:
                # If all images are used, return the collage
                return collage

    return collage  # Return the collage after all cells are filled

# Directory containing your images
input_dir = r"C:\Users\Usuario\Desktop\PROJECTS\KIOSKOLO\ALMACEN"

# Load all images from the directory
original_images = []
for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)
    print("Loading image:", filepath)  # Print the filename being loaded
    if not filename.startswith("(WRAPPED)"):
        img = cv2.imread(filepath)
        if img is not None:
            print("Image loaded successfully:", filepath)  # Print if the image is loaded successfully
            original_images.append((filename, img))  # Store both filename and image
        else:
            print("Failed to load image:", filepath)  # Print if the image loading failed

# Sort images by filename
original_images.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()))

# Calculate mean dimensions
mean_width, mean_height = calculate_mean_dimensions([img for _, img in original_images])

# Resize images
resized_original_images = resize_images([img for _, img in original_images], mean_width, mean_height)

# Create collages with different numbers of images
output_dir = r"C:\Users\Usuario\Desktop\PROJECTS\KIOSKOLO\KIOSKO\COLLAGES"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for i in range(1, len(original_images) + 1):
    # Calculate the dimensions of the collage grid
    a, b = calculate_dimensions(i)
    collage_size = (a, b)

    # Create collage
    collage = create_collage(resized_original_images[:i], collage_size)

    # Save collage
    cv2.imwrite(os.path.join(output_dir, f"COLLAGE {i}.jpg"), collage)
    print(f"Collage with {i} images saved to:", os.path.join(output_dir, f"COLLAGE {i}.jpg"))
